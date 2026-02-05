import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


BASE_URL = "https://www.gsmarena.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SamsungAdvisorBot/1.0)"
}


class GSMArenaScraper:
    """
    Scrapes Samsung phone specifications from GSMArena.
    """

    def __init__(self, delay: float = 1.5):
        self.delay = delay

    # -------------------------------------------------
    def fetch_samsung_phone_links(self, limit: int = 25) -> List[str]:
        """
        Fetch Samsung phone detail page links.
        """
        url = f"{BASE_URL}/samsung-phones-9.php"
        res = requests.get(url, headers=HEADERS, timeout=20)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        phone_links = []
        phones = soup.select(".makers ul li a")

        for phone in phones[:limit]:
            href = phone.get("href")
            phone_links.append(f"{BASE_URL}/{href}")

        return phone_links

    # -------------------------------------------------
    def scrape_phone(self, url: str) -> Dict:
        """
        Scrape individual phone specification page.
        """
        res = requests.get(url, headers=HEADERS, timeout=20)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        def safe_text(selector):
            el = soup.select_one(selector)
            return el.text.strip() if el else None

        phone = {
            "model_name": safe_text("h1.specs-phone-name-title"),
            "release_date": safe_text("span[data-spec=released-hl]"),
            "display": safe_text("span[data-spec=displaysize-hl]"),
            "battery": safe_text("span[data-spec=battery-hl]"),
            "camera": safe_text("span[data-spec=cam1modules]"),
            "ram": safe_text("span[data-spec=internalmemory]"),
            "storage": safe_text("span[data-spec=internalmemory]"),
            "price": None,  # GSMArena doesn't give reliable prices
        }

        return phone

    # -------------------------------------------------
    def scrape(self, limit: int = 25) -> List[Dict]:
        """
        Main scraper pipeline.
        """
        phones_data = []
        links = self.fetch_samsung_phone_links(limit)

        for idx, link in enumerate(links, start=1):
            try:
                print(f"[{idx}/{len(links)}] Scraping {link}")
                phone = self.scrape_phone(link)
                phones_data.append(phone)
                time.sleep(self.delay)
            except Exception as e:
                print(f"❌ Failed: {e}")

        return phones_data
