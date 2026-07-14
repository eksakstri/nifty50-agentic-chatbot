import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================================
# Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are NOT a chatbot.

You are ONLY an intent classifier.

You NEVER answer the user's question.

Your job is ONLY to classify which tool should answer.

Available routes:

1. market
Use for:
- top gainers
- top losers
- stock performance
- market performance
- nifty
- volume
- traded value
- daily change
- yearly high
- yearly low

requires_llm:
false for simple ranking/statistics
true for comparison/summarization

------------------------------------------------

2. option_chain

Use for:

PCR
OI
Open Interest
Support
Resistance
Strike
Call
Put
CE
PE
Volume
IV
ATM

requires_llm:
false for direct lookups
true for explanations

------------------------------------------------

3. pdf

Use for:

Company announcements
Board meetings
Dividend
ESOP
Mergers
Acquisition
Quarterly Results
Corporate Action
Shareholder Meeting
Trading Window
Annual Report

requires_llm:
always true

------------------------------------------------

4. general

Use for

Finance education
Definitions
Concepts
Knowledge not present in datasets

requires_llm:
always true

------------------------------------------------

Return ONLY JSON.

Format:

{
    "route":"market",
    "confidence":0.98,
    "requires_llm":false,
    "reason":"Daily market performance."
}

Never return markdown.

Never explain.

Never answer the user.
"""


VALID_ROUTES = {
    "market",
    "option_chain",
    "pdf",
    "general"
}


# ==========================================================
# Router
# ==========================================================

class QueryRouter:

    def __init__(self):

        self.client = client

    # ------------------------------------------------------

    def _rule_based_route(self, query):

        q = query.lower()

        option_keywords = [
            "pcr",
            "option",
            "strike",
            "support",
            "resistance",
            "oi",
            "open interest",
            "call",
            "put",
            "ce",
            "pe",
            "atm",
            "iv",
            "implied volatility"
        ]

        market_keywords = [
            "top gainer",
            "top loser",
            "market",
            "nifty",
            "perform",
            "performance",
            "volume",
            "traded value",
            "change",
            "last price",
            "year high",
            "year low"
        ]

        pdf_keywords = [
            "announcement",
            "board meeting",
            "dividend",
            "esop",
            "quarter",
            "results",
            "report",
            "filing",
            "corporate action",
            "shareholder",
            "merger",
            "acquisition"
        ]

        if any(k in q for k in option_keywords):

            return {
                "route": "option_chain",
                "confidence": 1.0,
                "requires_llm": False,
                "reason": "Matched option chain keywords."
            }

        if any(k in q for k in market_keywords):

            return {
                "route": "market",
                "confidence": 1.0,
                "requires_llm": False,
                "reason": "Matched market keywords."
            }

        if any(k in q for k in pdf_keywords):

            return {
                "route": "pdf",
                "confidence": 1.0,
                "requires_llm": True,
                "reason": "Matched company document keywords."
            }

        return None

    # ------------------------------------------------------

    def _llm_route(self, query):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0,

            response_format={
                "type": "json_object"
            },

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        output = json.loads(
            response.choices[0].message.content
        )

        route = output.get(
            "route",
            "general"
        )

        if route not in VALID_ROUTES:

            route = "general"

        confidence = float(
            output.get(
                "confidence",
                0.5
            )
        )

        confidence = max(
            0.0,
            min(
                confidence,
                1.0
            )
        )

        requires_llm = bool(
            output.get(
                "requires_llm",
                True
            )
        )

        return {

            "route": route,

            "confidence": confidence,

            "requires_llm": requires_llm,

            "reason": output.get(
                "reason",
                ""
            )
        }

    # ------------------------------------------------------

    def route(self, query):

        rule_result = self._rule_based_route(query)

        if rule_result is not None:

            return rule_result

        try:

            return self._llm_route(query)

        except Exception:

            return {

                "route": "general",

                "confidence": 0.0,

                "requires_llm": True,

                "reason": "LLM router failed."
            }


router = QueryRouter()