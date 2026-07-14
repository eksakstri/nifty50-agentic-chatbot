import time
import streamlit as st
from main import Nifty50Chatbot

st.set_page_config(
    page_title="NIFTY50 Assistant",
    page_icon="📈",
    layout="wide"
)


@st.cache_resource
def load_bot():
    return Nifty50Chatbot()


bot = load_bot()


st.title("📈 NIFTY50 Financial Assistant")

st.caption(
    "Corporate announcements • Market Snapshot • Option Chain • General Finance"
)

query = st.text_input(
    "Ask a question",
    placeholder="Why did HDFC Bank move today?"
)


if st.button("Ask"):

    if query.strip():

        start = time.time()

        with st.spinner("Thinking..."):

            result = bot.graph.invoke({

                "query": query,

                "route": None,

                "router_confidence": 0,

                "retrieval_source": None,

                "retrieved_context": None,

                "retrieval_confidence": 0,

                "answer": None

            })

        end = time.time()

        st.markdown("## Answer")

        st.write(result["answer"])

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Route",
            result["retrieval_source"]
        )

        col2.metric(
            "Confidence",
            f"{result['retrieval_confidence']:.2f}"
        )

        col3.metric(
            "Time",
            f"{end-start:.2f}s"
        )