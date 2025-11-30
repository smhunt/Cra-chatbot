"""
CLI Interface for CRA Documentation Scrapers
Easy-to-use command-line tool for collecting CRA documents
"""

import json
import click
from pathlib import Path
from loguru import logger
from typing import List

from src.data_collection.html_scraper import CRAHTMLScraper
from src.data_collection.pdf_scraper import CRAPDFScraper


@click.group()
def cli():
    """CRA Documentation Scraper CLI"""
    logger.info("CRA Chatbot - Documentation Collection Tool")


@cli.command()
@click.option(
    "--tier",
    type=click.Choice(["1", "2", "3", "all"]),
    default="1",
    help="Which tier of sources to scrape (1=core, 2=business, 3=comprehensive)"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be scraped without actually scraping"
)
def scrape_sources(tier: str, dry_run: bool):
    """
    Scrape CRA documentation sources from sources.json

    Tier 1 (Core): ~400 documents for Phase 1
    Tier 2 (Business): ~320 documents for Phase 2
    Tier 3 (Comprehensive): ~1100+ documents for Phase 3
    """
    # Load sources.json
    sources_file = Path("data/sources.json")

    if not sources_file.exists():
        logger.error(f"sources.json not found at {sources_file}")
        return

    with open(sources_file, "r") as f:
        sources_data = json.load(f)

    # Determine which tiers to scrape
    if tier == "all":
        tiers_to_scrape = ["tier_1_core", "tier_2_business_gst", "tier_3_comprehensive"]
    else:
        tier_map = {
            "1": "tier_1_core",
            "2": "tier_2_business_gst",
            "3": "tier_3_comprehensive"
        }
        tiers_to_scrape = [tier_map[tier]]

    logger.info(f"Scraping tiers: {tiers_to_scrape}")

    if dry_run:
        logger.info("DRY RUN MODE - No actual scraping will occur")

    total_sources = 0
    for tier_name in tiers_to_scrape:
        if tier_name not in sources_data["sources"]:
            logger.warning(f"Tier {tier_name} not found in sources.json")
            continue

        tier_data = sources_data["sources"][tier_name]
        sources = tier_data.get("sources", [])

        logger.info(f"\n{'='*60}")
        logger.info(f"Tier: {tier_data['description']}")
        logger.info(f"Estimated Documents: {tier_data['estimated_documents']}")
        logger.info(f"Target Accuracy: {tier_data['target_accuracy']}")
        logger.info(f"{'='*60}\n")

        for source in sources:
            total_sources += 1
            logger.info(f"\nSource {total_sources}: {source['name']}")
            logger.info(f"  ID: {source['id']}")
            logger.info(f"  URL: {source['url']}")
            logger.info(f"  Type: {source['document_type']}")
            logger.info(f"  Format: {source['format']}")
            logger.info(f"  Topics: {', '.join(source['topics'])}")
            logger.info(f"  Priority: {source['priority']}")
            logger.info(f"  Est. Count: {source['estimated_count']}")

            if dry_run:
                logger.info("  [SKIPPED - Dry run mode]")
                continue

            # Scrape based on format
            if source["format"] == "pdf":
                logger.info("  Scraping PDF...")
                with CRAPDFScraper() as scraper:
                    result = scraper.scrape_pdf(
                        source["url"],
                        document_type=source["document_type"],
                        topics=source["topics"],
                        tax_year=source.get("tax_year", 2024)
                    )
                    if result:
                        logger.success(f"  ✓ Saved to {result}")
                    else:
                        logger.error(f"  ✗ Failed to scrape")

            elif source["format"] == "html":
                logger.info("  Scraping HTML...")
                with CRAHTMLScraper() as scraper:
                    result = scraper.scrape_url(
                        source["url"],
                        document_type=source["document_type"],
                        topics=source["topics"]
                    )
                    if result:
                        logger.success(f"  ✓ Saved to {result}")
                    else:
                        logger.error(f"  ✗ Failed to scrape")

    logger.info(f"\nTotal sources: {total_sources}")


@cli.command()
@click.argument("url")
@click.option("--type", "doc_type", default="guide", help="Document type")
@click.option("--topics", default="general", help="Comma-separated topics")
@click.option("--year", type=int, default=2024, help="Tax year")
def scrape_url(url: str, doc_type: str, topics: str, year: int):
    """Scrape a single URL (HTML or PDF)"""
    topics_list = [t.strip() for t in topics.split(",")]

    logger.info(f"Scraping URL: {url}")
    logger.info(f"Type: {doc_type}, Topics: {topics_list}, Year: {year}")

    if url.endswith(".pdf"):
        with CRAPDFScraper() as scraper:
            result = scraper.scrape_pdf(url, doc_type, topics_list, year)
    else:
        with CRAHTMLScraper() as scraper:
            result = scraper.scrape_url(url, doc_type, topics_list)

    if result:
        logger.success(f"Saved to: {result}")
    else:
        logger.error("Scraping failed")


@cli.command()
@click.option("--guides", default="RC4092,RC4466,RC4065,T1-M,T777,P113", help="Comma-separated guide codes")
@click.option("--year", type=int, default=2024, help="Tax year")
def scrape_guides(guides: str, year: int):
    """Scrape CRA guides by code (e.g., RC4092, RC4466)"""
    guide_codes = [g.strip().upper() for g in guides.split(",")]

    logger.info(f"Scraping {len(guide_codes)} CRA guides for {year}")
    logger.info(f"Guides: {', '.join(guide_codes)}")

    with CRAPDFScraper() as scraper:
        results = scraper.scrape_cra_guides(guide_codes, year)

    logger.info(f"Successfully scraped {len(results)}/{len(guide_codes)} guides")


@cli.command()
def stats():
    """Show statistics about collected documents"""
    raw_data_path = Path("data/raw")

    if not raw_data_path.exists():
        logger.error("No data directory found")
        return

    # Count documents
    json_files = list(raw_data_path.glob("*.json"))
    pdf_files = list((raw_data_path / "pdfs").glob("*.pdf")) if (raw_data_path / "pdfs").exists() else []

    logger.info("="*60)
    logger.info("CRA Documentation Collection Statistics")
    logger.info("="*60)
    logger.info(f"JSON Documents:     {len(json_files)}")
    logger.info(f"PDFs Stored:        {len(pdf_files)}")

    # Analyze by document type
    doc_types = {}
    topics = {}
    tax_years = {}

    for json_file in json_files:
        try:
            with open(json_file, "r") as f:
                doc = json.load(f)

            # Count by type
            doc_type = doc.get("document_type", "unknown")
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1

            # Count by topics
            for topic in doc.get("topics", []):
                topics[topic] = topics.get(topic, 0) + 1

            # Count by tax year
            tax_year = doc.get("tax_year", "unknown")
            tax_years[str(tax_year)] = tax_years.get(str(tax_year), 0) + 1

        except Exception as e:
            logger.warning(f"Error reading {json_file}: {e}")

    logger.info("\nBy Document Type:")
    for doc_type, count in sorted(doc_types.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  {doc_type:20s}: {count:3d}")

    logger.info("\nBy Topic:")
    for topic, count in sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10]:
        logger.info(f"  {topic:20s}: {count:3d}")

    logger.info("\nBy Tax Year:")
    for year, count in sorted(tax_years.items(), reverse=True):
        logger.info(f"  {year:20s}: {count:3d}")

    logger.info("="*60)


@cli.command()
@click.argument("document_id")
def view(document_id: str):
    """View a scraped document by ID"""
    raw_data_path = Path("data/raw")

    # Find document
    pattern = f"{document_id}_*.json"
    matches = list(raw_data_path.glob(pattern))

    if not matches:
        logger.error(f"No document found with ID: {document_id}")
        return

    if len(matches) > 1:
        logger.warning(f"Multiple documents found: {len(matches)}")

    doc_path = matches[0]
    logger.info(f"Reading: {doc_path}")

    with open(doc_path, "r") as f:
        doc = json.load(f)

    logger.info("="*60)
    logger.info(f"Document: {doc.get('title', 'No title')}")
    logger.info("="*60)
    logger.info(f"ID:            {doc['document_id']}")
    logger.info(f"Type:          {doc['document_type']}")
    logger.info(f"Topics:        {', '.join(doc['topics'])}")
    logger.info(f"Tax Year:      {doc.get('tax_year', 'N/A')}")
    logger.info(f"Source:        {doc.get('source_url', 'N/A')}")
    logger.info(f"Length:        {doc['content_length']} chars")
    logger.info(f"Scraped:       {doc.get('date_scraped', 'N/A')}")
    logger.info("="*60)
    logger.info("\nContent Preview (first 500 chars):")
    logger.info("-"*60)
    logger.info(doc['content'][:500] + "...")
    logger.info("-"*60)


if __name__ == "__main__":
    cli()
