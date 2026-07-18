import os
import time
import traceback
import gradio as gr

print("=" * 60)
print("APP STARTING")
print("=" * 60)

print(f"Python Version: {os.sys.version}")
print(f"Current Working Directory: {os.getcwd()}")
print(f"PORT = {os.environ.get('PORT')}")
print(f"GROQ_API_KEY exists = {'GROQ_API_KEY' in os.environ}")
print()

# ------------------------------------------------------------

print("[1] Importing download_assets...")

from download_assets import download_assets

print("[2] Running download_assets()...")

try:
    download_assets()
    print("[3] download_assets() completed successfully.\n")
except Exception:
    print("[ERROR] download_assets() failed")
    traceback.print_exc()
    raise

# ------------------------------------------------------------

print("[4] Importing chatbot...")

try:
    from main import Nifty50Chatbot
    print("[5] main.py imported successfully.\n")
except Exception:
    print("[ERROR] Failed while importing main.py")
    traceback.print_exc()
    raise

# ------------------------------------------------------------

print("[6] Creating chatbot object...")

try:
    bot = Nifty50Chatbot()
    print("[7] Chatbot created successfully.\n")
except Exception:
    print("[ERROR] Failed while creating chatbot")
    traceback.print_exc()
    raise

# ------------------------------------------------------------

def ask_question(query):

    if not query.strip():
        return (
            "Please enter a question.",
            "",
            "",
            ""
        )

    print(f"\nIncoming Query: {query}")

    start = time.time()

    try:

        result = bot.graph.invoke({

            "query": query,

            "route": None,

            "router_confidence": 0,

            "retrieval_source": None,

            "retrieved_context": None,

            "retrieval_confidence": 0,

            "answer": None

        })

    except Exception:

        traceback.print_exc()

        return (
            "Internal Error",
            "",
            "",
            ""
        )

    elapsed = time.time() - start

    print(f"Query completed in {elapsed:.2f}s")

    return (
        result["answer"],
        result["retrieval_source"],
        f"{result['retrieval_confidence']:.2f}",
        f"{elapsed:.2f} sec"
    )


print("[8] Building Gradio UI...")

with gr.Blocks(
    title="NIFTY50 Financial Assistant"
) as demo:

    gr.Markdown("""
# 📈 NIFTY50 Financial Assistant

Corporate announcements • Market Snapshot • Option Chain • General Finance
""")

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

print("[9] Gradio UI built successfully.")

# ------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("LAUNCHING GRADIO")
    print("=" * 60)

    try:

        demo.launch(
            server_name="0.0.0.0",
            server_port=int(os.environ.get("PORT", 7860)),
            show_error=True
        )

        print("Gradio exited normally.")

    except Exception:

        print("[ERROR] demo.launch() failed")

        traceback.print_exc()

        raise
