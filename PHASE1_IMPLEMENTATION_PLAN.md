# PHASE 1 IMPLEMENTATION PLAN: CRA CHATBOT FOUNDATION
**Goal**: 70% accuracy on 5-10 core tax topics (beating 17% baseline)

---

## OVERVIEW

This plan breaks down Phase 1 into specific, actionable tasks with time estimates and dependencies. Phase 1 focuses on building a solid foundation with high accuracy on a limited scope before expanding.

**Total Estimated Time**: 130-180 hours (6-8 weeks at 20-25 hours/week)

---

## 1. PROJECT SETUP & INFRASTRUCTURE

### 1.1 Repository Structure Setup
**Time**: 2-3 hours | **Dependencies**: None

**Tasks**:
- [ ] Create project directory structure:
  ```
  /cra-chatbot
    /src
      /data_collection      # Scrapers and data ingestion
      /processing           # Document chunking and preprocessing
      /rag                  # RAG pipeline components
      /retrieval            # Dense + sparse retrieval
      /reranking            # Reranking models
      /generation           # LLM integration
      /evaluation           # Testing and validation
    /data
      /raw                  # Original CRA documents
      /processed            # Chunked and embedded docs
      /ground_truth         # Verified Q&A pairs
    /config                 # Configuration files
    /tests                  # Unit and integration tests
    /docs                   # Project documentation
    /scripts                # Utility scripts
  ```
- [ ] Initialize git repository with .gitignore (exclude data/, .env, api keys)
- [ ] Create README.md with project overview and setup instructions
- [ ] Set up branch protection for main branch

### 1.2 Environment & Dependency Setup
**Time**: 3-4 hours | **Dependencies**: 1.1

**Tasks**:
- [ ] Create Python virtual environment (Python 3.10+)
- [ ] Create requirements.txt with core dependencies:
  ```
  # LLM & RAG Framework
  llama-index>=0.9.0
  openai>=1.0.0
  anthropic>=0.8.0

  # Vector Database
  qdrant-client>=1.7.0
  sentence-transformers>=2.2.0

  # Document Processing
  beautifulsoup4>=4.12.0
  scrapy>=2.11.0
  pdfplumber>=0.10.0
  pypdf2>=3.0.0

  # Retrieval & Reranking
  rank-bm25>=0.2.2
  cohere>=4.37.0

  # Utilities
  python-dotenv>=1.0.0
  pydantic>=2.5.0
  fastapi>=0.108.0
  uvicorn>=0.25.0

  # Testing & Evaluation
  pytest>=7.4.0
  pytest-asyncio>=0.21.0
  ragas>=0.1.0
  ```
- [ ] Create .env.template file for API keys (OpenAI, Anthropic, Cohere, Qdrant)
- [ ] Set up Qdrant Cloud free tier account
- [ ] Verify all dependencies install correctly

### 1.3 Configuration Management
**Time**: 2 hours | **Dependencies**: 1.2

**Tasks**:
- [ ] Create config/settings.py using Pydantic for configuration
- [ ] Define configurations for:
  - LLM settings (model, temperature, max_tokens)
  - Embedding model settings
  - Retrieval parameters (top_k, similarity threshold)
  - Chunking strategy (chunk_size: 512-1024 tokens, overlap: 128 tokens)
  - Reranking settings
  - API endpoints and keys
- [ ] Create separate configs for dev/staging/prod environments
- [ ] Document all configuration options

---

## 2. CRA DOCUMENTATION COLLECTION

### 2.1 Prioritize Initial CRA Sources
**Time**: 4-6 hours | **Dependencies**: None (can run parallel to 1.x)

**Tasks**:
- [ ] Identify and prioritize CRA documentation sources:

  **PRIORITY 1 - Core Tax Topics (Week 1-2)**:
  - [ ] T1 General Tax Guide (current year)
  - [ ] RRSP contribution limits and rules
  - [ ] Basic personal deductions guide
  - [ ] Filing deadlines and requirements
  - [ ] Tax credits (basic non-refundable credits)
  - [ ] TFSA contribution limits and rules

  **PRIORITY 2 - Common Queries (Week 3-4)**:
  - [ ] GST/HST credit information
  - [ ] Canada Child Benefit
  - [ ] Moving expenses
  - [ ] Home office expenses
  - [ ] Medical expense deductions

  **PRIORITY 3 - Supporting Documents**:
  - [ ] CRA FAQs for priority topics
  - [ ] Tax bulletins related to priority topics
  - [ ] Form instructions (T1, Schedule 1, etc.)

- [ ] Document source URLs in /data/sources.json with metadata:
  - URL, document type, tax year, topic category, priority level

### 2.2 Build Web Scrapers
**Time**: 8-12 hours | **Dependencies**: 1.2, 2.1

**Tasks**:
- [ ] Create base scraper class in src/data_collection/base_scraper.py
- [ ] Implement CRA website scraper:
  - [ ] HTML parser using BeautifulSoup
  - [ ] Rate limiting (respect robots.txt, 1-2 second delays)
  - [ ] Error handling and retry logic
  - [ ] Progress tracking and logging
- [ ] Implement PDF downloader and processor:
  - [ ] Download PDFs from CRA website
  - [ ] Extract text using pdfplumber (preserves structure better than PyPDF2)
  - [ ] Handle tables and forms
  - [ ] OCR fallback for image-based PDFs (if needed)
- [ ] Create scraper for CRA news/updates
- [ ] Add data validation (check for corrupted downloads, missing content)
- [ ] Test scrapers on 5-10 sample documents before full run

### 2.3 Data Storage & Organization
**Time**: 4-6 hours | **Dependencies**: 2.2

**Tasks**:
- [ ] Create data schema for raw documents:
  ```python
  {
    "document_id": "unique_id",
    "source_url": "https://...",
    "title": "Document Title",
    "document_type": "guide|faq|bulletin|form",
    "tax_year": 2024,
    "topics": ["rrsp", "deductions"],
    "date_published": "2024-01-15",
    "date_scraped": "2024-11-15",
    "content": "full text...",
    "metadata": {...}
  }
  ```
- [ ] Store raw documents in /data/raw/ with consistent naming:
  - Format: {tax_year}_{document_type}_{topic}_{id}.json
- [ ] Create SQLite database for document metadata and indexing
- [ ] Implement deduplication logic
- [ ] Create backup strategy for scraped data

### 2.4 Metadata Tagging System
**Time**: 6-8 hours | **Dependencies**: 2.3

**Tasks**:
- [ ] Define taxonomy of tax topics:
  ```python
  TOPICS = {
    "rrsp": ["contributions", "limits", "withdrawals", "hbp", "llp"],
    "tfsa": ["contributions", "limits", "withdrawals"],
    "deductions": ["basic_personal", "medical", "charitable", "moving"],
    "credits": ["basic_personal", "age", "disability", "tuition"],
    "filing": ["deadlines", "requirements", "methods", "amendments"],
  }
  ```
- [ ] Create automated tagging using keyword extraction
- [ ] Implement manual tag verification process
- [ ] Tag documents by:
  - Topic/subtopic
  - Taxpayer type (individual, business, non-profit)
  - Province (if province-specific)
  - Complexity level (basic, intermediate, advanced)
  - Tax year
- [ ] Create tag validation tests
- [ ] Generate tag statistics report

---

## 3. INITIAL SCOPE DEFINITION

### 3.1 Select 5-10 Core Topics
**Time**: 3-4 hours | **Dependencies**: 2.1

**Selected Topics (with Rationale)**:

1. **RRSP Contribution Limits**
   - Why: Very common, well-documented, quantifiable answers
   - Success criteria: 90%+ accuracy on limit calculations and carry-forward

2. **TFSA Contribution Limits**
   - Why: Clear rules, annual updates, high user interest
   - Success criteria: 90%+ accuracy on limits and over-contribution penalties

3. **Basic Personal Amount (Tax Credit)**
   - Why: Universal to all taxpayers, straightforward
   - Success criteria: 95%+ accuracy on current year amounts

4. **Filing Deadlines**
   - Why: Simple, binary answers (date-based)
   - Success criteria: 100% accuracy on standard deadlines

5. **Medical Expense Deductions (Basic)**
   - Why: Common query, has clear eligibility rules
   - Success criteria: 80%+ accuracy on eligible expenses

6. **Charitable Donation Credits**
   - Why: Well-documented, clear calculation rules
   - Success criteria: 85%+ accuracy on credit calculations

7. **Moving Expense Deductions**
   - Why: Has specific eligibility criteria to test RAG precision
   - Success criteria: 80%+ accuracy on eligibility and claimable expenses

8. **Home Office Expense (Employee)**
   - Why: Highly relevant post-COVID, specific rules
   - Success criteria: 80%+ accuracy on eligibility and methods

**Tasks**:
- [ ] Document scope decisions in /docs/phase1_scope.md
- [ ] Create topic-specific success criteria
- [ ] Define out-of-scope queries and fallback responses
- [ ] Establish scope expansion criteria (when to add topics)

### 3.2 Create Success Metrics
**Time**: 2-3 hours | **Dependencies**: 3.1

**Tasks**:
- [ ] Define accuracy measurement methodology:
  - Expert review by tax professional or CRA documentation cross-reference
  - Automated fact-checking against source documents
  - User feedback collection
- [ ] Set Phase 1 targets:
  - Overall accuracy: 70%+ (beats 17% baseline)
  - Citation coverage: 100% (every answer has source)
  - Hallucination rate: <5%
  - Average response time: <3 seconds
  - "I don't know" responses: Acceptable for out-of-scope
- [ ] Create measurement tools and dashboards
- [ ] Define weekly accuracy audit process (100 random Q&A samples)

---

## 4. RAG IMPLEMENTATION

### 4.1 Document Chunking Strategy
**Time**: 8-10 hours | **Dependencies**: 2.3, 2.4

**Tasks**:
- [ ] Implement semantic chunking (not fixed-size):
  - Preserve paragraph/section boundaries
  - Keep related content together
  - Target chunk size: 512-1024 tokens
  - Overlap: 128 tokens between chunks
- [ ] Create specialized chunkers for different document types:
  - [ ] Narrative text (guides, explanations)
  - [ ] Lists and bullet points
  - [ ] Tables and forms
  - [ ] Q&A format documents
- [ ] Add metadata to each chunk:
  ```python
  {
    "chunk_id": "unique_id",
    "document_id": "parent_doc_id",
    "content": "chunk text...",
    "chunk_index": 0,
    "topic_tags": ["rrsp", "limits"],
    "tax_year": 2024,
    "source_url": "https://...",
    "document_title": "...",
    "section_heading": "...",
    "prev_chunk_id": null,
    "next_chunk_id": "chunk_id_1"
  }
  ```
- [ ] Test chunking quality on 20+ diverse documents
- [ ] Validate chunks preserve meaning and context
- [ ] Store processed chunks in /data/processed/

### 4.2 Vector Database Setup (Qdrant)
**Time**: 6-8 hours | **Dependencies**: 1.2, 4.1

**Tasks**:
- [ ] Set up Qdrant Cloud collection with schema:
  - Vector size: 3072 (for text-embedding-3-large)
  - Distance metric: Cosine similarity
  - Payload schema for metadata
- [ ] Choose embedding model:
  - Recommended: OpenAI text-embedding-3-large (best accuracy)
  - Alternative: text-embedding-3-small (cheaper)
- [ ] Create embedding pipeline:
  - [ ] Batch processing (100 chunks at a time)
  - [ ] Error handling and retry logic
  - [ ] Progress tracking
  - [ ] Cost monitoring
- [ ] Implement indexing script:
  - [ ] Read processed chunks
  - [ ] Generate embeddings
  - [ ] Upload to Qdrant with metadata
  - [ ] Verify upload success
- [ ] Create test queries to verify retrieval works
- [ ] Set up backup/restore procedures for vector DB

### 4.3 Dense Retrieval Implementation
**Time**: 6-8 hours | **Dependencies**: 4.2

**Tasks**:
- [ ] Create dense retrieval module (src/retrieval/dense_retrieval.py):
  - [ ] Query embedding generation
  - [ ] Vector similarity search in Qdrant
  - [ ] Configurable top_k (start with k=20)
  - [ ] Similarity threshold filtering (e.g., >0.7)
- [ ] Implement query preprocessing:
  - [ ] Normalize whitespace
  - [ ] Expand abbreviations (RRSP → Registered Retirement Savings Plan)
  - [ ] Add tax year context if not specified
- [ ] Add result post-processing:
  - [ ] Deduplication
  - [ ] Metadata enrichment
  - [ ] Score normalization
- [ ] Test retrieval on 50+ sample queries
- [ ] Measure retrieval accuracy (% of relevant docs in top-k)

### 4.4 Sparse Retrieval Implementation (BM25)
**Time**: 6-8 hours | **Dependencies**: 4.1

**Tasks**:
- [ ] Create sparse retrieval module (src/retrieval/sparse_retrieval.py):
  - [ ] Implement BM25 using rank-bm25 library
  - [ ] Index all chunks with tokenization
  - [ ] Support keyword-based search
- [ ] Create custom tokenizer for tax terms:
  - Preserve tax-specific terms (T1, T4, RRSP, TFSA, etc.)
  - Handle dollar amounts and percentages
  - Preserve form numbers and codes
- [ ] Implement exact match boosting for:
  - Tax years (2024, 2023, etc.)
  - Form numbers (T1, T4A, Schedule 1)
  - Specific dollar amounts
  - Dates and deadlines
- [ ] Test on keyword-heavy queries
- [ ] Tune BM25 parameters (k1, b)

### 4.5 Hybrid Retrieval Pipeline
**Time**: 8-10 hours | **Dependencies**: 4.3, 4.4

**Tasks**:
- [ ] Create hybrid retrieval orchestrator (src/retrieval/hybrid_retrieval.py):
  ```python
  def hybrid_retrieve(query, top_k=20):
      # Get results from both retrievers
      dense_results = dense_retrieval(query, top_k=20)
      sparse_results = sparse_retrieval(query, top_k=20)

      # Fusion: Reciprocal Rank Fusion (RRF)
      combined = reciprocal_rank_fusion(dense_results, sparse_results)

      # Return top_k combined results
      return combined[:top_k]
  ```
- [ ] Implement Reciprocal Rank Fusion (RRF):
  - Weight results from both retrievers
  - Handle duplicates
  - Preserve metadata
- [ ] Add adaptive retrieval logic:
  - Detect query type (factual, procedural, calculation)
  - Adjust retrieval strategy based on query type
  - Use dense for conceptual, sparse for exact matches
- [ ] Test hybrid vs individual retrievers
- [ ] Measure improvement in retrieval recall

### 4.6 Reranking Implementation
**Time**: 8-12 hours | **Dependencies**: 4.5

**Tasks**:
- [ ] Choose reranking approach:
  - Recommended: Cohere Rerank v3.5 (best accuracy)
  - Alternative: BGE-Reranker-Large (free, local)
- [ ] Implement reranking module (src/reranking/reranker.py):
  - [ ] Take top-k results from hybrid retrieval
  - [ ] Rerank based on query-document relevance
  - [ ] Return top-n most relevant (n=5-10)
- [ ] Add metadata-based boosting:
  - Boost current tax year documents
  - Boost documents matching user's taxpayer type
  - Boost official guides over FAQs
- [ ] Implement relevance threshold:
  - Filter out low-relevance results (score <0.5)
  - Trigger "insufficient information" if no good matches
- [ ] Test reranking impact on accuracy
- [ ] Measure latency impact

### 4.7 Response Generation with Citations
**Time**: 10-15 hours | **Dependencies**: 4.6

**Tasks**:
- [ ] Choose LLM:
  - Recommended: Claude 3.5 Sonnet (best RAG performance)
  - Alternative: GPT-4 Turbo
- [ ] Create prompt template with strict instructions:
  ```python
  PROMPT_TEMPLATE = """
  You are a CRA tax information assistant. You MUST:
  1. ONLY use information from the provided context
  2. NEVER make up or infer information
  3. Always cite sources with [Source: document title, section]
  4. Say "I don't have enough information" if context is insufficient
  5. Include relevant tax year in your response
  6. Use plain language, not legal jargon

  Context from CRA documentation:
  {context_chunks}

  User question: {query}

  Response (with citations):
  """
  ```
- [ ] Implement generation module (src/generation/generator.py):
  - [ ] Format context from reranked documents
  - [ ] Call LLM with prompt
  - [ ] Parse response
  - [ ] Extract and validate citations
  - [ ] Add confidence score
- [ ] Create response formatting:
  - Main answer (2-3 paragraphs)
  - Citations with links
  - Disclaimers
  - "Last updated" date
- [ ] Implement safety checks:
  - [ ] Verify all claims have citations
  - [ ] Check for hallucination indicators
  - [ ] Validate tax year consistency
- [ ] Add confidence scoring:
  - High (>0.85): Direct match, recent docs
  - Medium (0.6-0.85): Partial match, some uncertainty
  - Low (<0.6): Trigger "I don't know" or human escalation
- [ ] Test with 100+ diverse queries

### 4.8 End-to-End RAG Pipeline
**Time**: 6-8 hours | **Dependencies**: 4.1-4.7

**Tasks**:
- [ ] Create main RAG orchestrator (src/rag/pipeline.py):
  ```python
  def answer_query(query: str) -> dict:
      # 1. Query preprocessing
      processed_query = preprocess(query)

      # 2. Hybrid retrieval
      candidates = hybrid_retrieve(processed_query, top_k=20)

      # 3. Reranking
      top_docs = rerank(processed_query, candidates, top_n=5)

      # 4. Check confidence threshold
      if max_score(top_docs) < 0.5:
          return {"answer": "I don't have enough information...",
                  "confidence": "low"}

      # 5. Generate response
      response = generate_with_citations(processed_query, top_docs)

      # 6. Verify response quality
      verified_response = verify_response(response, top_docs)

      return verified_response
  ```
- [ ] Add logging and monitoring:
  - [ ] Log all queries and responses
  - [ ] Track retrieval performance
  - [ ] Monitor generation latency
  - [ ] Record confidence scores
- [ ] Implement caching for common queries
- [ ] Add rate limiting and error handling
- [ ] Create API endpoint (FastAPI)
- [ ] Test full pipeline with 50+ queries

---

## 5. TESTING & VALIDATION

### 5.1 Create Ground Truth Dataset
**Time**: 15-20 hours | **Dependencies**: 3.1

**Tasks**:
- [ ] Compile 50-100 verified Q&A pairs for initial scope (10-15 per topic):

  **For each topic**:
  - [ ] Write 5-7 common/straightforward questions
  - [ ] Write 3-5 edge case questions
  - [ ] Write 2-3 questions requiring multi-document synthesis

  **Example for RRSP**:
  - "What is the RRSP contribution limit for 2024?" (straightforward)
  - "I have unused RRSP room from 2022. Can I still use it?" (carry-forward)
  - "What happens if I over-contribute to my RRSP?" (edge case)
  - "Can I contribute to RRSP after age 71?" (age limit edge case)

- [ ] For each Q&A pair, document:
  ```python
  {
    "question": "...",
    "answer": "verified answer from CRA",
    "source_urls": ["https://..."],
    "source_documents": ["doc_id_1", "doc_id_2"],
    "topic": "rrsp",
    "complexity": "basic|intermediate|advanced",
    "tax_year": 2024,
    "key_facts": ["$31,560 limit for 2024", "18% of previous year income"],
    "common_mistakes": ["confusing with TFSA", "not accounting for carry-forward"]
  }
  ```
- [ ] Manually verify each answer against CRA documentation
- [ ] Have second reviewer validate answers
- [ ] Store in /data/ground_truth/phase1_qa.json
- [ ] Create separate test sets:
  - Development set (70%): For tuning and experimentation
  - Test set (30%): For final evaluation

### 5.2 Accuracy Measurement Framework
**Time**: 10-12 hours | **Dependencies**: 4.8, 5.1

**Tasks**:
- [ ] Create evaluation module (src/evaluation/accuracy.py):
  - [ ] Load ground truth dataset
  - [ ] Run RAG pipeline on all test questions
  - [ ] Compare generated vs expected answers
- [ ] Implement accuracy metrics:
  - [ ] **Factual Accuracy**: Does answer contain correct facts? (0-100%)
  - [ ] **Completeness**: Does answer cover all key points? (0-100%)
  - [ ] **Citation Accuracy**: Are citations correct and relevant? (0-100%)
  - [ ] **Hallucination Detection**: Any made-up information? (Yes/No)
  - [ ] **Confidence Calibration**: Is confidence score appropriate? (0-100%)
- [ ] Create automated evaluation using Ragas framework:
  - Answer relevancy
  - Faithfulness (to source docs)
  - Context precision
  - Context recall
- [ ] Manual evaluation process:
  - Random sample of 20-30 answers per week
  - Expert review by tax professional or CRA doc comparison
  - Flag errors for analysis
- [ ] Generate evaluation reports:
  - Overall accuracy by topic
  - Common failure patterns
  - Confidence score distribution
  - Retrieval success rate
  - Generation quality scores
- [ ] Create visualization dashboard

### 5.3 Hallucination Detection
**Time**: 6-8 hours | **Dependencies**: 5.2

**Tasks**:
- [ ] Implement hallucination detection:
  - [ ] Cross-reference generated facts with source documents
  - [ ] Flag unsupported claims
  - [ ] Detect contradictions with source material
- [ ] Use automated hallucination detection:
  - Check each sentence against retrieved context
  - Score: 0 (hallucinated) to 1 (grounded)
  - Threshold: Flag if score <0.7
- [ ] Create hallucination report:
  - List all potential hallucinations
  - Source the claim vs actual documentation
  - Categorize by severity (minor vs major)
- [ ] Add to monitoring dashboard

### 5.4 Continuous Testing & Expansion Criteria
**Time**: 4-6 hours | **Dependencies**: 5.2, 5.3

**Tasks**:
- [ ] Create automated test suite:
  - [ ] Unit tests for each component
  - [ ] Integration tests for pipeline
  - [ ] Regression tests for ground truth dataset
  - [ ] Run tests on every code change
- [ ] Define scope expansion criteria:
  ```
  Expand to new topics when:
  - Current topics achieve >70% accuracy for 2 consecutive weeks
  - Hallucination rate <5%
  - Citation coverage >95%
  - User feedback positive (if in beta)
  ```
- [ ] Create topic prioritization for Phase 2:
  - Rank by user demand
  - Rank by documentation availability
  - Rank by expected accuracy
- [ ] Set up weekly accuracy review meeting
- [ ] Document lessons learned and improvements

---

## TIMELINE & MILESTONES

### Week 1: Setup & Initial Collection
**Days 1-2**: Project setup (1.1-1.3) - 7-9 hours
**Days 3-5**: Source prioritization & scraper development (2.1-2.2) - 12-18 hours
**Deliverable**: Development environment ready, first documents scraped

### Week 2: Data Processing
**Days 1-3**: Data storage & metadata tagging (2.3-2.4) - 10-14 hours
**Days 4-5**: Scope definition & success metrics (3.1-3.2) - 5-7 hours
**Deliverable**: Structured dataset, defined scope

### Week 3: RAG Foundation
**Days 1-2**: Document chunking (4.1) - 8-10 hours
**Days 3-4**: Vector DB setup & dense retrieval (4.2-4.3) - 12-16 hours
**Day 5**: Sparse retrieval (4.4) - 6-8 hours
**Deliverable**: Basic retrieval working

### Week 4: RAG Advanced
**Days 1-2**: Hybrid retrieval & reranking (4.5-4.6) - 16-22 hours
**Days 3-5**: Response generation & pipeline integration (4.7-4.8) - 16-23 hours
**Deliverable**: End-to-end RAG pipeline

### Week 5-6: Testing & Validation
**Days 1-4**: Ground truth dataset creation (5.1) - 15-20 hours
**Days 5-7**: Accuracy measurement framework (5.2) - 10-12 hours
**Days 8-10**: Hallucination detection & continuous testing (5.3-5.4) - 10-14 hours
**Deliverable**: Validated system with accuracy metrics

**Total**: 130-180 hours (6-8 weeks at 20-25 hours/week)

---

## DEPENDENCIES DIAGRAM

```
1. Project Setup (1.1-1.3) → All development tasks
2. Documentation Collection (2.1) → 2.2, 3.1
3. Scrapers (2.2) → 2.3
4. Data Storage (2.3) → 2.4, 4.1
5. Metadata Tagging (2.4) → 4.1
6. Scope Definition (3.1) → 3.2, 5.1
7. Document Chunking (4.1) → 4.2, 4.4
8. Vector DB Setup (4.2) → 4.3
9. Dense Retrieval (4.3) → 4.5
10. Sparse Retrieval (4.4) → 4.5
11. Hybrid Retrieval (4.5) → 4.6
12. Reranking (4.6) → 4.7
13. Generation (4.7) → 4.8
14. Full Pipeline (4.8) → 5.2
15. Ground Truth (5.1) → 5.2
16. Accuracy Measurement (5.2) → 5.3, 5.4
```

---

## CRITICAL SUCCESS FACTORS

1. **Don't Skip Testing**: Allocate 30% of time to testing and validation
2. **Start Small**: Resist urge to expand scope before hitting accuracy targets
3. **Ground Truth is King**: Invest heavily in creating verified Q&A dataset
4. **Monitor Continuously**: Track accuracy from day 1, not just at the end
5. **Iterate Quickly**: Test each component independently before integration
6. **Document Everything**: Record decisions, experiments, and results
7. **Real CRA Docs Only**: Never supplement with generic tax information

---

## RISK MITIGATION

| Risk | Mitigation Strategy |
|------|---------------------|
| Scraping fails/blocked | Add rate limiting, use multiple approaches, manual download backup |
| Low initial accuracy | Start with even smaller scope, improve retrieval before generation |
| Hallucinations persist | Increase reranking threshold, add verification layer, use stricter prompts |
| Slow performance | Implement caching, optimize embeddings, use smaller model for dev |
| Scope creep | Strict adherence to 5-10 topics, formal expansion criteria |
| Insufficient documentation | Flag topics as "needs more research", don't guess |
| API costs too high | Use prompt caching, implement query caching, consider local models |
| Vector DB limits | Start with Qdrant free tier (1GB), optimize embeddings, monitor usage |

---

## PHASE 1 SUCCESS CRITERIA

**Must achieve before moving to Phase 2**:
- [ ] 70%+ overall accuracy on ground truth dataset
- [ ] <5% hallucination rate
- [ ] 100% citation coverage (every answer has sources)
- [ ] <3 second average response time
- [ ] All 8 core topics covered with individual accuracy targets met
- [ ] Automated testing pipeline in place
- [ ] Weekly accuracy monitoring established

---

## NEXT STEPS AFTER PHASE 1

Once Phase 1 achieves success criteria:
1. **Phase 2**: Expand to 10-15 additional topics
2. **Phase 3**: Add province-specific rules
3. **Phase 4**: Implement user interface and conversation history
4. Beta testing with real users
5. Continuous monitoring and improvement

---

## RECOMMENDED TECH STACK

Based on research in TECH_STACK_RECOMMENDATION.md:

- **Framework**: LlamaIndex 0.9.x
- **LLM**: Claude 3.5 Sonnet (with prompt caching)
- **Vector DB**: Qdrant Cloud (free tier → paid)
- **Embeddings**: OpenAI text-embedding-3-large
- **Reranker**: Cohere Rerank v3.5
- **Monitoring**: Langfuse (open source)
- **Python**: 3.10+

**Estimated Monthly Cost (Production)**: $285
- Claude 3.5 Sonnet: $167 (with caching)
- Qdrant Cloud: $50
- Embeddings: $0.10
- Cohere Rerank: $60
- Langfuse: $0-59

---

## ADDITIONAL RESOURCES

- **CRA Documentation Sources**: See CRA_DOCUMENTATION_SOURCES.md
- **Tech Stack Details**: See TECH_STACK_RECOMMENDATION.md and TECH_STACK_COMPARISON.md
- **Common AI Failures**: See RESEARCH_AI_ACCURACY.md
