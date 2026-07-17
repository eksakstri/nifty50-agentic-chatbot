import json
import re
from pathlib import Path

SNAPSHOT_PATH = Path(
    "../embeddings/nifty50_snapshot.json"
)


class MarketRetriever:

    def __init__(self):

        with open(
            SNAPSHOT_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            snapshot = json.load(f)

        self.market = snapshot
        self.data = snapshot["data"]

        # remove first row (NIFTY 50 index itself)
        self.companies = [
            x for x in self.data
            if x["symbol"] != "NIFTY 50"
        ]

        self.symbol_lookup = {
            x["symbol"].upper(): x
            for x in self.companies
        }

    # ----------------------------------------------------

    @staticmethod
    def to_float(value):

        if value is None:
            return 0.0

        value = (
            str(value)
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        if value in ["", "-"]:
            return 0.0

        try:
            return float(value)

        except:
            return 0.0

    # ----------------------------------------------------

    def rank(
        self,
        key,
        descending=True,
        top_n=5
    ):

        rows = sorted(
            self.companies,
            key=lambda x: self.to_float(
                x[key]
            ),
            reverse=descending
        )

        return rows[:top_n]

    # ----------------------------------------------------

    def company_search(
        self,
        query
    ):

        q = query.upper()

        for symbol, row in self.symbol_lookup.items():

            if symbol in q:
                return row

        return None

    # ----------------------------------------------------

    def retrieve(
        self,
        query
    ):

        q = query.lower()

        ##################################################
        # Company search
        ##################################################

        company = self.company_search(query)

        if company is not None:

            return {
                "intent": "company",
                "context": company
            }

        ##################################################
        # Top Gainers
        ##################################################

        if any(
            x in q
            for x in [
                "top gainer",
                "gainers",
                "best performer",
                "highest gain",
                "performed best",
                "rallied"
            ]
        ):

            return {
                "intent": "top_gainers",
                "context": self.rank(
                    "percent_change",
                    True,
                    5
                )
            }

        ##################################################
        # Top Losers
        ##################################################

        if any(
            x in q
            for x in [
                "top loser",
                "losers",
                "worst performer",
                "highest loss",
                "declined most",
                "fell most"
            ]
        ):

            return {
                "intent": "top_losers",
                "context": self.rank(
                    "percent_change",
                    False,
                    5
                )
            }

        ##################################################
        # Highest Volume
        ##################################################

        if (
            "volume" in q
            or "most traded" in q
        ):

            return {
                "intent": "highest_volume",
                "context": self.rank(
                    "volume",
                    True,
                    5
                )
            }

        ##################################################
        # Highest Traded Value
        ##################################################

        if (
            "traded value" in q
            or "turnover" in q
            or "value traded" in q
        ):

            return {
                "intent": "highest_value",
                "context": self.rank(
                    "traded_value_cr",
                    True,
                    5
                )
            }

        ##################################################
        # Best 30 day
        ##################################################

        if (
            "30 day" in q
            or "30d" in q
            or "month performance" in q
        ):

            return {
                "intent": "30_day",
                "context": self.rank(
                    "change_30d",
                    True,
                    5
                )
            }

        ##################################################
        # Ranking
        ##################################################

        if any(
            x in q
            for x in [
                "ranking",
                "rank",
                "sorted",
                "performance order"
            ]
        ):

            return {
                "intent": "ranking",
                "context": sorted(
                    self.companies,
                    key=lambda x:
                    self.to_float(
                        x["percent_change"]
                    ),
                    reverse=True
                )
            }

        ##################################################
        # Top N
        ##################################################

        m = re.search(
            r"top\s+(\d+)",
            q
        )

        if m:

            n = int(
                m.group(1)
            )

            return {

                "intent": "top_n",

                "context": self.rank(
                    "percent_change",
                    True,
                    n
                )
            }

        ##################################################
        # Market Snapshot
        ##################################################

        return {

            "intent": "market_snapshot",

            "context": {

                "total_companies":
                    self.market[
                        "total_companies"
                    ],

                "nifty":
                    self.data[0],

                "companies":
                    self.companies

            }

        }


market_retriever = MarketRetriever()