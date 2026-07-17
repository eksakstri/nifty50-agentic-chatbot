import re
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "embeddings"

CSV_PATH = DATA_DIR / "option_chain.csv"

class OptionChainRetriever:

    def __init__(self):

        self.df = self._load_csv()

    # -------------------------------------------------------

    def _load_csv(self):

        df = pd.read_csv(
            CSV_PATH,
            header = 0 
        )
        print(df.columns)
        print()
        df = df.drop(
            columns=[
                "Unnamed: 1",
                "Unnamed: 24"
            ]
        )
        print(df.columns)

        df.columns = [
            "call_oi",
            "call_change_oi",
            "call_volume",
            "call_iv",
            "call_ltp",
            "call_change",
            "call_bid_qty",
            "call_bid",
            "call_ask",
            "call_ask_qty",
            "strike",
            "put_bid_qty",
            "put_bid",
            "put_ask",
            "put_ask_qty",
            "put_change",
            "put_ltp",
            "put_iv",
            "put_volume",
            "put_change_oi",
            "put_oi",
            "unused"
        ]

        df = df.drop(
            columns=["unused"],
            errors="ignore"
        )

        for c in df.columns:

            df[c] = (
                df[c]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("-", "", regex=False)
                .str.strip()
            )

            if c != "strike":

                df[c] = pd.to_numeric(
                    df[c],
                    errors="coerce"
                )

        df["strike"] = pd.to_numeric(
            df["strike"],
            errors="coerce"
        )

        df = df.dropna(
            subset=["strike"]
        )

        return df.reset_index(drop=True)

    # -------------------------------------------------------

    def highest_call_oi(
        self,
        n=5
    ):

        return self.df.nlargest(
            n,
            "call_oi"
        )

    # -------------------------------------------------------

    def highest_put_oi(
        self,
        n=5
    ):

        return self.df.nlargest(
            n,
            "put_oi"
        )

    # -------------------------------------------------------

    def highest_call_volume(
        self,
        n=5
    ):

        return self.df.nlargest(
            n,
            "call_volume"
        )

    # -------------------------------------------------------

    def highest_put_volume(
        self,
        n=5
    ):

        return self.df.nlargest(
            n,
            "put_volume"
        )

    # -------------------------------------------------------

    def highest_call_change_oi(
        self,
        n=5
    ):

        return self.df.nlargest(
            n,
            "call_change_oi"
        )

    # -------------------------------------------------------

    def highest_put_change_oi(
        self,
        n=5
    ):

        return self.df.nlargest(
            n,
            "put_change_oi"
        )

    # -------------------------------------------------------

    def support_levels(
        self,
        n=5
    ):

        return self.highest_put_oi(n)

    # -------------------------------------------------------

    def resistance_levels(
        self,
        n=5
    ):

        return self.highest_call_oi(n)

    # -------------------------------------------------------

    def calculate_pcr(self):

        call = self.df["call_oi"].sum()

        put = self.df["put_oi"].sum()

        if call == 0:

            return None

        return round(
            put / call,
            3
        )

    # -------------------------------------------------------

    def atm(self):

        row = self.df.iloc[
            (
                self.df["call_ltp"]
                -
                self.df["put_ltp"]
            ).abs().idxmin()
        ]

        return row

    # -------------------------------------------------------

    def strike(
        self,
        strike
    ):

        row = self.df[
            self.df["strike"] == strike
        ]

        if len(row) == 0:

            return None

        return row.iloc[0]

    # -------------------------------------------------------

    def compare(
        self,
        strikes
    ):

        return self.df[
            self.df["strike"].isin(strikes)
        ]

    # -------------------------------------------------------

    def market_structure(self):

        return {

            "atm":

                self.atm().to_dict(),

            "support":

                self.support_levels(3).to_dict(
                    "records"
                ),

            "resistance":

                self.resistance_levels(3).to_dict(
                    "records"
                ),

            "pcr":

                self.calculate_pcr()

        }

    # -------------------------------------------------------

    def retrieve(
        self,
        query
    ):

        q = query.lower()

        if (
            "pcr" in q
        ):

            return {

                "intent":

                    "pcr",

                "context":

                    self.calculate_pcr()

            }

        if (
            "support" in q
        ):

            return {

                "intent":

                    "support",

                "context":

                    self.support_levels().to_dict(
                        "records"
                    )

            }

        if (
            "resistance" in q
        ):

            return {

                "intent":

                    "resistance",

                "context":

                    self.resistance_levels().to_dict(
                        "records"
                    )

            }

        if (
            "call oi" in q
            or
            "highest call" in q
        ):

            return {

                "intent":

                    "call_oi",

                "context":

                    self.highest_call_oi().to_dict(
                        "records"
                    )

            }

        if (
            "put oi" in q
            or
            "highest put" in q
        ):

            return {

                "intent":

                    "put_oi",

                "context":

                    self.highest_put_oi().to_dict(
                        "records"
                    )

            }

        if (
            "volume" in q
        ):

            return {

                "intent":

                    "volume",

                "context": {

                    "call":

                        self.highest_call_volume().to_dict(
                            "records"
                        ),

                    "put":

                        self.highest_put_volume().to_dict(
                            "records"
                        )

                }

            }

        if (
            "atm" in q
        ):

            return {

                "intent":

                    "atm",

                "context":

                    self.atm().to_dict()

            }

        matches = re.findall(
            r"\d{4,5}",
            q
        )

        if len(matches) == 1:

            strike = int(
                matches[0]
            )

            row = self.strike(
                strike
            )

            if row is not None:

                return {

                    "intent":

                        "strike",

                    "context":

                        row.to_dict()

                }

        if len(matches) >= 2:

            strikes = list(
                map(
                    int,
                    matches
                )
            )

            return {

                "intent":

                    "compare",

                "context":

                    self.compare(
                        strikes
                    ).to_dict(
                        "records"
                    )

            }

        return {

            "intent":

                "market_structure",

            "context":

                self.market_structure()

        }


option_chain_retriever = OptionChainRetriever()