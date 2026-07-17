import time
import gradio as gr
from download_assets import download_assets
download_assets()

from main import Nifty50Chatbot

print("Loading chatbot...")
bot = Nifty50Chatbot()
print("Chatbot loaded.")


def ask_question(query):

    if not query.strip():
        return (
            "Please enter a question.",
            "",
            "",
            ""
        )

    start = time.time()

    result = bot.graph.invoke({

        "query": query,

        "route": None,

        "router_confidence": 0,

        "retrieval_source": None,

        "retrieved_context": None,

        "retrieval_confidence": 0,

        "answer": None

    })

    elapsed = time.time() - start

    answer = result["answer"]

    route = result["retrieval_source"]

    confidence = f"{result['retrieval_confidence']:.2f}"

    runtime = f"{elapsed:.2f} sec"

    return (
        answer,
        route,
        confidence,
        runtime
    )


with gr.Blocks(
    title="NIFTY50 Financial Assistant"
) as demo:

    gr.Markdown(
        """
# 📈 NIFTY50 Financial Assistant

Corporate announcements • Market Snapshot • Option Chain • General Finance
"""
    )

    query = gr.Textbox(
        label="Ask a Question",
        placeholder="Why did HDFC Bank move today?"
    )

    ask_btn = gr.Button(
        "Ask",
        variant="primary"
    )

    gr.Markdown("## Answer")

    answer = gr.Markdown()

    with gr.Row():

        route = gr.Textbox(
            label="Route",
            interactive=False
        )

        confidence = gr.Textbox(
            label="Confidence",
            interactive=False
        )

        runtime = gr.Textbox(
            label="Response Time",
            interactive=False
        )

    ask_btn.click(

        fn=ask_question,

        inputs=query,

        outputs=[
            answer,
            route,
            confidence,
            runtime
        ]

    )

    query.submit(

        fn=ask_question,

        inputs=query,

        outputs=[
            answer,
            route,
            confidence,
            runtime
        ]

    )


if __name__ == "__main__":

    demo.launch()