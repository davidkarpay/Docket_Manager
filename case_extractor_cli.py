#!/usr/bin/env python3
"""
Interactive Case Data Extractor CLI
Easy-to-use interface for extracting case data from court websites
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better terminal UI: pip install rich")

from case_data_extractor import CaseDataExtractorApp, CasePageScraper


class InteractiveCLI:
    """Interactive command-line interface for case extraction"""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.app: Optional[CaseDataExtractorApp] = None
    
    def print(self, *args, **kwargs):
        """Print wrapper that uses rich if available"""
        if self.console:
            self.console.print(*args, **kwargs)
        else:
            print(*args)
    
    def input(self, prompt: str, default: str = "") -> str:
        """Input wrapper"""
        if RICH_AVAILABLE:
            return Prompt.ask(prompt, default=default) if default else Prompt.ask(prompt)
        else:
            result = input(f"{prompt}: ")
            return result if result else default
    
    def confirm(self, prompt: str, default: bool = True) -> bool:
        """Confirm wrapper"""
        if RICH_AVAILABLE:
            return Confirm.ask(prompt, default=default)
        else:
            while True:
                response = input(f"{prompt} [{'Y/n' if default else 'y/N'}]: ").lower()
                if not response:
                    return default
                if response in ['y', 'yes']:
                    return True
                if response in ['n', 'no']:
                    return False
    
    def show_header(self):
        """Display application header"""
        header = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         CASE DATA EXTRACTOR - Vision AI Edition             ║
║              Local, Private, Secure                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Extract case details from court websites using:
  • Browser automation (Playwright)
  • Local vision AI (LM Studio)
  • No external API calls
  • Complete data privacy
        """
        self.print(header, style="bold cyan" if self.console else None)
    
    def show_menu(self) -> str:
        """Display main menu and get selection"""
        self.print("\n[bold]What would you like to do?[/bold]" if self.console else "\nWhat would you like to do?")
        self.print("1. Extract single case")
        self.print("2. Extract batch from CSV file")
        self.print("3. Interactive search and extract")
        self.print("4. Configure settings")
        self.print("5. Check LM Studio connection")
        self.print("6. Exit")
        
        choice = self.input("\nSelect option [1-6]", "1")
        return choice
    
    async def check_lm_studio(self, url: str = "http://localhost:1234/v1") -> bool:
        """Check if LM Studio is accessible"""
        self.print("\n[yellow]Checking LM Studio connection...[/yellow]" if self.console else "\nChecking LM Studio connection...")
        
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{url}/models")
                response.raise_for_status()
                
                models = response.json()
                if models.get('data'):
                    model_name = models['data'][0].get('id', 'Unknown')
                    self.print(f"[green]✓ Connected to LM Studio[/green]" if self.console else "✓ Connected to LM Studio")
                    self.print(f"  Model: {model_name}")
                    return True
                else:
                    self.print("[yellow]⚠ LM Studio is running but no model loaded[/yellow]" if self.console else "⚠ LM Studio is running but no model loaded")
                    return False
        
        except Exception as e:
            self.print(f"[red]✗ Cannot connect to LM Studio: {e}[/red]" if self.console else f"✗ Cannot connect to LM Studio: {e}")
            self.print("\nMake sure:")
            self.print("  1. LM Studio is running")
            self.print("  2. A vision model is loaded (LLaVA recommended)")
            self.print("  3. Local server is started")
            return False
    
    async def single_case_mode(self):
        """Extract data from a single case"""
        self.print("\n[bold cyan]═══ Single Case Extraction ═══[/bold cyan]" if self.console else "\n=== Single Case Extraction ===")
        
        case_number = self.input("Enter case number (e.g., 2024CF001234)")
        if not case_number:
            self.print("[red]Case number is required[/red]" if self.console else "Case number is required")
            return
        
        url = self.input("Enter case details URL")
        if not url:
            self.print("[red]URL is required[/red]" if self.console else "URL is required")
            return
        
        wait_selector = self.input("CSS selector to wait for (optional, e.g., '.case-details')", "")
        
        headless = self.confirm("Run browser in headless mode? (no UI)", False)
        
        # Initialize app
        self.app = CaseDataExtractorApp(
            output_dir="extracted_cases",
            headless=headless
        )
        
        try:
            self.print(f"\n[yellow]Processing {case_number}...[/yellow]" if self.console else f"\nProcessing {case_number}...")
            
            case_data = await self.app.process_case_url(
                url,
                case_number,
                wait_selector=wait_selector if wait_selector else None
            )
            
            if case_data:
                self.app.results.append(case_data)
                
                # Show extracted data
                self.print("\n[green]✓ Extraction complete![/green]" if self.console else "\n✓ Extraction complete!")
                self.show_case_summary(case_data)
                
                # Export options
                if self.confirm("Export to CSV?", True):
                    filename = self.input("CSV filename", f"{case_number}.csv")
                    self.app.export_to_csv(filename)
                
                if self.confirm("Export to JSON? (includes raw extraction)", False):
                    filename = self.input("JSON filename", f"{case_number}.json")
                    self.app.export_to_json(filename)
            else:
                self.print("[red]✗ Extraction failed[/red]" if self.console else "✗ Extraction failed")
        
        finally:
            await self.app.cleanup()
    
    async def batch_mode(self):
        """Extract data from multiple cases"""
        self.print("\n[bold cyan]═══ Batch Extraction ═══[/bold cyan]" if self.console else "\n=== Batch Extraction ===")
        
        csv_file = self.input("Enter CSV file path (must have 'case_number' and 'url' columns)")
        
        if not Path(csv_file).exists():
            self.print(f"[red]File not found: {csv_file}[/red]" if self.console else f"File not found: {csv_file}")
            return
        
        # Read CSV
        import csv
        cases = []
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'case_number' in row and 'url' in row:
                        cases.append({
                            'case_number': row['case_number'],
                            'url': row['url']
                        })
        except Exception as e:
            self.print(f"[red]Error reading CSV: {e}[/red]" if self.console else f"Error reading CSV: {e}")
            return
        
        if not cases:
            self.print("[red]No valid cases found in CSV[/red]" if self.console else "No valid cases found in CSV")
            return
        
        self.print(f"\nFound {len(cases)} cases to process")
        
        if not self.confirm(f"Process all {len(cases)} cases?", True):
            return
        
        wait_selector = self.input("CSS selector to wait for (optional)", "")
        delay = int(self.input("Delay between cases (seconds)", "3"))
        headless = self.confirm("Run browser in headless mode?", True)
        
        # Initialize app
        self.app = CaseDataExtractorApp(
            output_dir="extracted_cases",
            headless=headless
        )
        
        try:
            await self.app.process_batch(
                cases,
                wait_selector=wait_selector if wait_selector else None,
                delay_between_cases=delay
            )
            
            self.print(f"\n[green]✓ Batch processing complete![/green]" if self.console else "\n✓ Batch processing complete!")
            self.print(f"Successfully extracted: {len(self.app.results)} / {len(cases)} cases")
            
            # Auto export
            self.app.export_to_csv()
            self.app.export_to_json()
        
        finally:
            await self.app.cleanup()
    
    async def search_mode(self):
        """Interactive search and extract"""
        self.print("\n[bold cyan]═══ Interactive Search Mode ═══[/bold cyan]" if self.console else "\n=== Interactive Search Mode ===")
        self.print("[yellow]This mode requires you to configure site-specific selectors[/yellow]" if self.console else "This mode requires you to configure site-specific selectors")
        
        search_url = self.input("Enter court search page URL")
        case_number = self.input("Enter case number to search")
        
        self.print("\nYou'll need to identify CSS selectors:")
        search_input_selector = self.input("  Case number input field selector (e.g., '#caseNumber')")
        search_button_selector = self.input("  Search button selector (e.g., '#searchBtn')")
        result_link_selector = self.input("  Result link selector (e.g., '.case-link')")
        
        headless = self.confirm("Run browser in headless mode?", False)
        
        # Initialize
        self.app = CaseDataExtractorApp(headless=headless)
        
        try:
            async with CasePageScraper(headless=headless) as scraper:
                page = await scraper.browser.new_page()
                
                self.print(f"\n[yellow]Navigating to search page...[/yellow]" if self.console else "\nNavigating to search page...")
                await page.goto(search_url)
                
                self.print("[yellow]Filling search form...[/yellow]" if self.console else "Filling search form...")
                await page.fill(search_input_selector, case_number)
                await page.click(search_button_selector)
                
                self.print("[yellow]Waiting for results...[/yellow]" if self.console else "Waiting for results...")
                await page.wait_for_selector(result_link_selector)
                
                self.print("[yellow]Clicking first result...[/yellow]" if self.console else "Clicking first result...")
                await page.click(f"{result_link_selector}:first-child")
                
                # Get URL
                await asyncio.sleep(2)
                url = page.url
                
                self.print(f"\n[green]Found case at: {url}[/green]" if self.console else f"\nFound case at: {url}")
                await page.close()
            
            # Now extract with vision
            case_data = await self.app.process_case_url(url, case_number)
            
            if case_data:
                self.app.results.append(case_data)
                self.print("\n[green]✓ Extraction complete![/green]" if self.console else "\n✓ Extraction complete!")
                self.show_case_summary(case_data)
                
                if self.confirm("Export results?", True):
                    self.app.export_to_csv(f"{case_number}.csv")
                    self.app.export_to_json(f"{case_number}.json")
        
        except Exception as e:
            self.print(f"[red]Error: {e}[/red]" if self.console else f"Error: {e}")
        
        finally:
            await self.app.cleanup()
    
    def show_case_summary(self, case_data):
        """Display summary of extracted case data"""
        if self.console:
            table = Table(title="Extracted Data")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")
            
            for field, value in case_data.__dict__.items():
                if field not in ['raw_extraction', 'extracted_at'] and value:
                    table.add_row(field.replace('_', ' ').title(), str(value))
            
            self.console.print(table)
        else:
            self.print("\n--- Extracted Data ---")
            for field, value in case_data.__dict__.items():
                if field not in ['raw_extraction', 'extracted_at'] and value:
                    self.print(f"{field.replace('_', ' ').title()}: {value}")
    
    async def configure_settings(self):
        """Configure application settings"""
        self.print("\n[bold cyan]═══ Settings ═══[/bold cyan]" if self.console else "\n=== Settings ===")
        
        current_url = "http://localhost:1234/v1"
        self.print(f"Current LM Studio URL: {current_url}")
        
        new_url = self.input("New LM Studio URL (press Enter to keep current)", current_url)
        
        # Test connection
        await self.check_lm_studio(new_url)
        
        output_dir = self.input("Output directory", "extracted_cases")
        self.print(f"\nSettings updated. Output directory: {output_dir}")
    
    async def run(self):
        """Main application loop"""
        self.show_header()
        
        # Check LM Studio on startup
        if not await self.check_lm_studio():
            if not self.confirm("\nLM Studio is not accessible. Continue anyway?", False):
                return
        
        while True:
            try:
                choice = self.show_menu()
                
                if choice == "1":
                    await self.single_case_mode()
                elif choice == "2":
                    await self.batch_mode()
                elif choice == "3":
                    await self.search_mode()
                elif choice == "4":
                    await self.configure_settings()
                elif choice == "5":
                    await self.check_lm_studio()
                elif choice == "6":
                    self.print("\n[cyan]Goodbye![/cyan]" if self.console else "\nGoodbye!")
                    break
                else:
                    self.print("[red]Invalid choice[/red]" if self.console else "Invalid choice")
                
                if choice in ["1", "2", "3"]:
                    if not self.confirm("\nReturn to main menu?", True):
                        break
            
            except KeyboardInterrupt:
                self.print("\n\n[yellow]Interrupted by user[/yellow]" if self.console else "\n\nInterrupted by user")
                break
            except Exception as e:
                self.print(f"\n[red]Error: {e}[/red]" if self.console else f"\nError: {e}")
                import traceback
                traceback.print_exc()


def main():
    """Entry point"""
    cli = InteractiveCLI()
    try:
        asyncio.run(cli.run())
    except KeyboardInterrupt:
        print("\n\nExiting...")


if __name__ == "__main__":
    main()
