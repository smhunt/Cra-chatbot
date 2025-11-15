# CRA Chatbot - AI-Powered Tax Information Assistant

A high-accuracy chatbot trained on official Canada Revenue Agency (CRA) documentation, designed to exceed the 17% accuracy baseline of current phone service.

## 🎯 Project Goals

- **Beat 17% baseline**: Achieve 70%+ accuracy in Phase 1, scaling to 90%+ in production
- **Grounded responses**: Every answer backed by official CRA documentation with citations
- **Zero hallucinations**: <5% hallucination rate through rigorous verification
- **Fast responses**: <3 second average response time
- **Comprehensive coverage**: 3,500+ CRA documents indexed

## 🏗️ Architecture

**RAG Pipeline (Retrieval-Augmented Generation)**:
```
User Query
    ↓
Query Preprocessing
    ↓
Hybrid Retrieval (Dense + Sparse)
    ↓
Reranking (Cohere Rerank v3.5)
    ↓
Verification Layer
    ↓
Response Generation (Claude 3.5 Sonnet)
    ↓
Citation & Confidence Scoring
```

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **LLM** | Claude 3.5 Sonnet | #1 in Galileo RAG benchmark, used by Thomson Reuters for tax analysis |
| **Vector DB** | Qdrant Cloud | 50% cheaper than Pinecone, hybrid search built-in |
| **Embeddings** | OpenAI text-embedding-3-large | 75% better accuracy than ada-002 |
| **Framework** | LlamaIndex 0.9.x | Best-in-class for document-heavy RAG |
| **Reranker** | Cohere Rerank v3.5 | 10-15% accuracy boost |
| **Monitoring** | Langfuse | Open source, hallucination detection |
| **Language** | Python 3.10+ | Comprehensive RAG ecosystem |

**Estimated Cost**: $285/month (startup phase)

## 📊 Phase 1 Scope (Current)

**8 Core Topics** with accuracy targets:
1. RRSP Contribution Limits (90%+)
2. TFSA Contribution Limits (90%+)
3. Basic Personal Amount (95%+)
4. Filing Deadlines (100%+)
5. Medical Expense Deductions (80%+)
6. Charitable Donation Credits (85%+)
7. Moving Expense Deductions (80%+)
8. Home Office Expenses (80%+)

**Timeline**: 6-8 weeks (130-180 hours)

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- API keys for:
  - OpenAI (embeddings)
  - Anthropic (Claude 3.5 Sonnet)
  - Cohere (reranking)
  - Qdrant Cloud (vector database)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Cra-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.template .env
# Edit .env and add your API keys
```

### Configuration

Edit `config/settings.py` to customize:
- LLM parameters (temperature, max_tokens)
- Retrieval settings (top_k, similarity threshold)
- Chunking strategy (chunk_size, overlap)
- Reranking parameters

### Running the Chatbot

```bash
# Start the API server
uvicorn src.rag.api:app --reload

# Or use the CLI
python -m src.rag.cli
```

## 📁 Project Structure

```
/Cra-chatbot
├── src/
│   ├── data_collection/    # Web scrapers for CRA documentation
│   ├── processing/          # Document chunking and preprocessing
│   ├── rag/                 # Main RAG pipeline orchestration
│   ├── retrieval/           # Dense, sparse, and hybrid retrieval
│   ├── reranking/           # Document reranking logic
│   ├── generation/          # LLM response generation
│   └── evaluation/          # Testing and accuracy measurement
├── data/
│   ├── raw/                 # Original CRA documents
│   ├── processed/           # Chunked and embedded documents
│   └── ground_truth/        # Verified Q&A pairs for testing
├── config/                  # Configuration files
├── tests/                   # Unit and integration tests
├── docs/                    # Project documentation
└── scripts/                 # Utility scripts

Research Documents:
├── RESEARCH_AI_ACCURACY.md           # Common AI failures and solutions
├── CRA_DOCUMENTATION_SOURCES.md      # 3,500+ CRA document sources
├── TECH_STACK_RECOMMENDATION.md      # Validated tech stack choices
├── TECH_STACK_COMPARISON.md          # Quick reference comparisons
└── PHASE1_IMPLEMENTATION_PLAN.md     # Detailed implementation roadmap
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run evaluation on ground truth dataset
python -m src.evaluation.accuracy
```

## 📈 Success Metrics

**Phase 1 Targets** (must achieve before Phase 2):
- ✅ 70%+ overall accuracy on ground truth dataset
- ✅ <5% hallucination rate
- ✅ 100% citation coverage (every answer has sources)
- ✅ <3 second average response time
- ✅ All 8 core topics meet individual accuracy targets

**Measurement Methods**:
- Expert evaluation by tax professionals
- Automated fact-checking against CRA sources
- Ragas framework metrics (faithfulness, answer relevancy)
- User feedback collection

## 🔍 Key Features

### 1. Hybrid Retrieval
Combines dense (semantic) and sparse (keyword) search for 10-15% accuracy improvement:
- Dense: Understands "retirement savings" = RRSP
- Sparse: Exact matches for form numbers, tax years, dollar amounts

### 2. Reranking Layer
Re-orders retrieved documents before generation:
- Reduces hallucinations by 20-30%
- Surfaces most relevant context
- Metadata boosting (current tax year, document type)

### 3. Source Citations
Every response includes:
- Specific CRA document reference
- Publication date
- Direct link to source
- Confidence score

### 4. Safety Features
- Hallucination detection (cross-reference with source docs)
- Confidence thresholds (escalate low-confidence queries)
- "I don't know" responses (vs. guessing)
- Tax year validation

## 📚 Documentation

- **Research**: See `/docs` for detailed research findings
- **Implementation Plan**: `PHASE1_IMPLEMENTATION_PLAN.md`
- **CRA Sources**: `CRA_DOCUMENTATION_SOURCES.md`
- **Tech Stack**: `TECH_STACK_RECOMMENDATION.md`

## 🛣️ Roadmap

**Phase 1** (6-8 weeks): ✅ In Progress
- Foundation with 8 core topics
- 70%+ accuracy target

**Phase 2** (4-6 weeks): Planned
- Expand to 15-20 additional topics
- 85%+ accuracy target

**Phase 3** (4-6 weeks): Planned
- Province-specific rules
- Advanced filtering
- 90%+ accuracy target

**Phase 4**: Planned
- User interface
- Conversation history
- Multimodal support (read tax forms, receipts)

## ⚠️ Important Notes

### Data Sources
- **Only official CRA documentation**: No third-party tax advice
- **Regular updates**: Quarterly CRA documentation refresh
- **Tax year awareness**: Defaults to current year, validates against sources

### Limitations
- **Scope**: Currently limited to 8 core topics in Phase 1
- **Not tax advice**: Informational purposes only, users should verify
- **Complex cases**: Escalates to human experts when confidence is low
- **Provincial variations**: Federal rules only in Phase 1

## 🤝 Contributing

See `PHASE1_IMPLEMENTATION_PLAN.md` for detailed development tasks and timeline.

## 📄 License

[To be determined]

## 🙏 Acknowledgments

- CRA for providing comprehensive public documentation
- Research based on 2024 RAG best practices (Galileo benchmark, academic papers)
- Inspired by successful implementations: IRS chatbots, Thomson Reuters legal AI

---

**Current Status**: Phase 1 - Week 1 (Project Setup)
**Last Updated**: November 15, 2024
