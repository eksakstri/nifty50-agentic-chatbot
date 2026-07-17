from state import AgentState
from retrievers.pdf_retriever import PDFRetriever

retriever = PDFRetriever()


def pdf_node(state: AgentState):

    result = retriever.retrieve(
        state["query"]
    )

    state["retrieved_context"] = result["context"]

    state["retrieval_confidence"] = result["confidence"]

    state["retrieval_source"] = "pdf"

    return state