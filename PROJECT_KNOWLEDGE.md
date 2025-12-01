# CRA Chatbot - Project Knowledge Base

**AI-Powered Tax Information Assistant for Canada Revenue Agency Documentation**

---

## 📋 Project Overview

### Mission
Build a high-accuracy chatbot trained on official Canada Revenue Agency (CRA) documentation that exceeds the current 17% accuracy baseline of CRA phone service, targeting 70-90%+ accuracy using modern RAG (Retrieval-Augmented Generation) technology.

### Current Status
**Phase 1 - Week 1: ~30% Complete**
- ✅ Project foundation and structure
- ✅ Comprehensive research and planning
- ✅ Configuration system implemented
- ✅ CRA documentation scrapers built
- 🔄 Ready to collect data and build RAG pipeline

### Key Metrics
- **Target Accuracy**: 70% (Phase 1) → 90%+ (Phase 3)
- **Current Baseline**: 17% (CRA phone service)
- **Timeline**: 6-8 weeks to Phase 1 completion
- **Estimated Cost**: $285/month in production
- **Documentation Sources**: 3,500+ CRA documents available

---

## 🏗️ Architecture

### RAG Pipeline
```
User Query
    ↓
Query Preprocessing & Expansion
    ↓
Hybrid Retrieval (Dense + Sparse/BM25)
    ↓
Reranking (Cohere Rerank v3.5)
    ↓
Verification Layer
    ↓
Response Generation (Claude 3.5 Sonnet)
    ↓
Citation & Confidence Scoring
    ↓
Response with Sources
```

### Tech Stack

| Component | Technology | Cost/Month | Justification |
|-----------|-----------|------------|---------------|
| **LLM** | Claude 3.5 Sonnet | $167 (w/ caching) | #1 in Galileo RAG benchmark, Thomson Reuters uses for tax |
| **Vector DB** | Qdrant Cloud | $50 | 50% cheaper than Pinecone, hybrid search built-in |
| **Embeddings** | text-embedding-3-large | $0.10 | 75% better accuracy than ada-002 |
| **Framework** | LlamaIndex 0.9.x | $0 | Best for document-heavy RAG |
| **Reranker** | Cohere Rerank v3.5 | $60 | 10-15% accuracy boost |
| **Monitoring** | Langfuse | $0-59 | Open source, hallucination detection |
| **Language** | Python 3.10+ | $0 | Comprehensive RAG ecosystem |
| **TOTAL** | | **$285/month** | |

### Why This Stack Beats the Baseline

**Modern RAG achieves 90-95% accuracy** through:
1. **Hybrid Retrieval**: Dense (semantic) + Sparse (keyword) = 10-15% accuracy boost
2. **Reranking Layer**: Additional 10-15% boost, reduces hallucinations by 20-30%
3. **Claude 3.5 Sonnet**: Best-in-class RAG performance (Galileo benchmark winner)
4. **Comprehensive CRA Docs**: 3,500+ source documents vs. general-purpose knowledge
5. **Rigorous Validation**: Ground truth dataset, hallucination detection, fact-checking

---

## 📁 Project Structure

```
/Cra-chatbot
├── src/
│   ├── data_collection/          # Web scrapers for CRA documentation
│   │   ├── base_scraper.py       # Base class with rate limiting, retries
│   │   ├── html_scraper.py       # CRA web page scraper
│   │   ├── pdf_scraper.py        # PDF downloader and extractor
│   │   └── cli.py                # Command-line interface
│   ├── processing/                # Document chunking (to be built)
│   ├── rag/                       # RAG pipeline orchestration (to be built)
│   ├── retrieval/                 # Dense, sparse, hybrid retrieval (to be built)
│   ├── reranking/                 # Cohere integration (to be built)
│   ├── generation/                # Claude 3.5 Sonnet integration (to be built)
│   └── evaluation/                # Testing and accuracy measurement (to be built)
├── data/
│   ├── raw/                       # Original CRA documents (JSON format)
│   ├── processed/                 # Chunked documents (to be generated)
│   ├── ground_truth/              # Verified Q&A pairs (to be created)
│   └── sources.json               # 12 prioritized CRA documentation sources
├── config/
│   └── settings.py                # Type-safe Pydantic configuration system
├── scripts/
│   └── setup.sh                   # Automated environment setup
├── tests/                         # Test suite (to be written)
├── docs/                          # Documentation
│
├── Research Documents:
│   ├── RESEARCH_AI_ACCURACY.md           # Common AI failures and solutions (8.4KB)
│   ├── CRA_DOCUMENTATION_SOURCES.md      # 3,500+ CRA sources mapped (33KB)
│   ├── TECH_STACK_RECOMMENDATION.md      # Validated tech choices (23KB)
│   ├── TECH_STACK_COMPARISON.md          # Quick reference tables (7.5KB)
│   └── PHASE1_IMPLEMENTATION_PLAN.md     # 6-8 week roadmap (detailed)
│
├── Configuration:
│   ├── README.md                  # Comprehensive project documentation
│   ├── requirements.txt           # Python dependencies (50+ packages)
│   ├── .env.template              # API key template
│   ├── .gitignore                 # Git exclusions
│   └── .claudeproject             # Claude Project configuration
```

---

## 🎯 Phase 1 Scope

### 8 Core Topics (Week 1-6)

| Topic | Accuracy Target | Rationale |
|-------|----------------|-----------|
| **RRSP Contribution Limits** | 90%+ | Very common, well-documented, quantifiable |
| **TFSA Contribution Limits** | 90%+ | Clear rules, annual updates, high interest |
| **Basic Personal Amount** | 95%+ | Universal to all taxpayers, straightforward |
| **Filing Deadlines** | 100%+ | Simple, binary answers (date-based) |
| **Medical Expense Deductions** | 80%+ | Common query, clear eligibility rules |
| **Charitable Donation Credits** | 85%+ | Well-documented, clear calculations |
| **Moving Expense Deductions** | 80%+ | Specific eligibility criteria |
| **Home Office Expenses** | 80%+ | Post-COVID relevance, specific rules |

### Success Criteria

Must achieve before Phase 2:
- ✅ 70%+ overall accuracy on ground truth dataset
- ✅ <5% hallucination rate
- ✅ 100% citation coverage (every answer has sources)
- ✅ <3 second average response time
- ✅ All 8 core topics meet individual accuracy targets
- ✅ Automated testing pipeline in place

---

## 📊 CRA Documentation Sources

### Tier 1: Core Topics (Priority 1)
**~400 documents | Target: 70% accuracy**

1. **Income Tax Folios** (7 series) - 200 documents
   - URL: https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax/income-tax-folios.html
   - Format: HTML
   - Topics: All major tax topics

2. **Top Tax Questions** - 100 FAQs
   - URL: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/tax-topics.html
   - Format: HTML
   - Topics: Real questions Canadians ask

3. **T1 General Tax Guide** (2024)
   - URL: https://www.canada.ca/en/revenue-agency/services/forms-publications/tax-packages-years/general-income-tax-benefit-package.html
   - Format: PDF
   - Topics: Filing, deductions, credits

4. **RRSP Guide (RC4092)**
   - Format: PDF
   - Topics: RRSP contributions, limits, withdrawals

5. **TFSA Guide (RC4466)**
   - Format: PDF
   - Topics: TFSA contributions, limits

6. **Medical Expenses (RC4065)**
   - Format: PDF
   - Topics: Eligible medical expenses

7. **Moving Expenses (T1-M)**
   - Format: PDF
   - Topics: Moving expense eligibility

8. **Home Office (T777)**
   - Format: PDF
   - Topics: Employee home office expenses

9. **Charitable Donations (P113)**
   - Format: PDF
   - Topics: Charitable donation credits

10. **2024-2025 What's New**
    - URL: https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/whats-new.html
    - Format: HTML
    - Topics: Recent tax changes

### Tier 2: Business/GST (Priority 2)
**~320 documents | Phase 2**

- GST/HST Memoranda Series (~150 docs)
- Business and Self-Employed Guides (~50 docs)

### Tier 3: Comprehensive (Priority 3)
**~1,100+ documents | Phase 3**

- Complete Forms Library (800+ forms)
- Information Circulars (100+)
- Historical Tax Packages (2018-2023)

---

## 🛠️ Key Components Built

### 1. Configuration System (`config/settings.py`)

Type-safe Pydantic configuration with modular settings:

```python
from config.settings import get_settings

settings = get_settings()

# Access configuration
llm_model = settings.llm.llm_model  # "claude-3-5-sonnet-20240620"
vector_db_url = settings.vector_db.qdrant_url
retrieval_top_k = settings.retrieval.retrieval_top_k  # 20
```

**Features**:
- Environment variable management
- Type validation
- Dev/staging/prod modes
- Cost tracking and budget alerts
- Feature flags (enable/disable reranking, caching, etc.)

### 2. Data Collection Scrapers (`src/data_collection/`)

**Base Scraper** (`base_scraper.py`):
- Rate limiting (2s delay between requests)
- Automatic retries with exponential backoff (3 attempts)
- Hash-based deduplication (SHA256)
- Statistics tracking
- Content validation
- Error handling (404s, timeouts, rate limits)

**HTML Scraper** (`html_scraper.py`):
```python
from src.data_collection.html_scraper import CRAHTMLScraper

with CRAHTMLScraper() as scraper:
    result = scraper.scrape_url(
        "https://www.canada.ca/en/...",
        document_type="guide",
        topics=["rrsp"]
    )
```

**PDF Scraper** (`pdf_scraper.py`):
```python
from src.data_collection.pdf_scraper import CRAPDFScraper

with CRAPDFScraper() as scraper:
    result = scraper.scrape_pdf(
        "https://www.canada.ca/content/dam/cra-arc/.../rc4092-24e.pdf",
        document_type="guide",
        topics=["rrsp"],
        tax_year=2024
    )
```

**CLI Interface** (`cli.py`):
```bash
# Scrape Tier 1 sources
python -m src.data_collection.cli scrape-sources --tier 1

# Scrape specific guides
python -m src.data_collection.cli scrape-guides --guides RC4092,RC4466

# View statistics
python -m src.data_collection.cli stats

# View document
python -m src.data_collection.cli view abc123
```

### 3. Document Output Format

Documents saved as JSON in `data/raw/`:

```json
{
  "document_id": "a1b2c3d4e5f6...",
  "source_url": "https://www.canada.ca/...",
  "title": "RC4092 - Registered Retirement Savings Plans",
  "document_type": "guide",
  "tax_year": 2024,
  "topics": ["rrsp"],
  "date_published": "2024-01-15",
  "date_scraped": "2024-11-15T18:30:00",
  "content": "Full extracted text...",
  "content_length": 45789,
  "metadata": {
    "format": "pdf",
    "page_count": 42
  },
  "scraper": "CRAPDFScraper"
}
```

Filename: `{doc_id}_{year}_{type}_{topic}.json`

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- API keys for:
  - Anthropic (Claude 3.5 Sonnet)
  - OpenAI (embeddings)
  - Cohere (reranking)
  - Qdrant Cloud (vector database)

### Installation

```bash
# Clone repository
git clone <repo-url>
cd Cra-chatbot

# Run automated setup
bash scripts/setup.sh

# Or manual setup:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
# Edit .env and add API keys
```

### Usage

**1. Collect CRA Documentation**
```bash
# Test with dry run
python -m src.data_collection.cli scrape-sources --tier 1 --dry-run

# Actually scrape
python -m src.data_collection.cli scrape-sources --tier 1
```

**2. Check Collection Status**
```bash
python -m src.data_collection.cli stats
```

**3. View Collected Documents**
```bash
python -m src.data_collection.cli view {document_id}
```

---

## 📈 Implementation Roadmap

### Week 1 (CURRENT - ~30% Complete)
- [x] Day 1-2: Project setup and configuration ✅
- [x] Day 3-5: Build web scrapers ✅
- [ ] Day 5: Test scrapers on sample documents

**Deliverable**: Development environment ready, scrapers functional

### Week 2
- [ ] Data storage & metadata tagging
- [ ] Scope definition & success metrics
- [ ] Begin Tier 1 data collection

**Deliverable**: Structured dataset with metadata

### Week 3
- [ ] Document chunking implementation
- [ ] Vector database setup (Qdrant)
- [ ] Dense retrieval implementation

**Deliverable**: Basic retrieval working

### Week 4
- [ ] Sparse retrieval (BM25)
- [ ] Hybrid retrieval pipeline
- [ ] Reranking integration
- [ ] Response generation with Claude

**Deliverable**: End-to-end RAG pipeline

### Week 5-6
- [ ] Create ground truth dataset (50-100 Q&A pairs)
- [ ] Implement accuracy measurement framework
- [ ] Hallucination detection
- [ ] Continuous testing setup

**Deliverable**: Validated system with 70%+ accuracy

---

## 🧪 Testing Strategy

### Ground Truth Dataset
- 50-100 verified Q&A pairs (10-15 per topic)
- Mix of straightforward, edge case, and multi-document questions
- Expert validation against CRA documentation

### Accuracy Metrics
1. **Factual Accuracy**: Does answer contain correct facts? (0-100%)
2. **Completeness**: Does answer cover all key points? (0-100%)
3. **Citation Accuracy**: Are citations correct and relevant? (0-100%)
4. **Hallucination Detection**: Any made-up information? (Yes/No)
5. **Confidence Calibration**: Is confidence score appropriate? (0-100%)

### Evaluation Framework
- Ragas framework for automated evaluation
- LLM-as-judge for answer comparison
- Manual expert review (20-30 samples/week)
- Continuous monitoring in production

---

## ⚠️ Common AI Failures (Avoided)

Based on research of real-world chatbot failures:

### What Goes Wrong
1. **Hallucinations** (69-88% in legal/tax queries without RAG)
   - Air Canada lost court case over hallucinated refund policy
   - Microsoft MyCity gave illegal labor advice

2. **Overconfidence Without Verification**
   - Present false information with high confidence
   - Cannot self-assess accuracy

3. **Lack of Grounding**
   - General-purpose LLM knowledge vs. specific CRA rules
   - No source verification

### How We Prevent It
1. **Mandatory RAG**: Never use raw LLM for tax advice
2. **Hybrid Retrieval**: 10-15% accuracy boost over vector-only
3. **Reranking**: Additional 10-15% boost, reduces hallucinations
4. **Citation Required**: Every answer must cite CRA sources
5. **Confidence Thresholds**: Escalate or say "I don't know" if <60%
6. **Hallucination Detection**: Cross-reference against source docs
7. **Ground Truth Validation**: Test against verified Q&A pairs

---

## 💰 Cost Analysis

### Startup Phase (1,000 queries/day)
| Service | Usage | Cost |
|---------|-------|------|
| Claude 3.5 Sonnet | ~30K input + 10K output tokens/query | $167/mo (w/ caching) |
| Qdrant Cloud | 100K documents, 3072 dims | $50/mo |
| text-embedding-3-large | One-time indexing + queries | $0.10/mo |
| Cohere Rerank v3.5 | 1K queries/day × 20 docs | $60/mo |
| Langfuse | Monitoring | $0-59/mo |
| **TOTAL** | | **$285/mo** |

### Scaling (10,000 queries/day)
- Claude: $1,000/mo (or $500 w/ caching)
- Qdrant: $100/mo
- Embeddings: $1/mo
- Reranking: $600/mo
- Monitoring: $59/mo
- **TOTAL**: **$1,710/mo**

### Cost Optimization Strategies
1. **Prompt Caching**: 50% savings on LLM costs
2. **Query Caching**: Cache common questions (Redis)
3. **Vector Quantization**: 30-50% vector DB savings
4. **Dimension Reduction**: Use 256 dims instead of 3072
5. **Self-Hosting**: Consider at 50K+ queries/day

---

## 🔒 Safety & Compliance

### Data Handling
- **Only public CRA documentation** - no private taxpayer data
- **Crown copyright compliance** - reproduction permitted for non-commercial use
- **Rate limiting** - respects CRA servers (2s delay)
- **robots.txt compliance** - follows CRA website rules

### Response Safety
- **Mandatory source citations** - every answer links to CRA docs
- **Confidence thresholds** - escalate low-confidence queries
- **"I don't know" responses** - better than guessing
- **Disclaimers** - "Informational purposes only, not tax advice"
- **Tax year validation** - ensure rules match query year
- **Hallucination detection** - flag unsupported claims

### Limitations
- **Scope**: Phase 1 limited to 8 core topics
- **Not tax advice**: Informational only, users should verify
- **Complex cases**: Escalates to human experts
- **Provincial rules**: Federal only in Phase 1
- **Not a replacement**: Supplement to professional advice

---

## 📚 Research Findings Summary

### AI Accuracy Research
- **Current AI chatbot failures**: 3-27% hallucination rate (higher without RAG)
- **IRS success**: 13M users served with limited-scope chatbot
- **Modern RAG performance**: 85-95% accuracy achievable
- **Key success factors**:
  - Hybrid retrieval (not just vector search)
  - Reranking layer (critical)
  - Source citation (mandatory)
  - Ground truth validation (measure everything)

### CRA Documentation Research
- **Total documents**: 3,500-4,000 available
- **No public API**: Web scraping required
- **Update frequency**: Quarterly for folios, annual for guides
- **Storage requirements**: ~10-15GB initial + 2-3GB/year
- **Tax year changes**: 2024 RRSP limit $32,490, TFSA $7,000

### Tech Stack Research
- **LLM**: Claude 3.5 Sonnet ranks #1 for RAG (Galileo benchmark)
- **Thomson Reuters**: Uses Claude for tax/legal analysis
- **Vector DB**: Qdrant 50% cheaper than Pinecone, same performance
- **Embeddings**: text-embedding-3-large 75% better than ada-002
- **Framework**: LlamaIndex better than LangChain for doc-heavy RAG

---

## 🔄 Next Steps

### Immediate (Week 1 completion)
1. **Test scrapers** on sample CRA documents
2. **Validate extraction quality** (text, tables, metadata)
3. **Begin Tier 1 collection** (10 core guides)

### Short Term (Week 2)
1. **Implement document chunking** (semantic, 512-1024 tokens)
2. **Set up Qdrant** and generate embeddings
3. **Create ground truth dataset** (50 Q&A pairs)

### Medium Term (Weeks 3-4)
1. **Build RAG pipeline** (retrieval → reranking → generation)
2. **Integrate Claude 3.5 Sonnet** with prompt caching
3. **Implement citation system** and confidence scoring

### Long Term (Weeks 5-6)
1. **Run accuracy evaluation** on test dataset
2. **Iterate and optimize** until 70%+ accuracy
3. **Deploy Phase 1** with 8 core topics

---

## 📞 Project Context

### Why This Matters
- **17% baseline accuracy** of CRA phone service is unacceptably low
- **Millions of Canadians** need accurate tax information
- **Financial consequences** of wrong advice (penalties, missed deductions)
- **Opportunity to demonstrate** modern RAG can beat legacy systems

### Success Definition
- **Phase 1**: 70%+ accuracy (4x improvement over baseline)
- **Phase 2**: 85% accuracy (industry standard)
- **Phase 3**: 90%+ accuracy (best-in-class)

### Long-Term Vision
- Expand to all tax topics
- Add provincial tax rules
- Multimodal support (read tax forms, receipts)
- Conversational interface with memory
- Real-time CRA updates
- API for third-party integration

---

## 🔗 Additional Resources

### Research Documents
All research is in the repository:
- `RESEARCH_AI_ACCURACY.md` - Common AI failures and solutions
- `CRA_DOCUMENTATION_SOURCES.md` - Complete source mapping
- `TECH_STACK_RECOMMENDATION.md` - Detailed tech choices
- `TECH_STACK_COMPARISON.md` - Quick reference tables
- `PHASE1_IMPLEMENTATION_PLAN.md` - Full 6-8 week roadmap

### External Links
- [CRA Forms & Publications](https://www.canada.ca/en/revenue-agency/services/forms-publications.html)
- [Income Tax Folios](https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax/income-tax-folios.html)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Ragas Evaluation Framework](https://docs.ragas.io/)

---

## 📊 Quick Stats

- **Language**: Python 3.10+
- **Lines of Code**: ~2,600+ (so far)
- **Files**: 23 files created
- **Dependencies**: 50+ Python packages
- **Documentation**: 70KB+ of research
- **Time Invested**: ~15-21 hours
- **Phase 1 Progress**: ~30% complete
- **Estimated Completion**: 4-5 more weeks

---

## 🎯 Success Metrics Dashboard

Track these in production:

```
Accuracy Metrics:
├── Overall Accuracy: Target 70%+ (Phase 1)
├── Hallucination Rate: Target <5%
├── Citation Coverage: Target 100%
├── Response Time: Target <3s
└── User Satisfaction: Target 4.5+/5

Cost Metrics:
├── Cost per Query: Target <$0.30
├── Monthly Budget: $285 (startup)
└── Cost per User: Target <$5/month

Performance Metrics:
├── Retrieval Precision: Target 80%+
├── Retrieval Recall: Target 90%+
├── Reranking Improvement: Target 15%+
└── Generation Quality: Target 85%+
```

---

**Last Updated**: November 15, 2024
**Phase**: 1 (Week 1)
**Status**: Active Development
**Next Milestone**: Complete Week 1 testing, begin Week 2 data processing
