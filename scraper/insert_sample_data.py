from app.core.database import SessionLocal
from app.models.phone import Phone


def insert_sample_phones():
    db = SessionLocal()

    phones = [
        Phone(
            model_name="Samsung Galaxy S23 Ultra",
            release_date="2023",
            display="6.8 AMOLED",
            battery=5000,
            camera="200MP",
            ram="12GB",
            storage="256GB",
            price=1199,
        ),
        Phone(
            model_name="Samsung Galaxy S22 Ultra",
            release_date="2022",
            display="6.8 AMOLED",
            battery=5000,
            camera="108MP",
            ram="12GB",
            storage="256GB",
            price=999,
        ),
        Phone(
            model_name="Samsung Galaxy S23",
            release_date="2023",
            display="6.1 AMOLED",
            battery=3900,
            camera="50MP",
            ram="8GB",
            storage="128GB",
            price=799,
        ),
        Phone(
            model_name="Samsung Galaxy A54",
            release_date="2023",
            display="6.4 AMOLED",
            battery=5000,
            camera="50MP",
            ram="8GB",
            storage="128GB",
            price=449,
        ),
    ]

    db.add_all(phones)
    db.commit()
    db.close()

    print("✅ Sample GSMArena phone data inserted successfully")


if __name__ == "__main__":
    insert_sample_phones()
