import logging
import time
from typing import Dict, Any
from sqlalchemy.orm import Session

# ===============================
# RAG / QUERY
# ===============================
from app.rag.query_classifier import (
    QueryClassifier,
    Intent,
    analyze_query,
)

# ===============================
# CONVERSATIONAL AGENTS
# ===============================
from app.agents.greeting_agent import GreetingAgent
from app.agents.help_agent import HelpAgent
from app.agents.clarification_agent import ClarificationAgent
from app.agents.fallback_agent import FallbackAgent

# ===============================
# DOMAIN AGENTS
# ===============================
from app.agents.data_extractor import DataExtractorAgent
from app.agents.review_generator import ReviewGeneratorAgent
from app.agents.confidence_agent import ConfidenceAgent

# ===============================
# CONFIG
# ===============================
try:
    from app.core.settings import settings
    CONFIDENCE_THRESHOLD = getattr(settings, "CONFIDENCE_THRESHOLD", 0.4)
except Exception:
    CONFIDENCE_THRESHOLD = 0.4

logger = logging.getLogger(__name__)


class AgentManager:
    """
    Central orchestrator of Conversational + RAG + Multi-Agent system.

    Pipeline:
    1. Intent classification
    2. Conversational shortcut (hi/help/etc)
    3. Domain analysis (RAG)
    4. Confidence scoring
    5. LLM generation
    """

    def __init__(self, db: Session):
        self.db = db

        # Conversational agents (cheap & fast)
        self.greeting_agent = GreetingAgent()
        self.help_agent = HelpAgent()
        self.clarification_agent = ClarificationAgent()
        self.fallback_agent = FallbackAgent()

        # Domain agents
        self.data_agent = DataExtractorAgent(db)
        self.review_agent = ReviewGeneratorAgent()
        self.confidence_agent = ConfidenceAgent()

    # ======================================================
    # MAIN ENTRY (API USES THIS)
    # ======================================================
    async def handle(self, question: str) -> Dict[str, Any]:
        start_time = time.perf_counter()

        try:
            # 1️⃣ High-level intent
            intent = QueryClassifier.classify(question)
            logger.info(f"Question='{question}' | Intent={intent}")

            # 2️⃣ Conversational short-circuit
            if intent in {
                Intent.GREETING,
                Intent.HELP,
                Intent.AMBIGUOUS,
                Intent.FALLBACK,
            }:
                answer = self._handle_conversational(intent)
                return self._response(answer, 1.0, intent.value, start_time)

            # 3️⃣ Domain (RAG) flow
            return await self._handle_domain(question, start_time)

        except Exception as e:
            logger.error("AgentManager fatal error", exc_info=True)
            return self._response(
                "⚠️ Internal system error. Please try again later.",
                0.0,
                "ERROR",
                start_time,
            )

    # ======================================================
    # CONVERSATIONAL HANDLER
    # ======================================================
    def _handle_conversational(self, intent: Intent) -> str:
        if intent == Intent.GREETING:
            return self.greeting_agent.run()

        if intent == Intent.HELP:
            return self.help_agent.run()

        if intent == Intent.AMBIGUOUS:
            return self.clarification_agent.run()

        return self.fallback_agent.run()

    # ======================================================
    # DOMAIN (RAG) HANDLER
    # ======================================================
    async def _handle_domain(self, question: str, start_time: float) -> Dict[str, Any]:
        # Step 1: semantic parsing
        domain_intent, entities = analyze_query(question)
        logger.debug(
            f"DomainIntent={domain_intent} | Entities={entities}"
        )

        # Step 2: DB / RAG fetch
        try:
            data = self.data_agent.run(domain_intent.value, entities)
        except Exception as e:
            logger.error("Data extraction failed", exc_info=True)
            return self._response(
                "❌ Database access failed. Please try again.",
                0.0,
                domain_intent.value,
                start_time,
            )

        if not data:
            msg = self._handle_no_data(domain_intent, entities)
            return self._response(msg, 0.0, domain_intent.value, start_time)

        # Step 3: confidence scoring
        confidence = self.confidence_agent.evaluate(data, intent=domain_intent.value)
        logger.info(f"Confidence={confidence}")

        if confidence < CONFIDENCE_THRESHOLD:
            return self._response(
                "⚠️ I found partial data, but it’s not reliable enough to answer confidently.",
                confidence,
                domain_intent.value,
                start_time,
            )

        # Step 4: LLM generation
        try:
            answer = self.review_agent.run(domain_intent.value, data)
        except Exception as e:
            logger.error("LLM generation failed", exc_info=True)
            return self._response(
                "❌ AI generation failed after retrieving data.",
                confidence,
                domain_intent.value,
                start_time,
            )

        return self._response(answer, confidence, domain_intent.value, start_time)

    # ======================================================
    # HELPERS
    # ======================================================
    def _handle_no_data(self, intent: Intent, entities: Dict[str, Any]) -> str:
        if intent == Intent.SPEC:
            return (
                f"I couldn’t find specs for "
                f"'{entities.get('model_name', 'this phone')}'."
            )

        if intent == Intent.COMPARE:
            return (
                "I need valid data for both phones to compare them."
            )

        if intent == Intent.RECOMMEND:
            return (
                "No Samsung phones matched your budget or criteria."
            )

        return "No relevant data found."

    def _response(
        self,
        answer: str,
        confidence: float,
        intent: str,
        start_time: float,
    ) -> Dict[str, Any]:
        latency = round((time.perf_counter() - start_time) * 1000, 2)
        return {
            "answer": answer,
            "confidence": round(confidence, 2),
            "intent": intent,
            "latency_ms": latency,
        }
