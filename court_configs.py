"""
Court Configuration Template
Copy and customize this file for your specific court system
"""

# Example: Palm Beach County Courts Configuration
PALM_BEACH_CONFIG = {
    'name': 'Palm Beach County Circuit Court',
    'base_url': 'https://courtwebsite.example.com',
    'case_url_template': 'https://courtwebsite.example.com/case/{case_number}',
    
    # Browser automation settings
    'wait_selector': '.case-details',  # CSS selector to wait for on case pages
    'wait_timeout': 10000,  # Milliseconds to wait for selector
    'additional_wait': 2000,  # Extra wait after selector found
    
    # Rate limiting (be respectful!)
    'rate_limit_seconds': 3,  # Seconds between requests
    'batch_size': 20,  # Max cases per batch before pause
    'batch_pause_seconds': 60,  # Pause between batches
    
    # Search page configuration (if using search feature)
    'search_url': 'https://courtwebsite.example.com/search',
    'search_selectors': {
        'case_number_input': '#caseNumber',
        'search_button': '#searchBtn',
        'result_link': '.case-link',
    },
    
    # Extraction customization
    'custom_fields': [
        # Add jurisdiction-specific fields here
        'vop_date',
        'public_defender_appointed',
        'discovery_deadline',
    ],
    
    # Output settings
    'output_dir': 'extracted_cases/palm_beach',
    'csv_filename_template': 'pb_cases_{date}.csv',
}

# Example: Broward County Courts Configuration  
BROWARD_CONFIG = {
    'name': 'Broward County Circuit Court',
    'base_url': 'https://browardcourts.example.com',
    'case_url_template': 'https://browardcourts.example.com/CaseDetail.aspx?caseno={case_number}',
    
    'wait_selector': '#caseDetails',
    'wait_timeout': 15000,
    'additional_wait': 3000,
    
    'rate_limit_seconds': 5,  # Slower for this court
    'batch_size': 10,
    'batch_pause_seconds': 120,
    
    'search_url': 'https://browardcourts.example.com/CaseSearch',
    'search_selectors': {
        'case_number_input': 'input[name="caseNum"]',
        'search_button': 'button[type="submit"]',
        'result_link': 'a.caseLink',
    },
    
    'custom_fields': [
        'preliminary_hearing_date',
        'grand_jury_date',
    ],
    
    'output_dir': 'extracted_cases/broward',
    'csv_filename_template': 'broward_cases_{date}.csv',
}

# Add your court configuration here
MY_COURT_CONFIG = {
    'name': 'My Court Name',
    'base_url': 'https://mycourtwebsite.com',
    'case_url_template': 'https://mycourtwebsite.com/case/{case_number}',
    
    # Browser settings
    'wait_selector': None,  # Leave None to wait for networkidle instead
    'wait_timeout': 10000,
    'additional_wait': 2000,
    
    # Rate limiting
    'rate_limit_seconds': 3,
    'batch_size': 20,
    'batch_pause_seconds': 60,
    
    # Search (optional - leave None if not using)
    'search_url': None,
    'search_selectors': None,
    
    # Custom fields (optional)
    'custom_fields': [],
    
    # Output
    'output_dir': 'extracted_cases/my_court',
    'csv_filename_template': 'cases_{date}.csv',
}

# Usage example:
"""
from court_configs import PALM_BEACH_CONFIG
from case_data_extractor import CaseDataExtractorApp

config = PALM_BEACH_CONFIG

app = CaseDataExtractorApp(
    output_dir=config['output_dir']
)

# Build URL from template
case_number = "2024CF001234"
url = config['case_url_template'].format(case_number=case_number)

# Process with config settings
await app.process_case_url(
    url=url,
    case_number=case_number,
    wait_selector=config['wait_selector']
)

# For batch processing with rate limiting
await app.process_batch(
    cases,
    wait_selector=config['wait_selector'],
    delay_between_cases=config['rate_limit_seconds']
)
"""

# Finding CSS Selectors Guide:
"""
HOW TO FIND CSS SELECTORS FOR YOUR COURT WEBSITE:

1. Open the court website in Chrome/Firefox
2. Navigate to a case details page
3. Right-click on the case details section → "Inspect" or "Inspect Element"
4. In the developer tools, right-click the HTML element
5. Select "Copy" → "Copy selector"
6. Paste into 'wait_selector' above

Common selector examples:
- By ID: '#caseDetails'
- By class: '.case-info-panel'
- By combination: 'div.case-details table'

Test your selector:
1. Open browser console (F12)
2. Type: document.querySelector('your-selector-here')
3. Should highlight the correct element
"""

# Prompt Customization for Jurisdiction-Specific Fields:
"""
TO ADD CUSTOM FIELDS FOR YOUR JURISDICTION:

1. Add field names to 'custom_fields' list above
2. Modify the extraction prompt in case_data_extractor.py:

In LMStudioVisionClient.extract_case_data(), add your fields:

prompt = f\"\"\"Extract the following fields:
...existing fields...
- vop_date: Violation of probation date if listed
- public_defender_appointed: Date PD was appointed
- discovery_deadline: Discovery deadline date
...rest of prompt...
\"\"\"

3. The model will attempt to extract these fields from the screenshot
"""

# Court-Specific Notes:
COURT_NOTES = {
    'palm_beach': """
    - Case numbers format: YYYY-CF-XXXXXX or YYYY-MM-XXXXXX
    - Website uses JavaScript rendering, wait for .case-details
    - Authentication required - log in manually before running
    - Rate limit: Max 20 requests per minute
    """,
    
    'broward': """
    - Case numbers format: YYCFXXXXXX
    - Slower website - use longer wait times
    - Search page has CAPTCHA - use direct URLs when possible
    - Rate limit: Max 10 requests per minute
    """,
}

# Export configurations dictionary
COURT_CONFIGS = {
    'palm_beach': PALM_BEACH_CONFIG,
    'broward': BROWARD_CONFIG,
    'my_court': MY_COURT_CONFIG,
}

def get_config(court_name: str):
    """
    Get configuration for a specific court
    
    Usage:
        config = get_config('palm_beach')
    """
    return COURT_CONFIGS.get(court_name.lower())

def list_courts():
    """List all configured courts"""
    return list(COURT_CONFIGS.keys())
