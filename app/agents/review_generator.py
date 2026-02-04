import json
import subprocess
from typing import Any

from app.core.settings import settings


class ReviewGeneratorAgent:
    """
    Agent responsible for generating natural-language
    reviews and recommendations using a local LLM (Ollama).
    Production-safe & hallucination-controlled.
    """

    def __init__(self, model_name: str | None = None):
        # Centralized model config
        self.model_name = model_name or settings.OLLAMA_MODEL

    # --------------------------------------------------
    def run(self, intent: str, data: Any) -> str:
        if not data:
            return "Sorry, I could not find relevant Samsung phone data."

        prompt = self._build_prompt(intent, data)
        return self._call_ollama(prompt)

    # --------------------------------------------------
    def _call_ollama(self, prompt: str) -> str:
        """
        Calls Ollama safely using subprocess.
        Handles Windows Unicode issues + timeout.
        """

        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                capture_output=True,
                encoding="utf-8",      # ✅ Windows fix
                errors="ignore",       # ✅ Safety
                timeout=120,           # ✅ Prevent hanging
            )

            if result.returncode != 0:
                return (
                    "LLM generation failed. "
                    "Please check if Ollama is running correctly."
                )

            output = result.stdout.strip()
            return output if output else "LLM returned an empty response."

        except subprocess.TimeoutExpired:
            return "LLM request timed out. Please try again."

        except Exception as e:
            return f"LLM execution error: {str(e)}"

    # --------------------------------------------------
    def _normalize(self, obj: Any) -> Any:
        """
        Converts Pydantic models, lists, and dicts
        into pure Python objects safe for JSON serialization.
        """

        if isinstance(obj, list):
            return [self._normalize(item) for item in obj]

        if isinstance(obj, dict):
            return {key: self._normalize(value) for key, value in obj.items()}

        # Pydantic v2
        if hasattr(obj, "model_dump"):
            return obj.model_dump()

        return obj

    # --------------------------------------------------
    def _build_prompt(self, intent: str, data: Any) -> str:
        safe_data = self._normalize(data)

        system_rules = (
            "You are a Samsung smartphone expert.\n"
            "STRICT RULES:\n"
            "- Use ONLY the provided data\n"
            "- Do NOT guess or invent specifications\n"
            "- If data is missing, say it clearly\n"
            "- Keep explanations clear and user-friendly\n"
        )

        if intent == "SPEC":
            return f"""
{system_rules}

Task:
Explain the following Samsung phone specifications clearly and simply.

DATA:
{json.dumps(safe_data, indent=2)}
"""

        if intent == "COMPARE":
            return f"""
{system_rules}

Task:
Compare the following Samsung phones.
Focus on:
- Camera
- Battery
- Performance
- Overall recommendation

DATA:
{json.dumps(safe_data, indent=2)}
"""

        if intent == "RECOMMEND":
            return f"""
{system_rules}

Task:
Based on the phones below, recommend the BEST Samsung phone.
Explain clearly why it is the best choice.

DATA:
{json.dumps(safe_data, indent=2)}
"""

        return f"""
{system_rules}

Task:
Generate a helpful Samsung smartphone review based on this data.

DATA:
{json.dumps(safe_data, indent=2)}
"""
