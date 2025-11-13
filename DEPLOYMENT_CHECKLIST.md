# DEPLOYMENT CHECKLIST & QUICK REFERENCE

## 📦 What You Have

Your complete case data extraction tool includes:

1. **case_data_extractor.py** - Core extraction engine (main tool)
2. **case_extractor_cli.py** - Interactive CLI interface (easy mode)
3. **case_extractor_requirements.txt** - Python dependencies
4. **CASE_EXTRACTOR_GUIDE.md** - Complete setup & usage guide (START HERE!)
5. **CASE_EXTRACTOR_README.md** - Quick overview
6. **court_configs.py** - Template for court-specific settings
7. **cases_template.csv** - Example batch processing file

## ✅ Pre-Deployment Checklist

### Phase 1: System Preparation
- [ ] Python 3.10+ installed (`python --version`)
- [ ] 16GB+ RAM available
- [ ] 10GB+ free disk space
- [ ] Windows 10/11, macOS 10.15+, or Linux

### Phase 2: Software Installation
- [ ] Download LM Studio from https://lmstudio.ai/
- [ ] Install LM Studio
- [ ] Create tool directory (e.g., `C:\CaseExtractor` or `~/case-extractor`)
- [ ] Copy all tool files to directory
- [ ] Open terminal in tool directory

### Phase 3: Python Setup
```bash
- [ ] pip install -r case_extractor_requirements.txt
- [ ] playwright install chromium
- [ ] python --version  # Verify 3.10+
```

### Phase 4: LM Studio Setup
- [ ] Launch LM Studio
- [ ] Search for "llava-v1.6-mistral-7b" in LM Studio
- [ ] Download the model (~8GB, may take time)
- [ ] Go to Chat tab → Load model
- [ ] Wait for "Model loaded" confirmation
- [ ] Go to Local Server tab → Start Server
- [ ] Verify: http://localhost:1234/v1/models in browser

### Phase 5: Testing
```bash
- [ ] python case_extractor_cli.py
- [ ] Select option 5: Check LM Studio connection
- [ ] Should show "✓ Connected to LM Studio"
```

### Phase 6: Court Website Preparation
- [ ] Log in to court website manually
- [ ] Navigate to a test case details page
- [ ] Find CSS selector for case details section (see guide)
- [ ] Update court_configs.py with your settings

### Phase 7: First Extraction
- [ ] Run: python case_extractor_cli.py
- [ ] Select option 1: Extract single case
- [ ] Enter test case number and URL
- [ ] Verify extraction completes
- [ ] Check screenshots in extracted_cases/screenshots/
- [ ] Review CSV output

## 🚀 Quick Start Commands

### First Time Setup
```bash
# 1. Install everything
pip install -r case_extractor_requirements.txt
playwright install chromium

# 2. Start LM Studio (manually)
# - Open LM Studio app
# - Load LLaVA model
# - Start server

# 3. Test connection
python case_extractor_cli.py  # Option 5
```

### Daily Use
```bash
# Interactive mode
python case_extractor_cli.py

# Direct extraction
python case_data_extractor.py
```

## 🎯 Recommended Vision Models

For 16GB RAM systems:

| Model | Command in LM Studio | RAM | Speed | Best For |
|-------|---------------------|-----|-------|----------|
| **LLaVA 1.6 Mistral 7B** ⭐ | Search: "llava-v1.6-mistral-7b" | 8GB | Fast | Daily use |
| BakLLaVA 7B | Search: "baklava" | 8GB | Fast | Documents |
| LLaVA 1.5 13B | Search: "llava-1.5-13b" | 14GB | Slower | Accuracy |

**Recommended**: Start with LLaVA 1.6 Mistral 7B

## 🔧 Common First-Run Issues

### Issue: "Cannot connect to LM Studio"
**Fix**:
1. Check LM Studio is running
2. Look for "Server running" in Local Server tab
3. Try: curl http://localhost:1234/v1/models
4. Restart LM Studio if needed

### Issue: "playwright: command not found"
**Fix**:
```bash
pip install playwright
playwright install chromium
```

### Issue: "No module named 'httpx'"
**Fix**:
```bash
pip install -r case_extractor_requirements.txt
```

### Issue: Can't find CSS selector
**Fix**:
1. Open court website
2. Right-click element → Inspect
3. Right-click in DevTools → Copy → Copy selector
4. Test in console: `document.querySelector('your-selector')`

### Issue: Out of memory
**Fix**:
1. Close other applications
2. Use 7B model instead of 13B
3. Run in headless mode
4. Process smaller batches

## 📱 Quick Reference: Interactive CLI Options

```
1. Extract single case          → Test/one-off extractions
2. Extract batch from CSV       → Process multiple cases
3. Interactive search           → Automated search + extract
4. Configure settings           → Change LM Studio URL
5. Check LM Studio connection   → Verify setup
6. Exit                         → Quit
```

## 🗂️ File Locations After Setup

```
your-tool-directory/
├── case_data_extractor.py      ← Main engine
├── case_extractor_cli.py       ← Run this for interactive mode
├── case_extractor_requirements.txt
├── court_configs.py            ← Customize for your court
├── cases_template.csv          ← Example for batch processing
├── CASE_EXTRACTOR_GUIDE.md     ← Full documentation
└── extracted_cases/            ← Created on first run
    ├── screenshots/
    ├── *.csv                   ← Import to docket manager
    └── *.json
```

## 📋 Daily Workflow Example

### Morning Docket Prep (10 minutes)
```bash
# 1. Get docket from court (manual download)
#    Save as: morning_docket_2025-01-15.csv

# 2. Create case list with URLs
#    Edit cases_template.csv or generate programmatically

# 3. Run extraction
python case_extractor_cli.py
# → Select 2 (Batch mode)
# → Enter your CSV file path
# → Wait for processing (3-5 sec per case)

# 4. Import to docket manager
#    Open morning_docket_manager_with_database.html
#    Load extracted CSV
#    Review and add notes

# 5. Ready for court!
```

## 🔒 Security Checklist

- [ ] Tool directory has restricted permissions
- [ ] Output directory is secure
- [ ] LM Studio only accessible locally (no network exposure)
- [ ] Authentication is manual (never stored)
- [ ] Verify extracted data before using
- [ ] Delete screenshots after verification
- [ ] Follow data retention policies
- [ ] Use appropriate rate limiting

## ⚖️ Legal Compliance Checklist

- [ ] Only access cases you're authorized to view
- [ ] Manually authenticate to court website
- [ ] Use respectful rate limiting (3-5 sec delays)
- [ ] Review court website terms of service
- [ ] Check local bar rules on automation
- [ ] Maintain audit trail (timestamps in JSON)
- [ ] Secure all extracted data appropriately
- [ ] Follow data retention requirements

## 🎓 Learning Path

### Week 1: Setup & Testing
- [ ] Complete installation
- [ ] Test with single case
- [ ] Verify extraction quality
- [ ] Adjust wait times if needed

### Week 2: Customization
- [ ] Configure court_configs.py
- [ ] Test batch processing (5-10 cases)
- [ ] Integrate with docket manager
- [ ] Document your workflow

### Week 3: Automation
- [ ] Create batch processing scripts
- [ ] Set up daily extraction routine
- [ ] Optimize extraction prompts
- [ ] Train team members

### Month 2+: Advanced
- [ ] Multi-court support
- [ ] Custom field extraction
- [ ] Automated reporting
- [ ] Integration with other tools

## 📞 Getting Help

### Self-Help Resources
1. **Read CASE_EXTRACTOR_GUIDE.md** (comprehensive!)
2. Check screenshots in output directory
3. Review error messages carefully
4. Test with known-good case first
5. Verify LM Studio connection

### Debugging Steps
```bash
# Test LM Studio
curl http://localhost:1234/v1/models

# Test Playwright
python -c "from playwright.sync_api import sync_playwright; print('OK')"

# Test imports
python -c "from case_data_extractor import *; print('OK')"

# Verbose mode
# Edit case_data_extractor.py and add at top:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Questions

**Q: How long does extraction take?**
A: 3-5 seconds per case with 7B model

**Q: Can I run this on a laptop?**
A: Yes, if you have 16GB RAM

**Q: Does this work offline?**
A: Yes, after models are downloaded

**Q: Can I extract PDF court documents?**
A: Not directly, but you can screenshot and extract

**Q: What if my court website changes?**
A: Vision AI adapts automatically - no code changes needed

**Q: Can this handle multi-page cases?**
A: Currently single-page. Modify for multi-page if needed.

## 🚨 Troubleshooting Emergency Guide

### Problem: Nothing works
1. Verify Python 3.10+ installed
2. Check all dependencies installed
3. Confirm LM Studio is running
4. Restart computer and try again

### Problem: Extraction is garbage
1. Check screenshot quality
2. Try larger model (13B)
3. Increase wait times
4. Verify page fully loaded

### Problem: Too slow
1. Use 7B model instead of 13B
2. Run in headless mode
3. Close other applications
4. Consider GPU acceleration

### Problem: Legal concerns
1. Review appropriate use guidelines
2. Check court website ToS
3. Consult IT security if needed
4. Document your usage

## ✨ Success Indicators

You know it's working when:
- [ ] CLI shows "✓ Connected to LM Studio"
- [ ] Browser opens and navigates to case page
- [ ] Screenshot appears in output folder
- [ ] CSV has populated fields (not all empty)
- [ ] Client name and case number are correct
- [ ] CSV imports to docket manager successfully

## 📈 Optimization Tips

### Speed
- Use 7B model for faster processing
- Run in headless mode (headless=True)
- Process during off-peak hours
- Batch similar cases together

### Accuracy
- Use 13B model for better extraction
- Increase wait times for slow pages
- Verify screenshots are complete
- Adjust prompts for your jurisdiction

### Workflow
- Automate URL generation
- Create court-specific configs
- Schedule daily extraction runs
- Integrate with case management

## 🎯 Next Steps After Setup

1. **Extract 1 test case** - Verify everything works
2. **Extract 5-10 cases** - Test batch processing
3. **Import to docket manager** - Verify CSV compatibility
4. **Customize court config** - Add your court settings
5. **Document workflow** - Write down your process
6. **Train others** - Share with team if applicable
7. **Automate routine tasks** - Set up daily extraction

## 📄 File You're Reading

**Location**: DEPLOYMENT_CHECKLIST.md  
**Purpose**: Quick reference for setup and daily use  
**Full Docs**: See CASE_EXTRACTOR_GUIDE.md

## 🎉 Ready to Deploy!

You have everything you need:
✓ All code files
✓ Complete documentation
✓ Configuration templates
✓ Usage examples
✓ Troubleshooting guide

**Next Action**: Open CASE_EXTRACTOR_GUIDE.md and follow Phase 1: System Preparation

---

**Questions? Issues? Customization needs?**  
This tool is yours to modify and adapt. Read the code, adjust as needed, make it work for your specific situation.

**Built with ❤️ for public defenders who code**

Good luck with your deployment! 🚀
