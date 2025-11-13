# Case Data Extractor - Vision AI for Court Websites

🔒 **100% Local | 🤖 AI Powered | 📊 Structured Output**

Extract structured case data from court websites using local AI vision models. Built for public defenders and legal professionals.

## ✨ Key Features

- **Complete Privacy**: Everything runs on your machine, no cloud services
- **Vision AI**: Uses LLaVA models to "read" web pages like a human
- **Universal**: Works on any court website layout
- **Easy to Use**: Interactive CLI or Python API
- **Structured Output**: CSV/JSON compatible with your tools
- **Efficient**: Runs on 16GB RAM

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r case_extractor_requirements.txt
playwright install chromium

# 2. Install LM Studio from https://lmstudio.ai/
#    Download "LLaVA 1.6 Mistral 7B" model
#    Load model and start server

# 3. Run the tool
python case_extractor_cli.py
```

## 📖 Usage Examples

**Single Case:**
```python
from case_data_extractor import CaseDataExtractorApp
import asyncio

async def extract():
    app = CaseDataExtractorApp()
    case_data = await app.process_case_url(
        url="https://courtsite.com/case/2024CF001234",
        case_number="2024CF001234"
    )
    app.results.append(case_data)
    app.export_to_csv("my_case.csv")
    await app.cleanup()

asyncio.run(extract())
```

**Batch Processing:**
```python
# Create cases_to_process.csv with case_number,url columns
# Then run:
python case_extractor_cli.py  # Select option 2: Batch mode
```

## 📊 What Gets Extracted

- Case number, client name, next court date
- Charges, attorney, judge, division
- Status, bond amount, dates
- Disposition, plea, sentence details
- And more...

All output is compatible with your morning docket manager.

## 🔒 Privacy & Security

✅ 100% local processing  
✅ No cloud AI services  
✅ No external data transmission  
✅ Works on air-gapped networks  
✅ You control all data  

## 📚 Documentation

- **[CASE_EXTRACTOR_GUIDE.md](CASE_EXTRACTOR_GUIDE.md)** - Complete setup and usage guide
- **[case_data_extractor.py](case_data_extractor.py)** - Core extraction engine
- **[case_extractor_cli.py](case_extractor_cli.py)** - Interactive interface

## 💡 Use Cases

- **Daily Docket Prep**: Extract all morning case details automatically
- **Client Intake**: Quickly gather case info during first meeting  
- **Case Management**: Build and maintain your case database
- **Pattern Analysis**: Extract data across multiple cases

## 🖥️ Requirements

- Python 3.10+
- 16GB RAM (12GB for model, 4GB for system)
- LM Studio (free from lmstudio.ai)
- 10GB disk space for models

## 🎯 How It Works

```
Browser Opens Page → Takes Screenshot → Local AI "Reads" It → 
Extracts Structured Data → Saves to CSV/JSON
```

Why vision AI instead of web scraping? Works on any layout, adapts to changes, minimal maintenance.

## ⚖️ Legal & Ethical Use

✅ Use for cases you represent  
✅ Building your case database  
✅ Automating authorized data entry  

❌ Don't access unauthorized cases  
❌ Don't bypass authentication  
❌ Don't make excessive requests  

**Note**: This tool uses YOUR authenticated browser session. You must log in manually.

## 🔧 Troubleshooting

**Can't connect to LM Studio?**
- Check LM Studio is running
- Verify model is loaded
- Ensure server is started

**Extraction incomplete?**
- Check screenshots in output folder
- Try larger model (13B instead of 7B)
- Increase wait times

See full guide for detailed troubleshooting.

## 📝 Example: Daily Workflow

```bash
# Morning routine:
# 1. Get court docket CSV
# 2. Run extractor in batch mode
python case_extractor_cli.py

# 3. Import CSV to docket manager
# 4. Review and add notes
# 5. Ready for court!
```

## 🤝 Customization

Built to be adapted for your needs:
- Modify extraction fields
- Add court-specific configurations  
- Customize output formats
- Integrate with your tools

## 📜 License

Public domain (Unlicense). Use freely for any purpose.

## 💝 Built For

Public defenders and legal professionals who use technology to better serve their clients.

---

**Ready to start? → [Open CASE_EXTRACTOR_GUIDE.md](CASE_EXTRACTOR_GUIDE.md) for complete setup instructions**
