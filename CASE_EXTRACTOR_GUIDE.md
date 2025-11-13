# Case Data Extractor - Complete Setup & Usage Guide

## 🎯 Overview

This tool extracts case details from court websites using:
- **Browser automation** (Playwright) - simulates human browsing
- **Local vision AI** (LM Studio) - reads screenshots using AI
- **Complete privacy** - everything runs on your machine
- **No external APIs** - no data leaves your network

Perfect for public defenders who need to extract and organize case data from court websites.

## 📋 Prerequisites

### System Requirements
- **RAM**: 16GB+ recommended (12GB for AI model, 4GB for system/browser)
- **Storage**: ~10GB for model files + output data
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: 3.10 or newer

### Check Your Python Version
```bash
python --version  # Should show 3.10 or higher
# If not installed, download from https://www.python.org/downloads/
```

## 🚀 Quick Start (5 Steps)

### 1. Install Dependencies
```bash
# Navigate to the tool directory
cd /path/to/case_extractor

# Install Python packages
pip install -r case_extractor_requirements.txt

# Install Playwright browser (one-time setup)
playwright install chromium
```

### 2. Install LM Studio
- Download from **https://lmstudio.ai/**
- Install and launch the application
- LM Studio is free and user-friendly

### 3. Download Vision Model in LM Studio

**Recommended Model: LLaVA 1.6 Mistral 7B** (fits in 16GB RAM)

Steps:
1. Open LM Studio
2. Click the **🔍 Search** icon
3. Search for: `llava-v1.6-mistral-7b`
4. Click the model → Click **Download**
5. Wait for download (~8GB)

**Alternative models** (if you have issues):
- **BakLLaVA 7B** - Good for document extraction
- **LLaVA 1.5 13B** - More accurate (needs ~14GB RAM)

### 4. Load Model and Start Server

In LM Studio:
1. Go to **💬 Chat** tab
2. Click **"Select a model to load"**
3. Choose your downloaded LLaVA model
4. Click **Load** → Wait for "Model loaded"
5. Go to **↔️ Local Server** tab
6. Click **Start Server**
7. Verify it says "Server running on http://localhost:1234"

**Keep LM Studio running while using the extractor!**

### 5. Run the Tool

**Easy way (Interactive menu)**:
```bash
python case_extractor_cli.py
```

**Or edit and run examples**:
```bash
python case_data_extractor.py
```

## 📖 Usage Guide

### Interactive CLI Mode (Recommended for Beginners)

```bash
python case_extractor_cli.py
```

**Menu Options**:

1. **Extract Single Case** - One-off case extraction
   - Enter case number and URL
   - See browser work in real-time (or hide it)
   - Immediate results

2. **Extract Batch from CSV** - Process multiple cases
   - Prepare CSV with case_number and url columns
   - Automated processing with rate limiting
   - Bulk export

3. **Interactive Search** - Search court website and extract
   - Configure search selectors
   - Automated search → click → extract
   - Great for repetitive workflows

4. **Configure Settings** - Change LM Studio URL, output directory

5. **Check LM Studio Connection** - Test setup

### Single Case Example

```python
import asyncio
from case_data_extractor import CaseDataExtractorApp

async def main():
    app = CaseDataExtractorApp(
        output_dir="extracted_cases",
        headless=False  # False = see browser, True = hide browser
    )
    
    try:
        case_data = await app.process_case_url(
            url="https://mycourtwebsite.com/case/2024CF001234",
            case_number="2024CF001234",
            wait_selector=".case-details"  # CSS selector to wait for (optional)
        )
        
        if case_data:
            app.results.append(case_data)
            app.export_to_csv("my_case.csv")
            app.export_to_json("my_case.json")
            print(f"✓ Extracted: {case_data.client_name}")
    
    finally:
        await app.cleanup()

asyncio.run(main())
```

### Batch Processing Example

1. **Create `cases_to_process.csv`**:
```csv
case_number,url
2024CF001234,https://mycourtwebsite.com/case/2024CF001234
2024CF001235,https://mycourtwebsite.com/case/2024CF001235
2024CF005678,https://mycourtwebsite.com/case/2024CF005678
```

2. **Run batch script**:
```python
import asyncio
import csv
from case_data_extractor import CaseDataExtractorApp

async def batch_extract():
    app = CaseDataExtractorApp(headless=True)  # Hide browser for batch
    
    # Load cases from CSV
    cases = []
    with open('cases_to_process.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append({
                'case_number': row['case_number'],
                'url': row['url']
            })
    
    print(f"Processing {len(cases)} cases...")
    
    try:
        await app.process_batch(
            cases,
            wait_selector=".case-details",
            delay_between_cases=3  # Be nice to court servers!
        )
        
        # Auto-export
        app.export_to_csv()  # Creates timestamped CSV
        app.export_to_json()  # Creates timestamped JSON
        
        print(f"✓ Complete! {len(app.results)} cases extracted")
    
    finally:
        await app.cleanup()

asyncio.run(batch_extract())
```

## 📊 Output Files

### File Structure
```
extracted_cases/
├── screenshots/                                    # Visual verification
│   ├── 2024CF001234_20250112_143022.png
│   ├── 2024CF001235_20250112_143045.png
│   └── ...
├── extracted_cases_20250112_143100.csv           # Import to docket manager
└── extracted_cases_20250112_143100.json          # Full data + debugging
```

### CSV Fields Extracted

All fields compatible with your docket manager:
- `case_number` - Case/docket number
- `client_name` - Defendant name
- `next_date` - Next court appearance
- `charges` - All charges listed
- `attorney` - Attorney of record
- `judge` - Assigned judge
- `division` - Court division/department
- `status` - Case status
- `bond_amount` - Bond/bail amount
- `arrest_date` - Arrest date
- `filing_date` - Filing/charge date
- `disposition` - Case disposition
- `plea` - Plea information
- `sentence` - Sentence if any
- `probation_info` - Probation details
- `victim_info` - Victim information (if visible)
- `notes` - Additional notes
- `page_url` - Source URL
- `extracted_at` - Timestamp

### Import to Docket Manager

1. Run extractor → generates CSV
2. Open `morning_docket_manager_with_database.html`
3. Click "Choose File" → select generated CSV
4. Data populates automatically!

## 🔧 Troubleshooting

### "Cannot connect to LM Studio"

**Checklist**:
- [ ] LM Studio is running
- [ ] Model is loaded (look for "Model loaded" message)
- [ ] Server is started (Local Server tab)
- [ ] http://localhost:1234/v1/models works in browser

**Fix**: Restart LM Studio, reload model, restart server

### Data Extraction is Incomplete

**Solutions**:
1. **Check screenshot** - Look in `extracted_cases/screenshots/` to see if full page captured
2. **Try larger model** - Use LLaVA 1.5 13B instead of 7B
3. **Increase wait time** - Add longer wait_selector or increase timeout
4. **Adjust prompt** - Edit prompt in `LMStudioVisionClient.extract_case_data()`

### "Browser not found" Error

```bash
# Reinstall Playwright browsers
playwright install chromium
```

### "Timeout waiting for selector"

**Causes**:
- Page loads slowly
- Wrong CSS selector
- Content is dynamic/JavaScript-heavy

**Solutions**:
- Remove `wait_selector` parameter (let it wait for networkidle)
- Increase timeout: `await page.wait_for_selector(selector, timeout=30000)`
- Use browser developer tools to find correct selector

### Out of Memory Errors

**Solutions**:
1. Use 7B model instead of 13B
2. Close other applications
3. Run browser in headless mode (`headless=True`)
4. Process smaller batches (10-20 cases at a time)

## 🔒 Privacy & Security Features

### ✅ What Stays Local
- All case data
- All screenshots
- All AI processing
- All extracted information

### ✅ Security Benefits
- No cloud services
- No external APIs
- No data transmission
- Works on air-gapped networks
- You control all data

### 🛡️ Best Practices

1. **Secure storage**: Set proper file permissions on output directory
   ```bash
   chmod 700 extracted_cases/
   ```

2. **Data retention**: Delete screenshots after verification
   ```python
   import shutil
   shutil.rmtree('extracted_cases/screenshots')
   ```

3. **Access control**: Run tool as limited user, not admin

4. **Audit trail**: JSON files include timestamps for verification

5. **Manual review**: Always verify extracted data

## ⚖️ Legal & Ethical Considerations

### ✅ Appropriate Uses
- Cases you're assigned to represent
- Building your case management database
- Automating data entry tasks
- Analyzing your own caseload
- Improving public defender workflows

### ❌ Inappropriate Uses
- Accessing unauthorized cases
- Bypassing authentication
- Excessive automated requests
- Sharing data beyond authorized personnel
- Commercial use without court permission

### Important Guidelines

**Rate Limiting**: 
```python
delay_between_cases=3  # Minimum 3 seconds between requests
```

**Authentication**: This tool does NOT handle logins. You must:
- Log in manually to court website
- Keep session active
- Tool uses your authenticated session

**Court Rules**: Check local rules on automated access

**Data Retention**: Follow applicable policies for case data

## 🎓 How It Works (Technical Overview)

### Process Flow

```
1. Playwright opens Chromium browser
   ↓
2. Navigates to case URL (using your session)
   ↓
3. Waits for page to load fully
   ↓
4. Captures full-page screenshot
   ↓
5. Converts screenshot to base64
   ↓
6. Sends to local LM Studio vision model
   ↓
7. AI "reads" screenshot and extracts structured data
   ↓
8. Returns JSON with all visible fields
   ↓
9. Saves to CSV/JSON files
```

### Why Vision AI vs Traditional Scraping?

| Traditional Scraping | Vision AI Approach |
|---------------------|-------------------|
| Breaks when HTML changes | Works on any visual layout |
| Custom code per website | Universal approach |
| Fails on dynamic content | Handles any rendering |
| Complex maintenance | Minimal maintenance |

### Model Comparison

| Model | RAM | Speed | Accuracy | When to Use |
|-------|-----|-------|----------|-------------|
| LLaVA 1.6 Mistral 7B | 8GB | Fast | Good | Daily use, batch processing |
| BakLLaVA 7B | 8GB | Fast | Good | Document-heavy pages |
| LLaVA 1.5 13B | 14GB | Slower | Better | Complex layouts, critical cases |

## 💡 Real-World Workflows

### Morning Docket Prep

```bash
# 1. Get today's docket CSV from court
# 2. Extract case numbers
# 3. Generate URLs programmatically
# 4. Run batch extraction
python case_extractor_cli.py  # Option 2: Batch mode

# 5. Import CSV to docket manager
# 6. Review and add notes
# 7. Ready for court!
```

### New Client Intake

```bash
# 1. Get case number from client
# 2. Run single case extraction
python case_extractor_cli.py  # Option 1: Single case

# 3. Review extracted charges, dates, bond
# 4. Export for case file
# 5. Use data for initial strategy
```

### Weekly Case Review

```python
# Extract all active cases
# Analyze patterns (charge types, judges, outcomes)
# Export for reporting

cases = get_all_active_cases()  # Your logic here
await app.process_batch(cases)
app.export_to_csv(f"weekly_review_{date.today()}.csv")
```

## 🚀 Advanced Customization

### Custom Extraction Fields

Edit `LMStudioVisionClient.extract_case_data()` prompt:

```python
prompt = f"""Extract these specific fields for {jurisdiction}:
- vop_date: Violation of probation date
- public_defender_appointed: Date PD appointed
- discovery_deadline: Discovery deadline date
- trial_date: Trial date if scheduled
- pretrial_motions: List of pending motions

[rest of prompt]
"""
```

### Multi-Jurisdiction Support

```python
# config.py
COURT_CONFIGS = {
    'palm_beach': {
        'base_url': 'https://pbcounty.courts.gov',
        'case_url_template': 'https://pbcounty.courts.gov/case/{case_number}',
        'wait_selector': '.case-info-panel',
        'rate_limit': 3
    },
    'broward': {
        'base_url': 'https://broward.courts.gov',
        'case_url_template': 'https://broward.courts.gov/CaseDetail.aspx?caseno={case_number}',
        'wait_selector': '#caseDetails',
        'rate_limit': 5
    }
}

# Use in your code
config = COURT_CONFIGS['palm_beach']
url = config['case_url_template'].format(case_number=case_no)
```

### Automated Daily Runs

**Linux/Mac (cron)**:
```bash
# Edit crontab
crontab -e

# Run at 6 AM daily
0 6 * * * cd /home/user/case_extractor && /usr/bin/python3 batch_extract.py
```

**Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 6:00 AM
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:\CaseExtractor\batch_extract.py`
7. Start in: `C:\CaseExtractor`

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Save Page HTML

```python
# After navigating
html = await page.content()
Path('debug_page.html').write_text(html)
```

### Test Vision Model Separately

```python
# Test with a known-good screenshot
from case_data_extractor import LMStudioVisionClient
import base64

client = LMStudioVisionClient()
with open('test_screenshot.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

result = await client.extract_case_data(img_b64, "TEST123")
print(json.dumps(result, indent=2))
```

### Inspect Screenshots

Always check `extracted_cases/screenshots/` to verify:
- Full page is captured
- Text is readable
- Data you want is visible
- No authentication overlays

## 📚 Resources

- **LM Studio Documentation**: https://lmstudio.ai/docs
- **Playwright Python**: https://playwright.dev/python/docs/intro
- **LLaVA Models**: https://llava-vl.github.io/
- **Vision Model Papers**: Check LM Studio's model descriptions

## 🆘 Getting Help

### Checklist Before Asking for Help

- [ ] LM Studio is running with model loaded
- [ ] Server started in LM Studio
- [ ] Playwright browsers installed (`playwright install chromium`)
- [ ] Checked screenshots for quality
- [ ] Tested with single case first
- [ ] Reviewed error messages carefully

### Common Questions

**Q: Can this work with password-protected court sites?**  
A: Yes! Log in manually first. Tool uses your authenticated session.

**Q: How do I find CSS selectors?**  
A: 
1. Open court website
2. Right-click element → Inspect
3. Right-click in DevTools → Copy → Copy selector

**Q: Can I run this on a laptop?**  
A: Yes, if you have 16GB RAM. Close other apps while running.

**Q: Does this violate court website terms?**  
A: Check your court's terms. Generally OK for authorized users doing legitimate work with reasonable rate limiting.

**Q: Can I process 100+ cases at once?**  
A: Yes, but be respectful:
- Use 3-5 second delays
- Run during off-peak hours
- Consider breaking into batches

## 📝 Example: Complete Workflow Script

```python
#!/usr/bin/env python3
"""
daily_docket_extraction.py
Complete workflow for daily docket prep
"""

import asyncio
import csv
from datetime import date
from pathlib import Path
from case_data_extractor import CaseDataExtractorApp

async def main():
    # Configuration
    TODAY = date.today().strftime('%Y%m%d')
    COURT_BASE_URL = "https://mycourtwebsite.com/case/"
    INPUT_CSV = "morning_docket.csv"  # From court system
    OUTPUT_DIR = f"dockets/{TODAY}"
    
    # Create output directory
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    # Load cases from court CSV
    print(f"Loading cases from {INPUT_CSV}...")
    cases = []
    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            case_no = row['case_number']
            cases.append({
                'case_number': case_no,
                'url': f"{COURT_BASE_URL}{case_no}"
            })
    
    print(f"Found {len(cases)} cases to process")
    
    # Initialize extractor
    app = CaseDataExtractorApp(
        output_dir=OUTPUT_DIR,
        headless=True  # Run quietly
    )
    
    try:
        # Process all cases
        await app.process_batch(
            cases,
            wait_selector=".case-details",
            delay_between_cases=4  # Respectful rate limit
        )
        
        # Export results
        csv_file = f"docket_extracted_{TODAY}.csv"
        json_file = f"docket_extracted_{TODAY}.json"
        
        app.export_to_csv(csv_file)
        app.export_to_json(json_file)
        
        print(f"\n{'='*60}")
        print(f"✓ Extraction complete!")
        print(f"  Processed: {len(cases)} cases")
        print(f"  Successful: {len(app.results)} cases")
        print(f"  CSV: {OUTPUT_DIR}/{csv_file}")
        print(f"  JSON: {OUTPUT_DIR}/{json_file}")
        print(f"{'='*60}")
        
        # Print summary
        print("\nReady to import into docket manager!")
        print(f"1. Open morning_docket_manager_with_database.html")
        print(f"2. Choose file: {OUTPUT_DIR}/{csv_file}")
        print(f"3. Review and add notes")
        
    finally:
        await app.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🎉 You're Ready!

This tool is designed to save you time so you can focus on what matters: **representing your clients effectively**.

**Next Steps**:
1. Complete setup (5 steps above)
2. Test with a single case
3. Refine for your court's website
4. Integrate into your daily workflow
5. Customize as needed

**Built for public defenders who code. Made with ❤️ for justice.**

Questions? Issues? Customization needs? This is open-source—make it yours!
