import json
import os
from pathlib import Path

from config import GROQ_API_KEY
from config import MONGO_URI
from groq import Groq

from state import AgentState

client = Groq(
    api_key=GROQ_API_KEY
)

PDF_PROMPT = """
You are a financial assistant.

You MUST answer ONLY from the supplied context.

Rules:

- Never invent facts.
- Never use outside knowledge.
- If the answer is not present, say:

'I could not find that information in the available company documents.'

- Mention company names whenever possible.
- Do not mention embeddings, FAISS, vector search or retrieval.
"""

MARKET_PROMPT = """
You are a stock market assistant.

Answer ONLY from the supplied market snapshot.

Do not invent statistics.

If the requested information is unavailable, clearly state so.

Keep answers concise.
"""

OPTION_PROMPT = """
You are an option-chain analyst.

Answer ONLY from the supplied option-chain data.

Never estimate support/resistance.

Never fabricate PCR or OI.

If unavailable, clearly say so.
"""

GENERAL_PROMPT = """
You are a finance assistant.

Provide accurate educational answers.

If you are unsure, explicitly say so rather than guessing.
"""


# =====================================================
# Generator
# =====================================================

class AnswerGenerator:

    def __init__(self):

        self.client = client

    # -------------------------------------------------

    def _system_prompt(self, source):

        if source == "pdf":
            return PDF_PROMPT

        if source == "market":
            return MARKET_PROMPT

        if source == "option_chain":
            return OPTION_PROMPT

        return GENERAL_PROMPT

    # -------------------------------------------------

    def _context_missing(self, state):

        context = state.get("retrieved_context")

        if context is None:
            return True

        if isinstance(context, list) and len(context) == 0:
            return True

        if isinstance(context, dict):

            if "context" in context:

                value = context["context"]

                if value is None:
                    return True

                if isinstance(value, list) and len(value) == 0:
                    return True

        return False

    # -------------------------------------------------

    def _confidence_failed(self, state):

        confidence = state.get(
            "retrieval_confidence",
            1.0
        )

        source = state.get(
            "retrieval_source"
        )

        if source == "pdf":

            return confidence < 0.45

        return False

    # -------------------------------------------------

    def generate(self, state):

        source = state["retrieval_source"]

        query = state["query"]

        # ==========================================
        # Confidence Gate
        # ==========================================

        if self._confidence_failed(state):

            return (
                "I couldn't find enough relevant information "
                "in the available company documents to answer "
                "that confidently."
            )

        # ==========================================
        # Empty Context Gate
        # ==========================================

        if source != "general":

            if self._context_missing(state):

                if source == "pdf":

                    return (
                        "I could not find that information "
                        "in the available company documents."
                    )

                elif source == "market":

                    return (
                        "The requested market information "
                        "is not available in today's snapshot."
                    )

                elif source == "option_chain":

                    return (
                        "The requested option-chain information "
                        "is not available."
                    )

        # ==========================================
        # General Route
        # ==========================================

        if source == "general":

            user_prompt = query

        else:

            context = state["retrieved_context"]

            if isinstance(context, (dict, list)):
                context = json.dumps(
                    context,
                    indent=2,
                    ensure_ascii=False
                )

            user_prompt = f"""
Question

{query}

--------------------------------

Context

{context}

--------------------------------

Answer ONLY using the supplied context.
"""

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0,

            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt(source)
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()


generator = AnswerGenerator()


# =====================================================
# LangGraph Node
# =====================================================

def answer_node(state: AgentState):

    state["answer"] = generator.generate(state)

    return state