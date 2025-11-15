"""
Configuration Management for CRA Chatbot
Uses Pydantic Settings for type-safe configuration from environment variables
"""

from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    """LLM Provider Configuration"""

    # Anthropic (Claude)
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    llm_model: str = Field(default="claude-3-5-sonnet-20240620", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.1, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=1024, env="LLM_MAX_TOKENS")

    # OpenAI (Embeddings)
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    embedding_model: str = Field(default="text-embedding-3-large", env="EMBEDDING_MODEL")
    embedding_dimensions: int = Field(default=3072, env="EMBEDDING_DIMENSIONS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class VectorDBSettings(BaseSettings):
    """Qdrant Vector Database Configuration"""

    qdrant_url: Optional[str] = Field(default=None, env="QDRANT_URL")
    qdrant_api_key: Optional[str] = Field(default=None, env="QDRANT_API_KEY")

    # Local Qdrant settings
    qdrant_host: str = Field(default="localhost", env="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, env="QDRANT_PORT")

    # Collection name
    collection_name: str = Field(default="cra_documents", env="QDRANT_COLLECTION_NAME")

    # Vector configuration
    vector_size: int = Field(default=3072, env="EMBEDDING_DIMENSIONS")
    distance_metric: str = Field(default="Cosine", env="QDRANT_DISTANCE_METRIC")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def use_cloud(self) -> bool:
        """Check if using Qdrant Cloud vs local"""
        return self.qdrant_url is not None and self.qdrant_api_key is not None


class RerankingSettings(BaseSettings):
    """Cohere Reranking Configuration"""

    cohere_api_key: str = Field(..., env="COHERE_API_KEY")
    rerank_model: str = Field(default="rerank-english-v3.0", env="COHERE_RERANK_MODEL")
    rerank_top_n: int = Field(default=5, env="RERANK_TOP_N")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RetrievalSettings(BaseSettings):
    """RAG Retrieval Configuration"""

    # Retrieval parameters
    retrieval_top_k: int = Field(default=20, env="RETRIEVAL_TOP_K")
    similarity_threshold: float = Field(default=0.7, env="SIMILARITY_THRESHOLD")
    confidence_threshold: float = Field(default=0.6, env="CONFIDENCE_THRESHOLD")

    # Chunking strategy
    chunk_size: int = Field(default=1024, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=128, env="CHUNK_OVERLAP")

    # Hybrid retrieval weights
    dense_weight: float = Field(default=0.6, env="DENSE_RETRIEVAL_WEIGHT")
    sparse_weight: float = Field(default=0.4, env="SPARSE_RETRIEVAL_WEIGHT")

    # Enable/disable features
    enable_reranking: bool = Field(default=True, env="ENABLE_RERANKING")
    enable_hybrid_search: bool = Field(default=True, env="ENABLE_HYBRID_SEARCH")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class MonitoringSettings(BaseSettings):
    """Langfuse Monitoring Configuration"""

    langfuse_public_key: Optional[str] = Field(default=None, env="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: Optional[str] = Field(default=None, env="LANGFUSE_SECRET_KEY")
    langfuse_host: str = Field(default="https://cloud.langfuse.com", env="LANGFUSE_HOST")

    enable_hallucination_detection: bool = Field(default=True, env="ENABLE_HALLUCINATION_DETECTION")
    track_costs: bool = Field(default=True, env="TRACK_COSTS")
    monthly_budget_alert: float = Field(default=300.0, env="MONTHLY_BUDGET_ALERT")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_enabled(self) -> bool:
        """Check if Langfuse monitoring is enabled"""
        return (self.langfuse_public_key is not None and
                self.langfuse_secret_key is not None)


class DataCollectionSettings(BaseSettings):
    """Web Scraping & Data Collection Configuration"""

    scraper_delay_seconds: float = Field(default=2.0, env="SCRAPER_DELAY_SECONDS")
    scraper_max_retries: int = Field(default=3, env="SCRAPER_MAX_RETRIES")
    scraper_timeout_seconds: int = Field(default=30, env="SCRAPER_TIMEOUT_SECONDS")
    user_agent: str = Field(
        default="Mozilla/5.0 (compatible; CRA-ChatbotResearch/1.0)",
        env="USER_AGENT"
    )

    # Data paths
    raw_data_path: str = Field(default="./data/raw", env="RAW_DATA_PATH")
    processed_data_path: str = Field(default="./data/processed", env="PROCESSED_DATA_PATH")
    ground_truth_path: str = Field(
        default="./data/ground_truth/phase1_qa.json",
        env="GROUND_TRUTH_PATH"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DatabaseSettings(BaseSettings):
    """Database Configuration for Metadata Storage"""

    database_url: str = Field(default="sqlite:///./cra_chatbot.db", env="DATABASE_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class APISettings(BaseSettings):
    """API Server Configuration"""

    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")

    # Rate limiting
    rate_limit_per_minute: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    rate_limit_per_hour: int = Field(default=1000, env="RATE_LIMIT_PER_HOUR")

    # CORS
    cors_allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ALLOWED_ORIGINS"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class CachingSettings(BaseSettings):
    """Caching Configuration"""

    enable_prompt_caching: bool = Field(default=True, env="ENABLE_PROMPT_CACHING")
    enable_query_caching: bool = Field(default=True, env="ENABLE_QUERY_CACHING")

    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    upstash_redis_rest_url: Optional[str] = Field(default=None, env="UPSTASH_REDIS_REST_URL")
    upstash_redis_rest_token: Optional[str] = Field(default=None, env="UPSTASH_REDIS_REST_TOKEN")

    # Cache TTL in seconds
    query_cache_ttl: int = Field(default=3600, env="QUERY_CACHE_TTL")  # 1 hour

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_enabled(self) -> bool:
        """Check if caching is enabled and configured"""
        return (self.enable_query_caching and
                (self.redis_url is not None or self.upstash_redis_rest_url is not None))


class EvaluationSettings(BaseSettings):
    """Testing & Evaluation Configuration"""

    enable_auto_evaluation: bool = Field(default=True, env="ENABLE_AUTO_EVALUATION")
    evaluation_sample_size: int = Field(default=100, env="EVALUATION_SAMPLE_SIZE")

    # Accuracy targets
    phase1_accuracy_target: float = Field(default=0.70, env="PHASE1_ACCURACY_TARGET")
    hallucination_rate_threshold: float = Field(default=0.05, env="HALLUCINATION_RATE_THRESHOLD")
    citation_coverage_target: float = Field(default=1.0, env="CITATION_COVERAGE_TARGET")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    """Main Application Settings"""

    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Component settings
    llm: LLMSettings = Field(default_factory=LLMSettings)
    vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    reranking: RerankingSettings = Field(default_factory=RerankingSettings)
    retrieval: RetrievalSettings = Field(default_factory=RetrievalSettings)
    monitoring: MonitoringSettings = Field(default_factory=MonitoringSettings)
    data_collection: DataCollectionSettings = Field(default_factory=DataCollectionSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    api: APISettings = Field(default_factory=APISettings)
    caching: CachingSettings = Field(default_factory=CachingSettings)
    evaluation: EvaluationSettings = Field(default_factory=EvaluationSettings)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create Settings singleton instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Convenience function for quick access
def settings() -> Settings:
    """Get application settings"""
    return get_settings()


if __name__ == "__main__":
    # Test configuration loading
    try:
        s = get_settings()
        print("✅ Configuration loaded successfully!")
        print(f"Environment: {s.environment}")
        print(f"LLM Model: {s.llm.llm_model}")
        print(f"Embedding Model: {s.llm.embedding_model}")
        print(f"Vector DB: {'Cloud' if s.vector_db.use_cloud else 'Local'}")
        print(f"Monitoring: {'Enabled' if s.monitoring.is_enabled else 'Disabled'}")
        print(f"Caching: {'Enabled' if s.caching.is_enabled else 'Disabled'}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("Make sure to create .env file from .env.template")
