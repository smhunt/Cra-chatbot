# Quick Tech Stack Comparison Tables

**For CRA Tax Chatbot - 90% Accuracy Goal**

---

## LLM Provider Comparison (1000 queries/day = 30K/month)

| Provider | Model | Input/1M | Output/1M | Monthly Cost | RAG Accuracy | Special Features |
|----------|-------|----------|-----------|--------------|--------------|------------------|
| **Anthropic** ⭐ | Claude 3.5 Sonnet | $3 | $15 | $167 (cached) | Best | Prompt caching, 200K context, won Galileo index |
| OpenAI | GPT-4o | $5 | $20 | $328 | Good | Large ecosystem, function calling |
| OpenAI | GPT-4.1 | $2 | $8 | $193 | Good | Cheaper, newer model |
| Google | Gemini 2.5 Pro | $1.25 | $10 | $115 | Good | Cheapest option, multimodal |

**Winner:** Claude 3.5 Sonnet - Best RAG accuracy, 50% cheaper with prompt caching

---

## Vector Database Comparison (100K documents, 1536 dimensions)

| Database | Free Tier | Monthly Cost | Self-Host | Hybrid Search | Performance |
|----------|-----------|--------------|-----------|---------------|-------------|
| **Qdrant** ⭐ | 1GB cluster | $50-102 | Yes | Yes | Fast |
| Weaviate | None | $153 | Yes | Yes | Fast |
| Pinecone | 2GB, 2M ops | $150-200 | No | Limited | Fastest |
| ChromaDB | Unlimited | $0 (self) | Yes | Limited | Good |

**Winner:** Qdrant - 50% cheaper than competitors, open source, production-ready

---

## Embeddings Model Comparison

| Model | Cost/1M tokens | MTEB Score | Dimensions | Performance vs ada-002 |
|-------|----------------|------------|------------|------------------------|
| **text-embedding-3-large** ⭐ | $0.13 | 64.6% | 1536 (or 256) | +75% accuracy |
| text-embedding-ada-002 | $0.10 | 61.0% | 1536 | Baseline |
| Cohere embed-v3.0 | $0.50 | Good | 1024 | Good, but 5x cost |
| BGE-large (open) | $0* | 63.9% | 1024 | *Requires GPU hosting |

**Winner:** text-embedding-3-large - Best accuracy, minimal cost increase over ada-002

---

## Reranking Model Comparison

| Reranker | Cost/1K queries | Performance | Deployment | Multilingual |
|----------|-----------------|-------------|------------|--------------|
| **Cohere Rerank v3.5** ⭐ | $2.00 | Excellent | API | Yes |
| Pinecone Rerank V0 | Unknown | Best (+60%) | Requires Pinecone | Unknown |
| Mixedbread | Self-host* | NDCG 57.49 | Self-host | Yes |
| bge-reranker | Self-host* | Good | Self-host | Limited |

**Winner:** Cohere Rerank v3.5 - Production-ready, great performance, reasonable cost

---

## Monitoring & Observability Tools

| Tool | Pricing | Open Source | Hallucination Detection | Integrations |
|------|---------|-------------|-------------------------|--------------|
| **Langfuse** ⭐ | $0-59/mo | Yes | Yes | LlamaIndex, OpenAI, Anthropic |
| PromptLayer | $99/mo | No | Limited | Major LLMs |
| Arize AI | $500+/mo | No | Yes | Enterprise features |
| LangSmith | $39/mo | No | Yes | LangChain native |

**Winner:** Langfuse - Open source, best value, excellent features

---

## RAG Framework Comparison

| Framework | Language | Best For | Learning Curve | Community |
|-----------|----------|----------|----------------|-----------|
| **LlamaIndex** ⭐ | Python | RAG applications | Medium | Large |
| LangChain | Python/TS | General LLM apps | Steep | Huge |
| Haystack | Python | Search + RAG | Medium | Medium |
| DSPy | Python | Self-optimizing RAG | Steep | Growing |

**Winner:** LlamaIndex - Best RAG-specific features and abstractions

---

## Complete Stack Comparison

### Recommended Stack (90% Accuracy Target)

```
Monthly Cost: $285
Expected Accuracy: 90-95%

Claude 3.5 Sonnet        →  $167 (with caching)
Qdrant Cloud             →  $50 (with quantization)
text-embedding-3-large   →  $0.10 (after initial indexing)
Cohere Rerank v3.5       →  $60
Langfuse (self-hosted)   →  $0
AWS hosting              →  $55
```

### Budget Stack (<$100/month)

```
Monthly Cost: $70
Expected Accuracy: 80-85%

Gemini 2.5 Pro           →  $50
ChromaDB (self-hosted)   →  $20
text-embedding-3-small   →  $0
No reranking             →  $0
Ragas only               →  $0
```

### Premium Stack (Enterprise)

```
Monthly Cost: $1,500
Expected Accuracy: 95%+

Claude 3.5 Sonnet        →  $200
Pinecone Enterprise      →  $500
Cohere Enterprise        →  $200
Cohere Rerank            →  $100
Arize AI                 →  $500
```

---

## Cost Scaling Projections

| Queries/Day | Queries/Month | LLM Cost | Vector DB | Rerank | Total/Month |
|-------------|---------------|----------|-----------|--------|-------------|
| 1,000 | 30K | $167 | $50 | $60 | $285 |
| 5,000 | 150K | $550 | $150 | $300 | $1,115 |
| 10,000 | 300K | $550 | $300 | $600 | $1,710 |
| 50,000 | 1.5M | $2,750 | $800 | $3,000 | $7,244 |

*Costs with prompt caching and optimizations

---

## Decision Matrix

### Choose Claude 3.5 Sonnet if:
- Accuracy is top priority (tax/legal domain)
- Budget allows $150-200/month for LLM
- Need best RAG performance
- Want prompt caching cost savings

### Choose Gemini 2.5 Pro if:
- Budget very tight (<$100/month)
- Accuracy target is 80-85%
- Willing to sacrifice some accuracy for cost

### Choose Qdrant if:
- Want open source with no lock-in
- Need production performance at lower cost
- Budget is $50-100/month for vector DB
- May self-host in future

### Choose Pinecone if:
- Want fully managed with zero DevOps
- Enterprise budget available
- Need guaranteed SLAs
- Team has no time for infrastructure

### Choose text-embedding-3-large if:
- Want best embedding performance
- Cost difference ($0.03/M tokens) is acceptable
- Need multilingual support
- Targeting 90%+ accuracy

### Choose Langfuse if:
- Want open source monitoring
- Need hallucination detection
- Budget is <$100/month for observability
- May self-host

---

## Key Recommendations Summary

1. **LLM:** Claude 3.5 Sonnet ($167/mo with caching)
   - Reason: Best RAG accuracy, used by Thomson Reuters for tax analysis

2. **Vector DB:** Qdrant Cloud ($50/mo)
   - Reason: 50% cheaper than Pinecone, equally fast, open source

3. **Embeddings:** text-embedding-3-large ($0.10/mo)
   - Reason: 75% better than ada-002, minimal cost increase

4. **Reranker:** Cohere Rerank v3.5 ($60/mo)
   - Reason: 10-15% accuracy boost, production-ready

5. **Framework:** LlamaIndex (free)
   - Reason: Best RAG-specific abstractions

6. **Monitoring:** Langfuse ($0-59/mo)
   - Reason: Open source, hallucination detection, great features

**Total Startup Cost:** $285/month
**Expected Accuracy:** 90-95% with proper implementation

---

## Common Questions

### Q: Why not use open-source LLMs like Llama?
**A:** Self-hosting costs $500-1000/month for GPUs, lower accuracy than Claude, high maintenance. Only viable for privacy-sensitive data or massive scale.

### Q: Can I start with free tiers?
**A:** Yes! Use:
- Qdrant free tier (1GB)
- Langfuse free cloud tier (50k observations)
- Claude with pay-as-you-go (no minimum)
- Total: ~$50-100/month in testing phase

### Q: What's the breakeven for self-hosting embeddings?
**A:** Around 100M tokens/month. At 30k queries × 500 tokens = 15M tokens/month, OpenAI API is far cheaper than GPU hosting.

### Q: Should I use prompt caching?
**A:** Absolutely! With RAG, you're sending the same retrieved documents repeatedly. Prompt caching reduces costs by 50% for repeated content.

### Q: Can I achieve 90% accuracy with this stack?
**A:** Yes, with proper implementation:
- Claude 3.5 Sonnet (best RAG model)
- Hybrid retrieval (dense + sparse)
- Reranking (Cohere)
- Good chunking strategy
- Comprehensive CRA documentation
- Continuous evaluation and iteration

---

**Last Updated:** November 15, 2025
