from app.core.database import SessionLocal
from app.models.phone import Phone


def insert_sample_phones():
    db = SessionLocal()

    phones = [
        Phone(
            model_name="Samsung Galaxy S24 Ultra",
            release_date="2024",
            display="6.8 AMOLED",
            battery=5000,
            camera="200MP",
            ram="12GB",
            storage="256GB",
            price=1299,
        ),
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
            model_name="Samsung Galaxy S24",
            release_date="2024",
            display="6.2 AMOLED",
            battery=4000,
            camera="50MP",
            ram="8GB",
            storage="256GB",
            price=899,
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
            model_name="Samsung Galaxy S21 FE",
            release_date="2022",
            display="6.4 AMOLED",
            battery=4500,
            camera="12MP",
            ram="8GB",
            storage="128GB",
            price=699,
        ),
        Phone(
            model_name="Samsung Galaxy A55",
            release_date="2024",
            display="6.6 AMOLED",
            battery=5000,
            camera="50MP",
            ram="8GB",
            storage="256GB",
            price=499,
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
        Phone(
            model_name="Samsung Galaxy A34",
            release_date="2023",
            display="6.6 AMOLED",
            battery=5000,
            camera="48MP",
            ram="6GB",
            storage="128GB",
            price=349,
        ),
        Phone(
            model_name="Samsung Galaxy A25",
            release_date="2023",
            display="6.5 AMOLED",
            battery=5000,
            camera="50MP",
            ram="6GB",
            storage="128GB",
            price=299,
        ),
        Phone(
            model_name="Samsung Galaxy M54",
            release_date="2023",
            display="6.7 AMOLED",
            battery=6000,
            camera="108MP",
            ram="8GB",
            storage="256GB",
            price=499,
        ),
        Phone(
            model_name="Samsung Galaxy M34",
            release_date="2023",
            display="6.5 AMOLED",
            battery=6000,
            camera="50MP",
            ram="6GB",
            storage="128GB",
            price=349,
        ),
        Phone(
            model_name="Samsung Galaxy F54",
            release_date="2023",
            display="6.7 AMOLED",
            battery=6000,
            camera="108MP",
            ram="8GB",
            storage="256GB",
            price=499,
        ),
        Phone(
            model_name="Samsung Galaxy Z Flip 5",
            release_date="2023",
            display="6.7 Foldable AMOLED",
            battery=3700,
            camera="12MP",
            ram="8GB",
            storage="256GB",
            price=999,
        ),
        Phone(
            model_name="Samsung Galaxy Z Fold 5",
            release_date="2023",
            display="7.6 Foldable AMOLED",
            battery=4400,
            camera="50MP",
            ram="12GB",
            storage="512GB",
            price=1799,
        ),
    ]

    db.add_all(phones)
    db.commit()
    db.close()

    print("✅ 15 Samsung phones inserted successfully")


if __name__ == "__main__":
    insert_sample_phones()
