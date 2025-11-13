#!/usr/bin/env python3
"""
Case Data Extractor - Local Web Scraping + Vision AI Tool
Extracts case details from court websites using browser automation and local LLM vision models
"""

import asyncio
import json
import csv
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import os

from playwright.async_api import async_playwright, Page, Browser
import httpx


@dataclass
class CaseData:
    """Structured case data extracted from court pages"""
    case_number: str
    client_name: str
    next_date: Optional[str] = None
    charges: Optional[str] = None
    attorney: Optional[str] = None
    judge: Optional[str] = None
    division: Optional[str] = None
    status: Optional[str] = None
    bond_amount: Optional[str] = None
    arrest_date: Optional[str] = None
    filing_date: Optional[str] = None
    disposition: Optional[str] = None
    plea: Optional[str] = None
    sentence: Optional[str] = None
    probation_info: Optional[str] = None
    prior_record: Optional[str] = None
    victim_info: Optional[str] = None
    notes: Optional[str] = None
    page_url: Optional[str] = None
    extracted_at: Optional[str] = None
    raw_extraction: Optional[Dict] = None


class LMStudioVisionClient:
    """Client for LM Studio's OpenAI-compatible API with vision support"""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def extract_case_data(
        self, 
        screenshot_b64: str, 
        case_number: str,
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """
        Send screenshot to vision model and extract structured case data
        """
        
        prompt = f"""You are a legal data extraction assistant helping a public defender extract case information from court website screenshots.

CASE NUMBER: {case_number}
{additional_context}

Analyze this screenshot of a case details page and extract ALL visible information into a structured JSON format.

Extract the following fields if visible (use null for missing data):
- client_name: Full name of the defendant/client
- next_date: Next court date (format: YYYY-MM-DD if possible)
- charges: All charges listed (comma-separated if multiple)
- attorney: Attorney name(s)
- judge: Judge name
- division: Court division/department
- status: Case status
- bond_amount: Bond/bail amount
- arrest_date: Date of arrest
- filing_date: Filing/charge date
- disposition: Case disposition if any
- plea: Plea information
- sentence: Sentence information if any
- probation_info: Probation details
- victim_info: Victim information (redact personal details, keep case-relevant info)
- additional_fields: Any other important fields you see as key-value pairs

CRITICAL INSTRUCTIONS:
1. Extract ALL visible text data, even if uncertain about field names
2. Be precise with dates - convert to YYYY-MM-DD format when possible
3. For unclear fields, include them in "additional_fields" with descriptive keys
4. If multiple values exist (e.g., multiple charges), list them all
5. Preserve exact legal terminology and case numbers
6. Return ONLY valid JSON, no additional commentary

Return the data as a JSON object."""

        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": "local-model",  # LM Studio uses the loaded model
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{screenshot_b64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.1,  # Low temperature for factual extraction
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract the JSON from the response
            content = result['choices'][0]['message']['content']
            
            # Try to parse JSON from the response
            # Handle cases where model includes markdown code blocks
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            extracted_data = json.loads(content)
            return extracted_data
            
        except Exception as e:
            print(f"Error calling LM Studio API: {e}")
            return {"error": str(e), "raw_response": content if 'content' in locals() else None}
    
    async def close(self):
        await self.client.aclose()


class CasePageScraper:
    """Handles browser automation and screenshot capture"""
    
    def __init__(self, headless: bool = False, slow_mo: int = 100):
        self.headless = headless
        self.slow_mo = slow_mo
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def navigate_and_screenshot(
        self, 
        url: str,
        wait_selector: Optional[str] = None,
        wait_time: int = 2000
    ) -> tuple[bytes, Page]:
        """
        Navigate to URL and capture screenshot
        
        Args:
            url: Target URL
            wait_selector: Optional CSS selector to wait for before screenshot
            wait_time: Additional wait time in milliseconds
        
        Returns:
            Tuple of (screenshot_bytes, page)
        """
        page = await self.browser.new_page(
            viewport={'width': 1920, 'height': 1080}
        )
        
        try:
            print(f"Navigating to: {url}")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            if wait_selector:
                await page.wait_for_selector(wait_selector, timeout=10000)
            
            await asyncio.sleep(wait_time / 1000)
            
            # Capture full page screenshot
            screenshot = await page.screenshot(full_page=True, type='png')
            
            return screenshot, page
            
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            await page.close()
            raise
    
    async def extract_case_links(
        self, 
        page: Page, 
        selector: str
    ) -> List[str]:
        """Extract case detail page links from a listing page"""
        links = await page.locator(selector).all()
        urls = []
        for link in links:
            href = await link.get_attribute('href')
            if href:
                # Handle relative URLs
                if href.startswith('http'):
                    urls.append(href)
                else:
                    base = page.url.rsplit('/', 1)[0]
                    urls.append(f"{base}/{href}")
        return urls


class CaseDataExtractorApp:
    """Main application orchestrating the extraction process"""
    
    def __init__(
        self, 
        output_dir: str = "extracted_cases",
        lm_studio_url: str = "http://localhost:1234/v1",
        headless: bool = False
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.screenshots_dir = self.output_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
        
        self.vision_client = LMStudioVisionClient(lm_studio_url)
        self.headless = headless
        
        self.results: List[CaseData] = []
    
    async def process_case_url(
        self, 
        url: str,
        case_number: str,
        wait_selector: Optional[str] = None
    ) -> Optional[CaseData]:
        """Process a single case URL"""
        
        print(f"\n{'='*60}")
        print(f"Processing: {case_number}")
        print(f"URL: {url}")
        print(f"{'='*60}")
        
        async with CasePageScraper(headless=self.headless) as scraper:
            try:
                # Capture screenshot
                screenshot_bytes, page = await scraper.navigate_and_screenshot(
                    url, 
                    wait_selector=wait_selector
                )
                
                # Save screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = self.screenshots_dir / f"{case_number}_{timestamp}.png"
                screenshot_path.write_bytes(screenshot_bytes)
                print(f"Screenshot saved: {screenshot_path}")
                
                # Convert to base64 for API
                screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
                
                # Extract data using vision model
                print("Sending to vision model for extraction...")
                extracted = await self.vision_client.extract_case_data(
                    screenshot_b64, 
                    case_number
                )
                
                print("Extraction complete!")
                print(json.dumps(extracted, indent=2))
                
                # Build CaseData object
                case_data = CaseData(
                    case_number=case_number,
                    client_name=extracted.get('client_name', ''),
                    next_date=extracted.get('next_date'),
                    charges=extracted.get('charges'),
                    attorney=extracted.get('attorney'),
                    judge=extracted.get('judge'),
                    division=extracted.get('division'),
                    status=extracted.get('status'),
                    bond_amount=extracted.get('bond_amount'),
                    arrest_date=extracted.get('arrest_date'),
                    filing_date=extracted.get('filing_date'),
                    disposition=extracted.get('disposition'),
                    plea=extracted.get('plea'),
                    sentence=extracted.get('sentence'),
                    probation_info=extracted.get('probation_info'),
                    victim_info=extracted.get('victim_info'),
                    notes=extracted.get('notes'),
                    page_url=url,
                    extracted_at=datetime.now().isoformat(),
                    raw_extraction=extracted
                )
                
                await page.close()
                return case_data
                
            except Exception as e:
                print(f"Error processing {case_number}: {e}")
                import traceback
                traceback.print_exc()
                return None
    
    async def process_batch(
        self, 
        cases: List[Dict[str, str]],
        wait_selector: Optional[str] = None,
        delay_between_cases: int = 2
    ):
        """
        Process multiple cases
        
        Args:
            cases: List of dicts with 'case_number' and 'url' keys
            wait_selector: CSS selector to wait for on each page
            delay_between_cases: Seconds to wait between requests
        """
        
        for i, case_info in enumerate(cases, 1):
            print(f"\n\n{'#'*60}")
            print(f"PROCESSING CASE {i}/{len(cases)}")
            print(f"{'#'*60}")
            
            case_data = await self.process_case_url(
                case_info['url'],
                case_info['case_number'],
                wait_selector
            )
            
            if case_data:
                self.results.append(case_data)
            
            # Rate limiting
            if i < len(cases):
                print(f"\nWaiting {delay_between_cases} seconds before next case...")
                await asyncio.sleep(delay_between_cases)
    
    def export_to_csv(self, filename: Optional[str] = None):
        """Export results to CSV"""
        if not self.results:
            print("No results to export")
            return
        
        if filename is None:
            filename = f"extracted_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        output_path = self.output_dir / filename
        
        # Get all unique fields from all results
        all_fields = set()
        for case in self.results:
            case_dict = asdict(case)
            all_fields.update(case_dict.keys())
        
        # Remove raw_extraction from CSV (too large)
        all_fields.discard('raw_extraction')
        
        fieldnames = sorted(all_fields)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for case in self.results:
                case_dict = asdict(case)
                case_dict.pop('raw_extraction', None)
                writer.writerow(case_dict)
        
        print(f"\n{'='*60}")
        print(f"CSV exported: {output_path}")
        print(f"Total cases: {len(self.results)}")
        print(f"{'='*60}")
    
    def export_to_json(self, filename: Optional[str] = None):
        """Export results to JSON (includes raw extraction data)"""
        if not self.results:
            print("No results to export")
            return
        
        if filename is None:
            filename = f"extracted_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                [asdict(case) for case in self.results],
                f,
                indent=2,
                default=str
            )
        
        print(f"\nJSON exported: {output_path}")
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.vision_client.close()


# Example usage functions

async def example_single_case():
    """Example: Extract data from a single case URL"""
    
    app = CaseDataExtractorApp(
        output_dir="extracted_cases",
        lm_studio_url="http://localhost:1234/v1",
        headless=False  # Set to True to hide browser
    )
    
    # Replace with actual case URL
    case_url = "https://courtwebsite.example.com/case/2024CF001234"
    case_number = "2024CF001234"
    
    try:
        case_data = await app.process_case_url(
            case_url,
            case_number,
            wait_selector=".case-details"  # Adjust selector as needed
        )
        
        if case_data:
            app.results.append(case_data)
            app.export_to_csv("single_case.csv")
            app.export_to_json("single_case.json")
    
    finally:
        await app.cleanup()


async def example_batch_from_csv():
    """Example: Process cases from a CSV file with case numbers and URLs"""
    
    app = CaseDataExtractorApp(
        output_dir="extracted_cases",
        headless=False
    )
    
    # Read cases from CSV
    cases = []
    with open('cases_to_process.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append({
                'case_number': row['case_number'],
                'url': row['url']
            })
    
    try:
        await app.process_batch(
            cases,
            wait_selector=".case-details",  # Adjust as needed
            delay_between_cases=3  # Be respectful to the server
        )
        
        app.export_to_csv()
        app.export_to_json()
    
    finally:
        await app.cleanup()


async def example_with_search():
    """Example: Search for a case and extract details"""
    
    app = CaseDataExtractorApp(headless=False)
    
    async with CasePageScraper(headless=False) as scraper:
        # Navigate to search page
        page = await scraper.browser.new_page()
        await page.goto("https://courtwebsite.example.com/search")
        
        # Fill in search form (adjust selectors as needed)
        await page.fill("#case-number-input", "2024CF001234")
        await page.click("#search-button")
        
        # Wait for results
        await page.wait_for_selector(".search-results")
        
        # Click on first result
        await page.click(".case-link:first-child")
        
        # Wait for case details page
        await page.wait_for_selector(".case-details")
        
        # Get URL and case number
        url = page.url
        case_number = "2024CF001234"
        
        await page.close()
    
    # Now process with vision
    try:
        case_data = await app.process_case_url(url, case_number)
        if case_data:
            app.results.append(case_data)
            app.export_to_csv()
    
    finally:
        await app.cleanup()


if __name__ == "__main__":
    # Choose which example to run
    print("""
    Case Data Extractor - Local Vision AI Tool
    ==========================================
    
    Before running:
    1. Start LM Studio and load a vision model (LLaVA 1.6 Mistral 7B recommended)
    2. Enable the local server in LM Studio
    3. Prepare your case URLs
    
    Uncomment the example you want to run below.
    """)
    
    # Uncomment one of these:
    # asyncio.run(example_single_case())
    # asyncio.run(example_batch_from_csv())
    # asyncio.run(example_with_search())
    
    print("\nEdit the file to uncomment an example or create your own workflow.")
