# Case Data Extractor - Technical Architecture & Design Decisions

## 🎯 Design Philosophy

This tool was designed with three core principles:

1. **Privacy First** - All processing happens locally, no external dependencies
2. **Resilient to Change** - Works on any visual layout without custom scrapers
3. **Accessible to Public Defenders** - Easy to use, easy to customize

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User's Local Machine                      │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Python     │───▶│  Playwright  │───▶│   Browser    │  │
│  │ Application  │    │   Driver     │    │  (Chromium)  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                                         │          │
│         │                                         ▼          │
│         │                                  ┌──────────────┐  │
│         │                                  │  Screenshot  │  │
│         │                                  │    Capture   │  │
│         │                                  └──────────────┘  │
│         │                                         │          │
│         ▼                                         ▼          │
│  ┌──────────────┐                         ┌──────────────┐  │
│  │  LM Studio   │◀────── Base64 ──────────│   Convert    │  │
│  │   Local AI   │                         │   to Base64  │  │
│  │   Server     │                         └──────────────┘  │
│  └──────────────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │   LLaVA      │                                           │
│  │Vision Model  │                                           │
│  │  (Local)     │                                           │
│  └──────────────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐                                           │
│  │ Structured   │                                           │
│  │ JSON Output  │                                           │
│  └──────────────┘                                           │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────────────────────────┐                       │
│  │  CSV/JSON Export                 │                       │
│  │  → Import to Docket Manager      │                       │
│  └──────────────────────────────────┘                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘

         ▲
         │
         │ Authenticated
         │ Session
         │
   ┌─────────────┐
   │   Court     │
   │  Website    │
   └─────────────┘
```

## 🔧 Component Deep Dive

### 1. Playwright (Browser Automation)

**What**: Headless browser automation framework  
**Why Chosen**: 
- Modern, well-maintained
- Excellent for dynamic JavaScript-heavy sites
- Built-in screenshot capabilities
- Cross-platform support
- Better than Selenium for modern web apps

**Alternatives Considered**:
- Selenium: Older, more complex setup
- Requests + BeautifulSoup: Fails on JavaScript sites
- Puppeteer: Node.js only (wanted Python)

**Key Features Used**:
- Page navigation with wait conditions
- Full-page screenshot capture
- Cookie/session preservation
- Viewport control for consistent rendering

### 2. LM Studio (Local AI Server)

**What**: Desktop application for running AI models locally  
**Why Chosen**:
- User-friendly GUI (critical for non-ML experts)
- OpenAI-compatible API (standard interface)
- Easy model management
- Cross-platform
- Free and open source

**Alternatives Considered**:
- Ollama: CLI-only, harder for beginners
- llama.cpp: Requires compilation, complex setup
- Hugging Face Transformers: Requires ML knowledge
- GPT-4 Vision API: Not local, costs money, privacy concerns

**Key Features Used**:
- Model loading and management
- Local HTTP API server
- Vision model support
- Memory management

### 3. LLaVA (Vision Language Model)

**What**: Open-source multimodal AI that can "see" and understand images  
**Why Chosen**:
- Strong visual understanding capabilities
- Good text extraction from images
- Multiple size options (7B, 13B, 34B)
- Fits in consumer hardware (16GB RAM)
- Open source and free

**Alternatives Considered**:
- GPT-4 Vision: Not local, expensive
- Claude 3 with vision: Not local
- OCR (Tesseract): Can't understand context/structure
- Document-specific models: Too narrow

**Model Selection Criteria**:
| Model Size | RAM | Speed | Accuracy | Best For |
|-----------|-----|-------|----------|----------|
| 7B | 8GB | Fast | Good | Daily use |
| 13B | 14GB | Medium | Better | Complex cases |
| 34B | 32GB+ | Slow | Best | Not practical for most users |

**Recommended**: 7B for production, 13B for accuracy-critical tasks

### 4. Data Extraction Strategy

**Approach**: Vision-based extraction with structured prompting

**Prompt Engineering**:
```
1. Clear instructions
2. Specific field definitions
3. Output format specification (JSON)
4. Error handling instructions
5. Context about the source (court system)
```

**Why This Works**:
- Model trained on visual understanding
- Can handle any layout/styling
- Adapts to changes automatically
- Understands legal terminology
- Provides structured output

## 🔄 Data Flow

### Single Case Extraction Flow

```
1. User provides case number + URL
   ↓
2. Playwright launches browser
   ↓
3. Navigate to URL (using user's auth session)
   ↓
4. Wait for page load (networkidle or selector)
   ↓
5. Capture full-page screenshot (PNG)
   ↓
6. Convert screenshot to base64 string
   ↓
7. Construct extraction prompt with context
   ↓
8. Send to LM Studio API:
   - Prompt (text)
   - Screenshot (base64 image)
   ↓
9. LLaVA model processes:
   - Analyzes visual content
   - Extracts text and structure
   - Maps to requested fields
   - Outputs JSON
   ↓
10. Parse JSON response
    ↓
11. Create CaseData object
    ↓
12. Save screenshot to disk (for verification)
    ↓
13. Add to results collection
    ↓
14. Export to CSV/JSON
```

### Batch Processing Flow

```
Load case list from CSV
   ↓
For each case:
   ├─→ Extract (as above)
   ├─→ Rate limit delay (3-5 seconds)
   └─→ Continue to next
   ↓
Aggregate all results
   ↓
Export single CSV/JSON with all cases
```

## 🔒 Security & Privacy Architecture

### Privacy Guarantees

1. **No Network Transmission of Case Data**
   - All processing local
   - No external API calls
   - No telemetry/tracking

2. **Session Isolation**
   - Uses user's manual authentication
   - No credential storage
   - No session hijacking

3. **Data Storage Control**
   - All data in user-specified directory
   - Explicit file permissions
   - User controls retention

### Security Measures

1. **Input Validation**
   - URL validation
   - File path sanitization
   - Case number format checking

2. **Output Sanitization**
   - Prevent path traversal
   - Safe file naming
   - JSON parsing with error handling

3. **Error Handling**
   - Graceful failures
   - No sensitive info in logs
   - Exception catching

## 📊 Performance Considerations

### Speed Bottlenecks

1. **Page Load Time** (1-5 seconds)
   - Depends on court website
   - Network latency
   - JavaScript execution

2. **Screenshot Capture** (0.5-1 seconds)
   - Full page rendering
   - Image encoding

3. **AI Inference** (2-4 seconds with 7B model)
   - Model size dependent
   - CPU vs GPU
   - Image complexity

**Total Per Case**: ~5-10 seconds

### Optimization Strategies

1. **Headless Mode**
   - No GUI rendering overhead
   - Faster for batch processing

2. **Model Selection**
   - 7B model: 2-3 sec inference
   - 13B model: 4-6 sec inference
   - Trade accuracy for speed

3. **Parallel Processing** (Future Enhancement)
   - Multiple browser instances
   - Queue-based extraction
   - Would require careful rate limiting

4. **Caching** (Future Enhancement)
   - Cache screenshots
   - Skip re-extraction of unchanged cases
   - Local database integration

## 🎨 Design Decisions & Rationales

### Why Vision AI Instead of Traditional Web Scraping?

| Traditional Scraping | Vision AI Approach |
|---------------------|-------------------|
| **Fragile**: Breaks on HTML changes | **Resilient**: Works on any visual layout |
| **Site-specific**: Custom code per court | **Universal**: Same code for all sites |
| **Complex**: XPath, CSS selectors, DOM parsing | **Simple**: "Show me the page" |
| **Maintenance**: Constant updates needed | **Maintenance**: Minimal |
| **Dynamic content**: Fails on JavaScript | **Dynamic content**: Handles any rendering |

**Real-world example**: Court website redesign
- Traditional scraper: Breaks completely, requires rewrite
- Vision AI: Continues working, extracts data from new layout

### Why Local AI Instead of Cloud?

**Legal/Ethical Reasons**:
1. **Attorney-client privilege**: Can't send to cloud
2. **Bar rules**: May prohibit external data sharing
3. **Court rules**: Case data sensitivity
4. **Client consent**: Would need explicit permission

**Practical Reasons**:
1. **Cost**: $0 vs potentially $$$ per case
2. **Speed**: No network latency
3. **Reliability**: No internet dependency
4. **Privacy**: Complete control

### Why Playwright Instead of Requests?

Modern court websites use:
- JavaScript rendering
- Dynamic content loading
- Session management
- AJAX calls
- WebSocket connections

**Requests library** can't handle these.  
**Playwright** provides a real browser that handles everything a human would see.

### Why Python?

**Pros**:
- Excellent library ecosystem
- Easy to read/modify
- Good async support
- Cross-platform
- Popular in legal tech

**Cons**:
- Slower than compiled languages
- GIL limitations for true parallelism

**Why still chosen**: Ease of use > raw performance for this use case

## 🧩 Extensibility Points

### 1. Custom Field Extraction

Modify prompt in `LMStudioVisionClient.extract_case_data()`:

```python
prompt = f"""
Extract these additional fields:
- vop_date: Violation of probation date
- preliminary_hearing: Preliminary hearing date
- {jurisdiction_specific_field}: {description}
"""
```

### 2. Multi-Court Support

Use `court_configs.py`:

```python
config = get_config('my_court')
app = CaseDataExtractorApp(output_dir=config['output_dir'])
```

### 3. Custom Output Formats

Extend export methods:

```python
def export_to_xml(self):
    # Your XML formatting logic
    pass

def export_to_database(self, connection):
    # Direct database insertion
    pass
```

### 4. Pre/Post Processing Hooks

```python
class CustomExtractor(CaseDataExtractorApp):
    async def pre_extraction_hook(self, page):
        # Custom page manipulation
        await page.evaluate("/* custom JS */")
    
    async def post_extraction_hook(self, case_data):
        # Validate or enrich data
        return validated_case_data
```

### 5. Alternative Vision Models

Swap out LLaVA for other models:

```python
# In LMStudioVisionClient
model = "bakllava-7b"  # or "llava-1.5-13b"
```

## 📈 Scalability Considerations

### Current Limitations

1. **Single-threaded**: One case at a time
2. **Memory**: Model stays in RAM
3. **Rate limiting**: Manual delay implementation

### Scaling Strategies

**Horizontal Scaling** (Multiple Machines):
```
Machine 1: Cases 1-100
Machine 2: Cases 101-200
Machine 3: Cases 201-300
```

**Vertical Scaling** (Bigger Hardware):
- Larger model (13B → 34B)
- GPU acceleration
- More RAM

**Queue-Based Processing**:
```
Producer: Generates case URLs
Queue: Redis/RabbitMQ
Workers: Multiple extraction instances
Database: Centralized storage
```

## 🔮 Future Enhancements

### Short-term (1-3 months)
- [ ] GPU acceleration support
- [ ] Parallel extraction (multiple browsers)
- [ ] OCR fallback for scanned docs
- [ ] Automated login handlers
- [ ] Better error recovery

### Medium-term (3-6 months)
- [ ] Multi-page case file processing
- [ ] Document attachment extraction
- [ ] Integration with case management systems
- [ ] Web UI for non-technical users
- [ ] Scheduled extraction jobs

### Long-term (6-12 months)
- [ ] Machine learning for accuracy improvement
- [ ] Natural language querying of extracted data
- [ ] Predictive analytics on case outcomes
- [ ] Multi-jurisdiction data normalization
- [ ] Mobile app for on-the-go extraction

## 🧪 Testing Strategy

### Unit Tests (Recommended)

```python
# test_extractor.py
import pytest
from case_data_extractor import LMStudioVisionClient

@pytest.mark.asyncio
async def test_vision_client_connection():
    client = LMStudioVisionClient()
    # Test connection
    
async def test_case_data_validation():
    # Test CaseData object creation
    pass
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_extraction_pipeline():
    app = CaseDataExtractorApp()
    # Test complete workflow
```

### Manual Testing Checklist

- [ ] Single case extraction
- [ ] Batch processing (5 cases)
- [ ] Screenshot quality verification
- [ ] CSV export validation
- [ ] Import to docket manager
- [ ] Error handling (bad URL, timeout)
- [ ] Rate limiting behavior

## 📚 Code Organization

```
case_extractor/
├── core/
│   ├── case_data_extractor.py    # Main engine
│   ├── browser.py                # Playwright wrapper
│   ├── vision_client.py          # LM Studio client
│   └── models.py                 # Data classes
├── cli/
│   └── case_extractor_cli.py     # Interactive interface
├── config/
│   └── court_configs.py          # Court-specific settings
├── utils/
│   ├── validators.py             # Input validation
│   └── exporters.py              # Export formats
├── tests/
│   ├── test_extractor.py
│   └── test_vision.py
└── docs/
    ├── CASE_EXTRACTOR_GUIDE.md
    └── ARCHITECTURE.md
```

## 🎓 Learning Resources

### Understanding the Stack

**Async Python**:
- Why: Court websites can be slow, non-blocking I/O is crucial
- Learn: Python's asyncio, async/await patterns
- Resource: https://docs.python.org/3/library/asyncio.html

**Vision Language Models**:
- What: AI models that understand both text and images
- How: Transformer architecture with visual encoder
- Paper: https://arxiv.org/abs/2304.08485 (LLaVA)

**Browser Automation**:
- Concept: Programmatic control of web browsers
- Why Playwright: Modern, reliable, cross-browser
- Docs: https://playwright.dev/python/

**Prompt Engineering**:
- Art: Crafting instructions for AI models
- Key: Clear, specific, structured prompts
- Guide: https://platform.openai.com/docs/guides/prompt-engineering

## 🏆 Best Practices

### Code Quality
- Type hints for better IDE support
- Docstrings for all public methods
- Async/await for I/O operations
- Error handling with try/except
- Logging for debugging

### Data Quality
- Always verify screenshots
- Manual spot-checks on CSV output
- Compare extracted data to source
- Test on edge cases (unusual formats)

### Operational
- Start with single cases
- Gradually increase batch size
- Monitor extraction accuracy
- Document court-specific quirks
- Version control for configs

### Security
- Regular security audits
- Keep dependencies updated
- Follow least privilege principle
- Encrypt sensitive data at rest
- Regular backups

## 🤝 Contributing Guidelines

### For Public Defenders
- Share court-specific configurations
- Report bugs or issues
- Suggest new features
- Document your workflows

### For Developers
- Follow existing code style
- Add tests for new features
- Update documentation
- Consider privacy implications

### For Researchers
- Analyze extraction accuracy
- Improve prompt engineering
- Benchmark different models
- Publish findings (with appropriate anonymization)

## 📖 Related Work

**Legal Tech**:
- CourtListener: Open legal data
- PACER: Federal court records (official)
- Legal tech APIs: Many commercial options

**Vision AI Applications**:
- Document understanding
- Receipt parsing
- Medical record extraction
- Form filling automation

**Similar Tools** (but not local/private):
- Various commercial legal tech platforms
- Cloud-based court scraping services

**Unique Advantages of This Tool**:
1. 100% local and private
2. No recurring costs
3. Customizable for any court
4. Open source and transparent

---

## 📝 Conclusion

This architecture balances:
- **Privacy** with **Functionality**
- **Simplicity** with **Power**
- **Current needs** with **Future growth**

The vision AI approach provides resilience to website changes while maintaining complete local control over sensitive case data.

**Questions about the architecture?** The code is documented and designed to be readable - dig in and customize as needed!

**Built for public defenders who understand the value of both justice and technology.**
