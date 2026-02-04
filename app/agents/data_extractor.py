from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.rag.retriever import PhoneRAGRetriever


class DataExtractorAgent:
    """
    Agent responsible for extracting structured phone data
    from PostgreSQL using SQL-based RAG.

    This layer must be:
    - Defensive (never crash API)
    - Deterministic (no guessing)
    - DB-only (no LLM here)
    """

    def __init__(self, db: Session):
        self.retriever = PhoneRAGRetriever(db)

    # --------------------------------------------------
    def run(self, intent: str, entities: Dict[str, Any]):
        """
        Main entry point.

        Returns:
            - PhoneSpecs (SPEC)
            - Dict(phone_1, phone_2) (COMPARE)
            - List[PhoneSummary] (RECOMMEND)
            - None if data not found or input invalid
        """

        try:
            if intent == "SPEC":
                return self._handle_spec(entities)

            if intent == "COMPARE":
                return self._handle_compare(entities)

            if intent == "RECOMMEND":
                return self._handle_recommend(entities)

            return None

        except Exception as e:
            # 🔥 NEVER let DB layer crash API
            print(f"[DataExtractorAgent] Error: {e}")
            return None

    # --------------------------------------------------
    def _handle_spec(self, entities: Dict[str, Any]):
        model_name = entities.get("model_name")

        if not model_name or len(model_name.strip()) < 2:
            return None

        return self.retriever.get_phone_specs(model_name)

    # --------------------------------------------------
    def _handle_compare(self, entities: Dict[str, Any]):
        model_1 = entities.get("model_1")
        model_2 = entities.get("model_2")

        # 🔒 SAFETY CHECK
        if not model_1 or not model_2:
            return None

        result = self.retriever.compare_phones(model_1, model_2)

        # Ensure meaningful comparison
        if not result:
            return None

        if not result.get("phone_1") or not result.get("phone_2"):
            return None

        return result

    # --------------------------------------------------
    def _handle_recommend(self, entities: Dict[str, Any]):
        max_price = entities.get("max_price", 1000)

        try:
            max_price = int(max_price)
        except Exception:
            max_price = 1000

        phones = self.retriever.get_phones_under_price(
            max_price=max_price,
            limit=10
        )

        return phones if phones else None
