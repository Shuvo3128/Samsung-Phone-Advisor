from typing import List, Optional, Dict
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.models.phone import Phone


# ======================================================
# 1. Pydantic Schemas (DTOs)
# ======================================================

class PhoneSpecs(BaseModel):
    model_name: str
    release_date: Optional[str] = None
    display: Optional[str] = None
    battery: Optional[int] = None
    camera: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    price: Optional[int] = None

    # Allow parsing directly from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


class PhoneSummary(BaseModel):
    model_name: str
    battery: Optional[int] = None
    camera: Optional[str] = None
    price: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# 2. SQL-based RAG Retriever
# ======================================================

class PhoneRAGRetriever:
    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------
    # Get full specs of a single phone
    # --------------------------------------------------
    def get_phone_specs(self, model_name: str) -> Optional[PhoneSpecs]:
        phone = (
            self.db.query(Phone)
            .filter(Phone.model_name.ilike(f"%{model_name}%"))
            .first()
        )

        if not phone:
            return None

        return PhoneSpecs.model_validate(phone)

    # --------------------------------------------------
    # Compare two phones
    # --------------------------------------------------
    def compare_phones(
        self, model_1: str, model_2: str
    ) -> Dict[str, Optional[PhoneSpecs]]:

        phones = (
            self.db.query(Phone)
            .filter(
                or_(
                    Phone.model_name.ilike(f"%{model_1}%"),
                    Phone.model_name.ilike(f"%{model_2}%"),
                )
            )
            .all()
        )

        result: Dict[str, Optional[PhoneSpecs]] = {
            "phone_1": None,
            "phone_2": None,
        }

        for phone in phones:
            specs = PhoneSpecs.model_validate(phone)

            if model_1.lower() in specs.model_name.lower():
                result["phone_1"] = specs
            elif model_2.lower() in specs.model_name.lower():
                result["phone_2"] = specs

        return result

    # --------------------------------------------------
    # Recommend phones under a given price
    # --------------------------------------------------
    def get_phones_under_price(
        self, max_price: int, limit: int = 10
    ) -> List[PhoneSummary]:

        phones = (
            self.db.query(Phone)
            .filter(Phone.price <= max_price)
            .order_by(Phone.price.desc())
            .limit(limit)
            .all()
        )

        return [PhoneSummary.model_validate(phone) for phone in phones]
