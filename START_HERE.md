# 🚀 START HERE - Case Data Extractor

## 👋 Welcome!

You have a **complete, production-ready tool** for extracting case data from court websites using local AI. Everything runs on your machine - 100% private and secure.

## 📂 What's in This Package?

### 🎯 Quick Start Guide
**READ THIS FIRST**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- Step-by-step setup instructions
- Quick reference for daily use
- Troubleshooting guide
- Takes 30 minutes to get running

### 📖 Main Documentation
**For detailed information**: [CASE_EXTRACTOR_GUIDE.md](CASE_EXTRACTOR_GUIDE.md)
- Complete setup & usage guide (300+ lines)
- Real-world examples and workflows
- Legal and ethical considerations
- Advanced customization options

### 💻 Core Application Files

1. **case_data_extractor.py** - The main extraction engine
   - Browser automation
   - Vision AI integration
   - Data export functions
   
2. **case_extractor_cli.py** - Interactive interface
   - Menu-driven interface
   - No coding required
   - Built-in testing tools

3. **case_extractor_requirements.txt** - Python dependencies
   - Install with: `pip install -r case_extractor_requirements.txt`

### ⚙️ Configuration Files

4. **court_configs.py** - Court-specific settings
   - Template for your court
   - Examples included
   - Fully customizable

5. **cases_template.csv** - Batch processing template
   - Shows required format
   - Ready to customize

### 📚 Additional Documentation

6. **CASE_EXTRACTOR_README.md** - Quick overview
7. **ARCHITECTURE.md** - Technical deep dive
8. **PROJECT_SUMMARY.md** - Complete project summary

## 🏃 Quick Start (30 Minutes)

### Step 1: Create Virtual Environment (2 min) - RECOMMENDED
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate      # On Linux/Mac
# OR
venv\Scripts\activate         # On Windows

# You should see (venv) in your terminal prompt
```

**Why use a virtual environment?**
- Isolates project dependencies from system Python
- Prevents conflicts with other Python projects
- Easy to delete and recreate if needed
- Python development best practice

**Note**: You'll need to activate the venv each time you open a new terminal.

### Step 2: Install Python Dependencies (5 min)
```bash
pip install -r case_extractor_requirements.txt
playwright install chromium
```

### Step 3: Setup LM Studio (15 min)
1. Download from **https://lmstudio.ai/**
2. Install and launch
3. Search for "llava-v1.6-mistral-7b"
4. Download model (~8GB)
5. Load model → Start server

### Step 4: Test Run (5 min)
```bash
python case_extractor_cli.py
# Select option 5: Check LM Studio connection
```

### Step 5: First Extraction (5 min)
```bash
python case_extractor_cli.py
# Select option 1: Single case extraction
# Enter a test case number and URL
```

## ✨ What This Tool Does

### Input
- Case number
- URL to case details page
- Or: batch CSV file with multiple cases

### Process
1. Opens browser → Navigates to page
2. Captures screenshot
3. Sends to local AI
4. AI extracts structured data
5. Saves to CSV/JSON

### Output
- **CSV file** - Import directly to your docket manager
- **JSON file** - Full data with metadata
- **Screenshots** - Visual verification

### Extracted Fields
Case number • Client name • Next date • Charges • Attorney • Judge • Division • Status • Bond amount • Arrest date • Filing date • Disposition • Plea • Sentence • Probation info • And more...

## 🎯 Common Use Cases

### Morning Docket Prep
```bash
# Get court's daily docket → Run batch extraction → Import to docket manager
python case_extractor_cli.py  # Option 2: Batch mode
```

### Client Intake
```bash
# Get case number → Extract details → Review for initial assessment
python case_extractor_cli.py  # Option 1: Single case
```

### Weekly Case Review
```bash
# Extract all active cases → Analyze patterns → Export for reporting
# Use programmatic API or batch CSV
```

## 🔒 Privacy & Security

✅ **100% Local** - No cloud services  
✅ **Zero External APIs** - All processing on your machine  
✅ **Attorney-Client Privilege Safe** - No third-party access  
✅ **Air-Gap Compatible** - Works offline after setup  
✅ **Full Control** - You decide what to keep/delete  

## 📋 System Requirements

| Item | Requirement |
|------|-------------|
| RAM | 16GB+ recommended |
| Storage | 10GB+ free space |
| Python | 3.10 or newer |
| OS | Windows 10+, macOS 10.15+, or Linux |

## 🎓 Documentation Guide

**If you're...**

- **Getting started** → Read [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **Need detailed info** → Read [CASE_EXTRACTOR_GUIDE.md](CASE_EXTRACTOR_GUIDE.md)
- **Quick overview** → Read [CASE_EXTRACTOR_README.md](CASE_EXTRACTOR_README.md)
- **Technical person** → Read [ARCHITECTURE.md](ARCHITECTURE.md)
- **Want everything** → Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🛠️ File Quick Reference

```
case_extractor_tool/
├── START_HERE.md                   ← You are here
├── DEPLOYMENT_CHECKLIST.md         ← Setup guide
├── CASE_EXTRACTOR_GUIDE.md         ← Complete documentation
├── ARCHITECTURE.md                 ← Technical details
├── case_data_extractor.py          ← Main engine
├── case_extractor_cli.py           ← Interactive interface
├── court_configs.py                ← Configuration template
├── cases_template.csv              ← Batch processing example
└── case_extractor_requirements.txt ← Dependencies
```

## 💡 Key Features

### Easy to Use
- Interactive CLI (no coding needed)
- Programmatic API (full automation)
- Comprehensive documentation
- 30-minute setup

### Powerful
- Universal court support (any website)
- Vision AI powered
- Batch processing
- Structured output (CSV/JSON)

### Private
- Everything local
- No external services
- No data transmission
- Complete control

### Professional
- Production-ready quality
- Error handling
- Rate limiting
- Audit trails

## 🚨 Important Notes

### Authentication
This tool **does NOT handle login**. You must:
1. Log in to court website manually
2. Keep your browser session active
3. Tool uses your authenticated session

### Rate Limiting
Be respectful to court servers:
- Default: 3-5 seconds between requests
- Configurable per court
- Follow your court's ToS

### Data Verification
Always verify extracted data:
- Check screenshots folder
- Spot-check CSV output
- Compare to original sources

## ⚖️ Legal & Ethical Use

### ✅ Appropriate Use
- Cases you're assigned to represent
- Building your case database
- Automating authorized data entry
- Analyzing your own caseload

### ❌ Inappropriate Use
- Accessing unauthorized cases
- Circumventing authentication
- Excessive automated requests
- Sharing data beyond authorized personnel

## 🎯 Success Checklist

You'll know it's working when:
- [ ] LM Studio shows "✓ Connected"
- [ ] Browser opens and loads page
- [ ] Screenshot saved in output folder
- [ ] CSV has populated fields
- [ ] Data matches original source
- [ ] CSV imports to docket manager

## 📞 Getting Help

### Self-Help Resources
1. Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) troubleshooting section
2. Read [CASE_EXTRACTOR_GUIDE.md](CASE_EXTRACTOR_GUIDE.md) for detailed explanations
3. Review screenshots in output folder
4. Verify LM Studio connection
5. Test with single known-good case

### Common Issues
- **Can't connect to LM Studio** → Check server is started
- **Extraction incomplete** → Check screenshots, try larger model
- **Browser errors** → Run `playwright install chromium`
- **Out of memory** → Use 7B model, close other apps

## 🎉 You're Ready!

### Next Steps:
1. ✅ **Open**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
2. ✅ **Follow**: Phase 1-5 setup instructions
3. ✅ **Test**: Single case extraction
4. ✅ **Customize**: Update court_configs.py
5. ✅ **Deploy**: Integrate into your workflow

### First Extraction in 4 Commands:
```bash
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r case_extractor_requirements.txt
playwright install chromium
python case_extractor_cli.py
```

## 🏆 Built For You

This tool was designed specifically for public defenders who:
- Value privacy and data security
- Need to automate repetitive tasks
- Want to work smarter, not harder
- Care about using technology ethically
- Understand the importance of local tools

**Everything is documented, tested, and ready to use.**

## 📝 Quick Command Reference

```bash
# Setup virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install
pip install -r case_extractor_requirements.txt
playwright install chromium

# Run interactive mode
python case_extractor_cli.py

# Test LM Studio connection
# (In CLI, select option 5)

# Extract single case
# (In CLI, select option 1)

# Extract batch
# (In CLI, select option 2)
```

## 🎓 Learn More

- **LM Studio**: https://lmstudio.ai/
- **Playwright**: https://playwright.dev/python/
- **LLaVA Models**: https://llava-vl.github.io/

## 💝 Philosophy

> "Technology should serve justice, and justice should be accessible to all."

This tool embodies that philosophy:
- Privacy first
- Simple to use
- Powerful enough for real work
- Transparent and open
- Built for public defenders

---

## 🚀 Let's Begin!

**Ready to start?**

Open [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) and follow Phase 1.

You'll have your first case extracted in about 30 minutes.

**Good luck!** 🎉

---

**Built with ❤️ for public defenders who code**

*Questions? Issues? Everything is documented in the guides. Read the docs, modify the code, make it yours.*

---

**IMPORTANT**: This is a local tool. Your data never leaves your machine. Use it responsibly and ethically.
