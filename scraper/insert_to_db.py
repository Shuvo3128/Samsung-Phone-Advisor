from app.core.database import SessionLocal
from app.models.phone import Phone
from scraper.gsmarena_scraper import GSMArenaScraper


def insert_scraped_phones(limit: int = 25):
    scraper = GSMArenaScraper()
    phones_data = scraper.scrape(limit)

    db = SessionLocal()
    inserted = 0

    for data in phones_data:
        if not data.get("model_name"):
            continue

        phone = Phone(
            model_name=data["model_name"],
            release_date=data["release_date"],
            display=data["display"],
            battery=_parse_battery(data["battery"]),
            camera=data["camera"],
            ram=data["ram"],
            storage=data["storage"],
            price=None,
        )

        db.add(phone)
        inserted += 1

    db.commit()
    db.close()

    print(f"✅ Inserted {inserted} phones into DB")


def _parse_battery(text):
    if not text:
        return None
    try:
        return int(text.replace("mAh", "").strip())
    except:
        return None


if __name__ == "__main__":
    insert_scraped_phones(limit=25)
