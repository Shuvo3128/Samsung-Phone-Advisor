import logging
from typing import Any, Dict

# Setup structured logging
logger = logging.getLogger(__name__)


class ConfidenceAgent:
    """
    Advanced confidence scoring system.

    Calculates a score (0.0 - 1.0) based on:
    1. Data Completeness (Are fields missing?)
    2. Data Quality (Are values 'N/A' or 0?)
    3. Field Importance (Is the missing field critical?)
    4. Comparison Overlap (Do both phones have the specs to compare?)
    """

    # Define weights: Critical fields affect the score more heavily
    CRITICAL_FIELDS = {
        "model_name": 1.0,
        "price": 0.9,
        "battery": 0.8,
        "camera": 0.8,
    }

    NORMAL_FIELDS = {
        "display": 0.5,
        "ram": 0.5,
        "storage": 0.5,
    }

    def evaluate(self, data: Any, intent: str = "general") -> float:
        """
        Main entry point.

        Args:
            data: The data retrieved (Dict, Pydantic model, or list).
            intent: Optional context (e.g., 'photography' could increase camera weight).
        """
        if not data:
            logger.warning("ConfidenceAgent: Data is empty/None.")
            return 0.0

        try:
            # Case 1: Comparison
            if isinstance(data, dict) and "phone_1" in data and "phone_2" in data:
                score = self._evaluate_comparison(data)
                logger.info(f"Confidence (Comparison): {score:.2f}")
                return score

            # Case 2: List of Phones
            if isinstance(data, list):
                if not data:
                    return 0.0
                scores = [self._evaluate_single(item) for item in data]
                avg_score = sum(scores) / len(scores)
                logger.info(f"Confidence (List): {avg_score:.2f}")
                return avg_score

            # Case 3: Single Object
            score = self._evaluate_single(data)
            logger.info(f"Confidence (Single): {score:.2f}")
            return score

        except Exception as e:
            logger.error("Confidence scoring failed", exc_info=True)
            return 0.3  # Fail-safe

    def _evaluate_single(self, model: Any) -> float:
        """
        Calculates weighted score for a single phone entity.
        """
        if hasattr(model, "model_dump"):
            fields = model.model_dump()
        elif isinstance(model, dict):
            fields = model
        else:
            return 0.2

        total_weight = 0.0
        earned_score = 0.0

        all_weights = {**self.CRITICAL_FIELDS, **self.NORMAL_FIELDS}

        for field, weight in all_weights.items():
            value = fields.get(field)
            total_weight += weight

            if self._is_valid_value(value):
                earned_score += weight
            else:
                logger.debug(f"Field '{field}' invalid/missing. Value: {value}")

        if total_weight == 0:
            return 0.5

        raw_score = earned_score / total_weight

        # Hard penalty if model name missing
        if not self._is_valid_value(fields.get("model_name")):
            raw_score *= 0.5

        return min(round(raw_score, 2), 0.99)

    def _evaluate_comparison(self, data: Dict) -> float:
        """
        Confidence based on overlap of valid fields between two phones.
        """
        p1 = data.get("phone_1")
        p2 = data.get("phone_2")

        if not p1 or not p2:
            return 0.0

        score_p1 = self._evaluate_single(p1)
        score_p2 = self._evaluate_single(p2)

        base_score = (score_p1 + score_p2) / 2

        gap = abs(score_p1 - score_p2)
        penalty = gap * 0.2

        return max(0.0, round(base_score - penalty, 2))

    def _is_valid_value(self, value: Any) -> bool:
        """
        Rejects: None, empty string, 'N/A', 'Unknown', 0, -1
        """
        if value is None:
            return False

        if isinstance(value, str):
            clean = value.strip().lower()
            if clean in {"", "n/a", "unknown", "tbd"}:
                return False

        if isinstance(value, (int, float)) and value <= 0:
            return False

        return True
