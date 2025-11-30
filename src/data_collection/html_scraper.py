"""
HTML Scraper for CRA Web Pages
Extracts content from CRA website HTML pages
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from loguru import logger
import re
from datetime import datetime

from src.data_collection.base_scraper import BaseScraper, BaseScraperError


class CRAHTMLScraper(BaseScraper):
    """
    Scraper for CRA HTML documentation pages

    Handles:
    - Income Tax Folios
    - FAQs and top tax questions
    - Web-based guides and bulletins
    - What's New pages
    """

    def __init__(self):
        """Initialize HTML scraper"""
        super().__init__()
        logger.info("CRAHTMLScraper initialized")

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content from CRA page, removing navigation and footers

        Args:
            soup: BeautifulSoup object

        Returns:
            Cleaned text content
        """
        # CRA pages typically use specific content containers
        # Try multiple selectors in order of preference
        content_selectors = [
            {"id": "wb-main"},  # Main content area
            {"class": "container"},
            {"role": "main"},
            {"id": "content"},
            {"class": "mwsbodytext"}  # Older CRA pages
        ]

        main_content = None
        for selector in content_selectors:
            main_content = soup.find("main", **selector) or soup.find("div", **selector)
            if main_content:
                break

        if not main_content:
            # Fallback: use body if no main content found
            main_content = soup.find("body")
            logger.warning("Could not find main content container, using body")

        if not main_content:
            raise BaseScraperError("No content found in page")

        # Remove unwanted elements
        unwanted_tags = ["nav", "header", "footer", "script", "style", "aside"]
        for tag_name in unwanted_tags:
            for tag in main_content.find_all(tag_name):
                tag.decompose()

        # Remove elements with specific classes/ids
        unwanted_selectors = [
            {"class": "wb-share"},  # Share buttons
            {"class": "pagedetails"},  # Page details
            {"id": "wb-info"},  # Info section
            {"class": "breadcrumb"},  # Breadcrumbs
            {"class": "wb-slc"}  # Language selector
        ]
        for selector in unwanted_selectors:
            for element in main_content.find_all(**selector):
                element.decompose()

        # Get text with preserved structure
        text = main_content.get_text(separator="\n", strip=True)

        # Clean up excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Max 2 newlines
        text = re.sub(r' +', ' ', text)  # Collapse spaces

        return text.strip()

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract metadata from CRA HTML page

        Args:
            soup: BeautifulSoup object
            url: Page URL

        Returns:
            Metadata dictionary
        """
        metadata = {
            "source_url": url,
            "format": "html"
        }

        # Extract title
        title_tag = soup.find("h1") or soup.find("title")
        if title_tag:
            metadata["title"] = title_tag.get_text(strip=True)

        # Extract date modified/published
        date_patterns = [
            {"id": "wb-dtmd"},  # Web Experience Toolkit date modified
            {"class": "dateModified"},
            {"property": "dateModified"}
        ]

        for pattern in date_patterns:
            date_element = soup.find(attrs=pattern)
            if date_element:
                date_text = date_element.get_text(strip=True)
                metadata["date_published"] = date_text
                break

        # Try to extract tax year from title or URL
        tax_year_match = re.search(r'20\d{2}', metadata.get("title", "") + " " + url)
        if tax_year_match:
            metadata["tax_year"] = int(tax_year_match.group())
        else:
            # Default to current year if not found
            metadata["tax_year"] = datetime.now().year

        # Extract language
        html_tag = soup.find("html")
        if html_tag and html_tag.get("lang"):
            metadata["language"] = html_tag.get("lang")

        return metadata

    def _detect_topics(self, title: str, content: str, url: str) -> List[str]:
        """
        Automatically detect topics based on content

        Args:
            title: Page title
            content: Page content
            url: Page URL

        Returns:
            List of detected topics
        """
        topics = []

        # Topic keywords mapping
        topic_keywords = {
            "rrsp": ["rrsp", "registered retirement savings plan", "retirement savings"],
            "tfsa": ["tfsa", "tax-free savings account"],
            "medical": ["medical expense", "medical deduction"],
            "charitable": ["charitable donation", "charitable gift", "donation receipt"],
            "moving": ["moving expense", "relocation"],
            "home_office": ["home office", "work from home", "employment expense"],
            "gst": ["gst", "hst", "goods and services tax"],
            "filing": ["filing", "tax return", "deadline"],
            "credits": ["tax credit", "non-refundable credit"],
            "deductions": ["deduction", "deductible"],
            "business": ["business income", "self-employed"]
        }

        text_to_search = (title + " " + url + " " + content[:1000]).lower()

        for topic, keywords in topic_keywords.items():
            if any(keyword in text_to_search for keyword in keywords):
                topics.append(topic)

        # Default topic if none detected
        if not topics:
            topics.append("general")

        return topics

    def scrape_url(
        self,
        url: str,
        document_type: str = "guide",
        topics: Optional[List[str]] = None
    ) -> Optional[Path]:
        """
        Scrape a single CRA HTML page

        Args:
            url: URL to scrape
            document_type: Type of document (guide, faq, folio, etc.)
            topics: Optional list of topics (auto-detected if not provided)

        Returns:
            Path to saved document, or None if skipped/failed
        """
        try:
            logger.info(f"Scraping HTML: {url}")

            # Make request
            response = self._make_request(url)
            self.stats["successful_downloads"] += 1

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract content
            content = self._extract_main_content(soup)

            # Validate content
            if not self._validate_content(content):
                logger.warning(f"Invalid content from {url}")
                self.stats["failed_downloads"] += 1
                return None

            # Extract metadata
            metadata = self._extract_metadata(soup, url)
            metadata["document_type"] = document_type

            # Detect or use provided topics
            if topics:
                metadata["topics"] = topics
            else:
                metadata["topics"] = self._detect_topics(
                    metadata.get("title", ""),
                    content,
                    url
                )

            # Generate document ID
            document_id = self._generate_document_id(content, url)

            # Save document
            filepath = self._save_document(document_id, content, metadata)

            return filepath

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            self.stats["failed_downloads"] += 1
            return None

    def scrape(
        self,
        urls: List[str],
        document_type: str = "guide",
        topics: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Scrape multiple CRA HTML pages

        Args:
            urls: List of URLs to scrape
            document_type: Type of documents
            topics: Optional topics for all documents

        Returns:
            List of paths to saved documents
        """
        logger.info(f"Starting HTML scraping of {len(urls)} URLs")

        saved_paths = []
        for i, url in enumerate(urls, 1):
            logger.info(f"Progress: {i}/{len(urls)}")

            filepath = self.scrape_url(url, document_type, topics)
            if filepath:
                saved_paths.append(filepath)

        logger.info(f"Completed: {len(saved_paths)}/{len(urls)} documents saved")
        return saved_paths

    def scrape_tax_folios(self) -> List[Path]:
        """
        Scrape Income Tax Folios (all 7 series)

        Returns:
            List of paths to saved documents
        """
        logger.info("Scraping Income Tax Folios...")

        # Base URL for tax folios
        base_url = "https://www.canada.ca/en/revenue-agency/services/tax/technical-information/income-tax/income-tax-folios"

        # This would need to be populated with actual folio URLs
        # For now, return empty list - would need to crawl the index page
        logger.warning("Tax folio scraping requires index page crawling - implement separately")
        return []

    def scrape_top_questions(self) -> List[Path]:
        """
        Scrape top tax questions and tips

        Returns:
            List of paths to saved documents
        """
        logger.info("Scraping top tax questions...")

        # Example URLs - would need full list
        urls = [
            "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/tax-topics.html"
        ]

        return self.scrape(urls, document_type="faq", topics=["general"])


if __name__ == "__main__":
    # Test HTML scraper
    from loguru import logger

    logger.info("Testing CRA HTML Scraper")

    with CRAHTMLScraper() as scraper:
        # Test with a sample CRA page
        test_url = "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/about-your-tax-return/tax-return/completing-a-tax-return/deductions-credits-expenses/line-22900-other-employment-expenses/work-space-home-expenses.html"

        result = scraper.scrape_url(test_url, document_type="guide", topics=["home_office"])

        if result:
            logger.success(f"Successfully scraped and saved to: {result}")
        else:
            logger.error("Scraping failed")
