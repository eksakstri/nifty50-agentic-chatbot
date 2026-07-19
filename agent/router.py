import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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
"""

VALID_ROUTES = {
    "market",
    "option_chain",
    "pdf",
    "general"
}

# ---------------------------------------------------------
# Company aliases
# ---------------------------------------------------------

COMPANIES = {
    "reliance":"RELIANCE",
    "hdfc bank":"HDFCBANK",
    "hdfcbank":"HDFCBANK",
    "icici bank":"ICICIBANK",
    "icicibank":"ICICIBANK",
    "infosys":"INFY",
    "infy":"INFY",
    "tcs":"TCS",
    "sbi":"SBIN",
    "sbin":"SBIN",
    "bharti":"BHARTIARTL",
    "bharti airtel":"BHARTIARTL",
    "l&t":"LT",
    "lt":"LT",
    "larsen":"LT",
    "mahindra":"M&M",
    "m&m":"M&M",
    "bajaj finance":"BAJFINANCE",
    "axis":"AXISBANK",
    "axis bank":"AXISBANK",
    "cipla":"CIPLA",
    "hindalco":"HINDALCO",
    "tata steel":"TATASTEEL",
    "bel":"BEL",
    "bharat electronics":"BEL",
    "adani ports":"ADANIPORTS",
    "bajaj auto":"BAJAJ-AUTO",
    "maruti":"MARUTI",
    "maruti suzuki":"MARUTI",
    "sun pharma":"SUNPHARMA",
    "sunpharma":"SUNPHARMA",
    "adani enterprises":"ADANIENT",
    "trent":"TRENT",
    "eternal":"ETERNAL",
    "zomato":"ETERNAL",
    "ntpc":"NTPC",
    "wipro":"WIPRO",
    "kotak":"KOTAKBANK",
    "kotak bank":"KOTAKBANK",
    "dr reddy":"DRREDDY",
    "dr reddy's":"DRREDDY",
    "ultratech":"ULTRACEMCO",
    "ultracemco":"ULTRACEMCO",
    "hcl":"HCLTECH",
    "hcltech":"HCLTECH",
    "power grid":"POWERGRID",
    "powergrid":"POWERGRID",
    "tech mahindra":"TECHM",
    "techm":"TECHM",
    "asian paints":"ASIANPAINT",
    "max health":"MAXHEALTH",
    "maxhealth":"MAXHEALTH",
    "indigo":"INDIGO",
    "interglobe":"INDIGO",
    "shriram finance":"SHRIRAMFIN",
    "shriramfin":"SHRIRAMFIN",
    "eicher":"EICHERMOT",
    "eicher motors":"EICHERMOT",
    "itc":"ITC",
    "jsw steel":"JSWSTEEL",
    "jsw":"JSWSTEEL",
    "jio financial":"JIOFIN",
    "jiofin":"JIOFIN",
    "titan":"TITAN",
    "nestle":"NESTLEIND",
    "nestle india":"NESTLEIND",
    "grasim":"GRASIM",
    "apollo":"APOLLOHOSP",
    "apollo hospitals":"APOLLOHOSP",
    "hdfc life":"HDFCLIFE",
    "ongc":"ONGC",
    "sbi life":"SBILIFE",
    "sbilife":"SBILIFE",
    "bajaj finserv":"BAJAJFINSV",
    "tata consumer":"TATACONSUM",
    "tataconsumer":"TATACONSUM",
    "coal india":"COALINDIA",
    "coalindia":"COALINDIA",
    "hindustan unilever":"HINDUNILVR",
    "hul":"HINDUNILVR",
    "hindunilvr":"HINDUNILVR",
}


class QueryRouter:

    def __init__(self):
        self.client = client

    # ------------------------------------------------------

    def _rule_based_route(self, query):

        q = query.lower()

        company_found = any(c in q for c in COMPANIES)

        option_keywords = [
            "option","option chain","pcr","oi",
            "open interest","support","resistance",
            "strike","call","put","ce","pe",
            "atm","iv","implied volatility"
        ]

        market_keywords = [
            "market","nifty","sensex",
            "price","stock price",
            "top gainer","top loser",
            "gainers","losers",
            "performance","volume",
            "traded value","change",
            "52 week high","52 week low",
            "year high","year low","ltp"
        ]

        pdf_keywords = [
            "announcement","announce",
            "board meeting","board",
            "dividend","esop",
            "quarter","quarterly",
            "result","results",
            "earnings",
            "annual report",
            "report",
            "filing",
            "corporate action",
            "shareholder",
            "merger",
            "acquisition",
            "agreement",
            "investment",
            "contract",
            "order",
            "approval",
            "conference call",
            "guidance"
        ]

        # Company queries

        if company_found:

            if any(k in q for k in option_keywords):

                return {
                    "route":"option_chain",
                    "confidence":1.0,
                    "requires_llm":False,
                    "reason":"Company option query."
                }

            if any(k in q for k in market_keywords):

                return {
                    "route":"market",
                    "confidence":1.0,
                    "requires_llm":False,
                    "reason":"Company market query."
                }

            return {
                "route":"pdf",
                "confidence":0.99,
                "requires_llm":True,
                "reason":"Company specific query."
            }

        # Generic option queries

        if any(k in q for k in option_keywords):

            return {
                "route":"option_chain",
                "confidence":1.0,
                "requires_llm":False,
                "reason":"Matched option keywords."
            }

        # Generic market queries

        if any(k in q for k in market_keywords):

            return {
                "route":"market",
                "confidence":1.0,
                "requires_llm":False,
                "reason":"Matched market keywords."
            }

        # Generic corporate document queries

        if any(k in q for k in pdf_keywords):

            return {
                "route":"pdf",
                "confidence":1.0,
                "requires_llm":True,
                "reason":"Matched PDF keywords."
            }

        return None

    # ------------------------------------------------------

    def _llm_route(self, query):

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0,

            response_format={
                "type":"json_object"
            },

            messages=[
                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },
                {
                    "role":"user",
                    "content":query
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

        return {

            "route":route,

            "confidence":max(
                0.0,
                min(float(output.get("confidence",0.5)),1.0)
            ),

            "requires_llm":bool(
                output.get("requires_llm",True)
            ),

            "reason":output.get("reason","")
        }

    # ------------------------------------------------------

    def route(self, query):

        result = self._rule_based_route(query)

        if result is not None:
            return result

        try:
            return self._llm_route(query)

        except Exception:

            return {

                "route":"general",

                "confidence":0.0,

                "requires_llm":True,

                "reason":"LLM router failed."
            }


router = QueryRouter()
