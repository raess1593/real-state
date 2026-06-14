import json
import logging
import os
from datetime import datetime
from typing import TypedDict

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


class ScrapedProperty(TypedDict):
    title: str
    price: str
    location: str | None
    meters: str


class RealEstateScraper:
    def __init__(self, url: str | None = None, page_limit: int = 1) -> None:
        self.url: str | None = url or os.getenv("url")
        self.page_limit: int = page_limit
        self.data: list[ScrapedProperty] = []

    def fetch_page(self, page_number: int = 1) -> str | None:
        if self.url is None:
            raise ValueError("URL is not configured")

        complete_url = f"{self.url}/page/{page_number}/"
        response = requests.get(complete_url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return None
        else:
            raise Exception(f"Failed to fetch page: {response.status_code}")

    def parse_page(self, html_content: str) -> None:
        soup = BeautifulSoup(html_content, "html.parser")
        try:
            properties = soup.find_all("div", class_="property-inner")
        except Exception:
            logger.exception("Error occurred while parsing page")
            return

        for prop in properties:
            try:
                title = prop.find("h2", class_="property-title").get_text(strip=True)
                price = prop.find("span", class_="property-price").get_text(strip=True)
                location_div = prop.find("div", class_="property-location")
                location = location_div.get("title")
                meters = prop.find("span", class_="ere__lpi-value").get_text(strip=True)
                self.data.append(
                    {
                        "title": title,
                        "price": price,
                        "location": location,
                        "meters": meters,
                    }
                )
                logger.info("Scraped property: %s", self.data[-1])
            except Exception:
                logger.exception("Error occurred while extracting property data")

    def save_data(self, filename: str) -> None:
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except IOError:
            logger.exception("File system error occurred while saving data")

    def run(self) -> None:
        for page in range(1, self.page_limit + 1):
            logger.info("Scraping page %s...", page)

            html_content = self.fetch_page(page)
            if html_content is None:
                logger.warning("Page %s not found. Stopping scraper.", page)
                break

            self.parse_page(html_content)

        output_file = (
            f"data/scraped_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        self.save_data(output_file)
        logger.info("Saved %s scraped properties to %s", len(self.data), output_file)


if __name__ == "__main__":
    scraper = RealEstateScraper(page_limit=5)
    scraper.run()
