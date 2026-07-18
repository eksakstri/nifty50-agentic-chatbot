print("=" * 60)
print("PDF_NODE.PY START")
print("=" * 60)

print("[PDF NODE] Importing AgentState...")
from state import AgentState
print("[✓] AgentState imported.")

print("[PDF NODE] Importing PDFRetriever...")
from retrievers.pdf_retriever import PDFRetriever
print("[✓] PDFRetriever class imported.")

print("[PDF NODE] Creating PDFRetriever...")

try:
    retriever = PDFRetriever()
    print("[✓] PDFRetriever created successfully.")
except Exception as e:
    import traceback

    print("[✗] Failed while creating PDFRetriever!")
    print(type(e).__name__)
    print(e)
    traceback.print_exc()

    raise

print("=" * 60)
print("PDF_NODE.PY READY")
print("=" * 60)


def pdf_node(state: AgentState):

    print("[PDF NODE] pdf_node() called")
    print(f"[PDF NODE] Query: {state['query']}")

    try:

        result = retriever.retrieve(
            state["query"]
        )

        print("[✓] Retrieval successful.")

    except Exception as e:

        import traceback

        print("[✗] Retrieval failed!")
        print(type(e).__name__)
        print(e)
        traceback.print_exc()

        raise

    state["retrieved_context"] = result["context"]

    state["retrieval_confidence"] = result["confidence"]

    state["retrieval_source"] = "pdf"

    print("[✓] State updated.")

    return state
