from state import AgentState
from retrievers.market_retriever import MarketRetriever

retriever = MarketRetriever()

def market_node(state: AgentState):

    result = retriever.retrieve(
        state["query"]
    )

    state["retrieved_context"] = result

    state["retrieval_source"] = "market"

    state["retrieval_confidence"] = 1.0

    return state