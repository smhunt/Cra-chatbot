"""
PDF Scraper and Extractor for CRA Documents
Downloads and extracts text from PDF guides, forms, and publications
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import pdfplumber
import PyPDF2
from loguru import logger
import re

from src.data_collection.base_scraper import BaseScraper, BaseScraperError


class CRAPDFScraper(BaseScraper):
    """
    Scraper for CRA PDF documents

    Handles:
    - Tax guides (T1, RC series)
    - Forms with instructions
    - Publications and bulletins
    - GST/HST memoranda (PDF versions)

    Features:
    - Downloads PDFs
    - Extracts text using pdfplumber (better for tables)
    - Fallback to PyPDF2 if pdfplumber fails
    - Preserves document structure
    """

    def __init__(self, save_pdfs: bool = True):
        """
        Initialize PDF scraper

        Args:
            save_pdfs: If True, save original PDFs in addition to extracted text
        """
        super().__init__()
        self.save_pdfs = save_pdfs

        # Create PDF storage directory
        if self.save_pdfs:
            self.pdf_storage_path = self.raw_data_path / "pdfs"
            self.pdf_storage_path.mkdir(parents=True, exist_ok=True)

        logger.info("CRAPDFScraper initialized")

    def _extract_text_pdfplumber(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using pdfplumber (better for tables and structure)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        try:
            text_parts = []

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text
                    page_text = page.extract_text()

                    if page_text:
                        text_parts.append(f"--- Page {page_num} ---\n{page_text}")

                    # Extract tables if present
                    tables = page.extract_tables()
                    if tables:
                        for table_num, table in enumerate(tables, 1):
                            table_text = self._format_table(table)
                            text_parts.append(f"\n[Table {table_num} on Page {page_num}]\n{table_text}\n")

            full_text = "\n\n".join(text_parts)
            logger.debug(f"Extracted {len(full_text)} chars using pdfplumber")
            return full_text

        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
            raise

    def _extract_text_pypdf2(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using PyPDF2 (fallback method)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        try:
            text_parts = []

            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page_num, page in enumerate(pdf_reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(f"--- Page {page_num} ---\n{page_text}")

            full_text = "\n\n".join(text_parts)
            logger.debug(f"Extracted {len(full_text)} chars using PyPDF2")
            return full_text

        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            raise

    def _format_table(self, table: List[List[str]]) -> str:
        """
        Format extracted table as text

        Args:
            table: List of rows, each row is a list of cell values

        Returns:
            Formatted table string
        """
        if not table:
            return ""

        # Find maximum width for each column
        col_widths = []
        for col_idx in range(len(table[0])):
            max_width = max(
                len(str(row[col_idx] or ""))
                for row in table
                if col_idx < len(row)
            )
            col_widths.append(max_width)

        # Format rows
        formatted_rows = []
        for row in table:
            formatted_cells = []
            for col_idx, cell in enumerate(row):
                cell_str = str(cell or "").ljust(col_widths[col_idx])
                formatted_cells.append(cell_str)
            formatted_rows.append(" | ".join(formatted_cells))

        return "\n".join(formatted_rows)

    def _extract_pdf_metadata(self, pdf_path: Path, url: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF

        Args:
            pdf_path: Path to PDF file
            url: Source URL

        Returns:
            Metadata dictionary
        """
        metadata = {
            "source_url": url,
            "format": "pdf",
            "file_size_bytes": pdf_path.stat().st_size
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Basic PDF metadata
                metadata["page_count"] = len(pdf.pages)

                # Try to extract PDF metadata
                if pdf.metadata:
                    if "Title" in pdf.metadata:
                        metadata["title"] = pdf.metadata["Title"]
                    if "Author" in pdf.metadata:
                        metadata["author"] = pdf.metadata["Author"]
                    if "CreationDate" in pdf.metadata:
                        metadata["creation_date"] = str(pdf.metadata["CreationDate"])

        except Exception as e:
            logger.warning(f"Could not extract PDF metadata: {e}")

        # Extract title from filename if not in metadata
        if "title" not in metadata:
            # Convert URL/filename to title
            filename = pdf_path.stem
            metadata["title"] = filename.replace("_", " ").replace("-", " ").title()

        # Try to extract tax year from filename or title
        tax_year_match = re.search(
            r'20\d{2}',
            metadata.get("title", "") + " " + url
        )
        if tax_year_match:
            metadata["tax_year"] = int(tax_year_match.group())

        return metadata

    def download_pdf(self, url: str, filename: Optional[str] = None) -> Path:
        """
        Download PDF from URL

        Args:
            url: URL to PDF
            filename: Optional custom filename

        Returns:
            Path to downloaded PDF

        Raises:
            BaseScraperError: If download fails
        """
        logger.info(f"Downloading PDF: {url}")

        # Make request
        response = self._make_request(url)

        # Verify it's actually a PDF
        content_type = response.headers.get("Content-Type", "")
        if "pdf" not in content_type.lower():
            logger.warning(f"URL may not be PDF (Content-Type: {content_type})")

        # Generate filename
        if not filename:
            # Extract from URL
            url_path = Path(url)
            filename = url_path.name
            if not filename.endswith(".pdf"):
                filename = f"{url_path.stem}.pdf"

        # Save PDF
        pdf_path = self.pdf_storage_path / filename if self.save_pdfs else Path(f"/tmp/{filename}")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        with open(pdf_path, "wb") as f:
            f.write(response.content)

        logger.info(f"Downloaded PDF: {pdf_path} ({len(response.content)} bytes)")
        self.stats["successful_downloads"] += 1

        return pdf_path

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from PDF using best available method

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text

        Raises:
            BaseScraperError: If extraction fails with all methods
        """
        # Try pdfplumber first (better for structured documents)
        try:
            text = self._extract_text_pdfplumber(pdf_path)
            if text and len(text.strip()) > 100:
                return text
        except Exception as e:
            logger.warning(f"pdfplumber failed, trying PyPDF2: {e}")

        # Fallback to PyPDF2
        try:
            text = self._extract_text_pypdf2(pdf_path)
            if text and len(text.strip()) > 100:
                return text
        except Exception as e:
            logger.error(f"PyPDF2 also failed: {e}")

        raise BaseScraperError("Could not extract text from PDF with any method")

    def scrape_pdf(
        self,
        url: str,
        document_type: str = "guide",
        topics: Optional[List[str]] = None,
        tax_year: Optional[int] = None
    ) -> Optional[Path]:
        """
        Download and extract text from a single PDF

        Args:
            url: URL to PDF
            document_type: Type of document (guide, form, bulletin, etc.)
            topics: List of topics
            tax_year: Tax year (auto-detected if not provided)

        Returns:
            Path to saved document JSON, or None if failed
        """
        try:
            logger.info(f"Scraping PDF: {url}")

            # Download PDF
            pdf_path = self.download_pdf(url)

            # Extract text
            content = self.extract_text_from_pdf(pdf_path)

            # Validate content
            if not self._validate_content(content, min_length=200):
                logger.warning(f"Invalid content from {url}")
                self.stats["failed_downloads"] += 1
                return None

            # Extract metadata
            metadata = self._extract_pdf_metadata(pdf_path, url)
            metadata["document_type"] = document_type

            if topics:
                metadata["topics"] = topics
            if tax_year:
                metadata["tax_year"] = tax_year

            # Generate document ID
            document_id = self._generate_document_id(content, url)

            # Save document
            filepath = self._save_document(document_id, content, metadata)

            # Clean up temporary PDF if not saving
            if not self.save_pdfs and pdf_path.exists():
                pdf_path.unlink()

            return filepath

        except Exception as e:
            logger.error(f"Error scraping PDF {url}: {e}")
            self.stats["failed_downloads"] += 1
            return None

    def scrape(
        self,
        urls: List[str],
        document_type: str = "guide",
        topics: Optional[List[str]] = None,
        tax_year: Optional[int] = None
    ) -> List[Path]:
        """
        Scrape multiple PDFs

        Args:
            urls: List of PDF URLs
            document_type: Type of documents
            topics: Optional topics for all documents
            tax_year: Optional tax year for all documents

        Returns:
            List of paths to saved documents
        """
        logger.info(f"Starting PDF scraping of {len(urls)} documents")

        saved_paths = []
        for i, url in enumerate(urls, 1):
            logger.info(f"Progress: {i}/{len(urls)}")

            filepath = self.scrape_pdf(url, document_type, topics, tax_year)
            if filepath:
                saved_paths.append(filepath)

        logger.info(f"Completed: {len(saved_paths)}/{len(urls)} PDFs processed")
        return saved_paths

    def scrape_cra_guides(self, guide_codes: List[str], tax_year: int = 2024) -> List[Path]:
        """
        Scrape CRA guides by their code (e.g., RC4092, T4002)

        Args:
            guide_codes: List of CRA guide codes (e.g., ["RC4092", "RC4466"])
            tax_year: Tax year

        Returns:
            List of paths to saved documents
        """
        logger.info(f"Scraping CRA guides: {guide_codes}")

        # CRA guide URL pattern
        base_url = "https://www.canada.ca/content/dam/cra-arc/formspubs"

        urls = []
        topics_map = {
            "RC4092": ["rrsp"],  # RRSP guide
            "RC4466": ["tfsa"],  # TFSA guide
            "RC4065": ["medical"],  # Medical expenses
            "T1-M": ["moving"],  # Moving expenses
            "T777": ["home_office"],  # Employment expenses
            "P113": ["charitable"]  # Charitable donations
        }

        for code in guide_codes:
            # Construct URL (may need adjustment based on actual CRA URL structure)
            url = f"{base_url}/{code.lower()}/{code.lower()}-{tax_year // 100}e.pdf"
            urls.append(url)

        # Scrape with appropriate topics
        results = []
        for i, url in enumerate(urls):
            code = guide_codes[i]
            topics = topics_map.get(code, ["general"])

            filepath = self.scrape_pdf(
                url,
                document_type="guide",
                topics=topics,
                tax_year=tax_year
            )
            if filepath:
                results.append(filepath)

        return results


if __name__ == "__main__":
    # Test PDF scraper
    from loguru import logger

    logger.info("Testing CRA PDF Scraper")

    with CRAPDFScraper(save_pdfs=True) as scraper:
        # Test with a sample CRA guide
        # Note: This is an example URL - actual URLs may differ
        test_url = "https://www.canada.ca/content/dam/cra-arc/formspubs/pub/rc4092/rc4092-24e.pdf"

        result = scraper.scrape_pdf(
            test_url,
            document_type="guide",
            topics=["rrsp"],
            tax_year=2024
        )

        if result:
            logger.success(f"Successfully scraped PDF and saved to: {result}")
        else:
            logger.error("PDF scraping failed")
