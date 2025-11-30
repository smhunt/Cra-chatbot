"""
Base Scraper Class for CRA Documentation Collection
Provides common functionality for all scrapers with error handling, rate limiting, and logging
"""

import time
import hashlib
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from loguru import logger
import json

from config.settings import get_settings


class BaseScraperError(Exception):
    """Base exception for scraper errors"""
    pass


class RateLimitError(BaseScraperError):
    """Raised when rate limit is exceeded"""
    pass


class DocumentNotFoundError(BaseScraperError):
    """Raised when document cannot be found"""
    pass


class BaseScraper(ABC):
    """
    Base class for all CRA documentation scrapers

    Features:
    - Rate limiting (respects CRA servers)
    - Automatic retries with exponential backoff
    - Request logging and error tracking
    - Document metadata management
    - Hash-based deduplication
    """

    def __init__(self):
        """Initialize scraper with configuration"""
        self.settings = get_settings()
        self.config = self.settings.data_collection

        # Paths
        self.raw_data_path = Path(self.config.raw_data_path)
        self.raw_data_path.mkdir(parents=True, exist_ok=True)

        # Rate limiting
        self.last_request_time = 0
        self.delay_seconds = self.config.scraper_delay_seconds

        # Session with retry logic
        self.session = self._create_session()

        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_downloads": 0,
            "failed_downloads": 0,
            "bytes_downloaded": 0,
            "documents_saved": 0,
            "duplicates_skipped": 0
        }

        logger.info(f"Initialized {self.__class__.__name__}")

    def _create_session(self) -> requests.Session:
        """Create requests session with headers and timeout"""
        session = requests.Session()
        session.headers.update({
            "User-Agent": self.config.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })
        return session

    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay_seconds:
            sleep_time = self.delay_seconds - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def _make_request(
        self,
        url: str,
        method: str = "GET",
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request with rate limiting and retry logic

        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional arguments for requests

        Returns:
            Response object

        Raises:
            BaseScraperError: If request fails after retries
        """
        self._rate_limit()
        self.stats["total_requests"] += 1

        # Set default timeout
        kwargs.setdefault("timeout", self.config.scraper_timeout_seconds)

        for attempt in range(self.config.scraper_max_retries):
            try:
                logger.debug(f"Request {method} {url} (attempt {attempt + 1})")
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()

                self.stats["bytes_downloaded"] += len(response.content)
                return response

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    retry_after = int(e.response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limited, waiting {retry_after}s")
                    time.sleep(retry_after)
                    continue
                elif e.response.status_code == 404:
                    raise DocumentNotFoundError(f"Document not found: {url}")
                else:
                    logger.error(f"HTTP error {e.response.status_code}: {url}")
                    if attempt < self.config.scraper_max_retries - 1:
                        sleep_time = 2 ** attempt  # Exponential backoff
                        logger.info(f"Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
                        continue
                    raise BaseScraperError(f"Failed after {attempt + 1} attempts: {e}")

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}: {url}")
                if attempt < self.config.scraper_max_retries - 1:
                    sleep_time = 2 ** attempt
                    time.sleep(sleep_time)
                    continue
                raise BaseScraperError(f"Timeout after {attempt + 1} attempts")

            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                if attempt < self.config.scraper_max_retries - 1:
                    sleep_time = 2 ** attempt
                    time.sleep(sleep_time)
                    continue
                raise BaseScraperError(f"Request failed: {e}")

        raise BaseScraperError(f"Failed after {self.config.scraper_max_retries} attempts")

    def _generate_document_id(self, content: str, url: str) -> str:
        """
        Generate unique document ID based on content hash

        Args:
            content: Document content
            url: Source URL

        Returns:
            Document ID (SHA256 hash prefix)
        """
        hash_input = f"{url}:{content}".encode("utf-8")
        return hashlib.sha256(hash_input).hexdigest()[:16]

    def _is_duplicate(self, document_id: str) -> bool:
        """
        Check if document already exists

        Args:
            document_id: Document ID to check

        Returns:
            True if document exists, False otherwise
        """
        # Check if any file in raw_data_path starts with this document_id
        pattern = f"{document_id}_*.json"
        existing_files = list(self.raw_data_path.glob(pattern))
        return len(existing_files) > 0

    def _save_document(
        self,
        document_id: str,
        content: str,
        metadata: Dict[str, Any]
    ) -> Path:
        """
        Save document to disk with metadata

        Args:
            document_id: Unique document identifier
            content: Document content
            metadata: Document metadata

        Returns:
            Path to saved file
        """
        # Check for duplicates
        if self._is_duplicate(document_id):
            logger.debug(f"Skipping duplicate document: {document_id}")
            self.stats["duplicates_skipped"] += 1
            return None

        # Create filename: {doc_id}_{tax_year}_{doc_type}_{topic}.json
        filename_parts = [
            document_id,
            str(metadata.get("tax_year", "unknown")),
            metadata.get("document_type", "unknown"),
            metadata.get("topics", ["unknown"])[0] if metadata.get("topics") else "unknown"
        ]
        filename = "_".join(filename_parts) + ".json"
        filepath = self.raw_data_path / filename

        # Create document structure
        document = {
            "document_id": document_id,
            "source_url": metadata.get("source_url"),
            "title": metadata.get("title"),
            "document_type": metadata.get("document_type"),
            "tax_year": metadata.get("tax_year"),
            "topics": metadata.get("topics", []),
            "date_published": metadata.get("date_published"),
            "date_scraped": datetime.now().isoformat(),
            "content": content,
            "metadata": metadata,
            "content_length": len(content),
            "scraper": self.__class__.__name__
        }

        # Save to disk
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(document, f, indent=2, ensure_ascii=False)

        self.stats["documents_saved"] += 1
        logger.info(f"Saved document: {filename}")

        return filepath

    def _validate_content(self, content: str, min_length: int = 100) -> bool:
        """
        Validate document content

        Args:
            content: Document content to validate
            min_length: Minimum content length

        Returns:
            True if valid, False otherwise
        """
        if not content or len(content.strip()) < min_length:
            logger.warning("Content too short or empty")
            return False

        # Check for common error pages
        error_indicators = [
            "404 not found",
            "page not found",
            "error",
            "access denied",
            "temporarily unavailable"
        ]

        content_lower = content.lower()
        for indicator in error_indicators:
            if indicator in content_lower and len(content) < 1000:
                logger.warning(f"Content appears to be error page: {indicator}")
                return False

        return True

    def get_stats(self) -> Dict[str, Any]:
        """Get scraper statistics"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_downloads"] / self.stats["total_requests"]
                if self.stats["total_requests"] > 0 else 0
            ),
            "mb_downloaded": self.stats["bytes_downloaded"] / (1024 * 1024)
        }

    def print_stats(self):
        """Print scraper statistics"""
        stats = self.get_stats()
        logger.info("=" * 60)
        logger.info(f"Scraper Statistics - {self.__class__.__name__}")
        logger.info("=" * 60)
        logger.info(f"Total Requests:        {stats['total_requests']}")
        logger.info(f"Successful Downloads:  {stats['successful_downloads']}")
        logger.info(f"Failed Downloads:      {stats['failed_downloads']}")
        logger.info(f"Documents Saved:       {stats['documents_saved']}")
        logger.info(f"Duplicates Skipped:    {stats['duplicates_skipped']}")
        logger.info(f"Success Rate:          {stats['success_rate']:.1%}")
        logger.info(f"Data Downloaded:       {stats['mb_downloaded']:.2f} MB")
        logger.info("=" * 60)

    @abstractmethod
    def scrape(self, *args, **kwargs) -> List[Path]:
        """
        Main scraping method - must be implemented by subclasses

        Returns:
            List of paths to saved documents
        """
        raise NotImplementedError("Subclasses must implement scrape()")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close session and print stats"""
        self.session.close()
        self.print_stats()
        return False


if __name__ == "__main__":
    # Test base scraper functionality
    logger.info("BaseScraper test - this is an abstract class")
    logger.info("Use CRAHTMLScraper or CRAPDFScraper for actual scraping")
