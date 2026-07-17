from state import AgentState
from retrievers.option_chain_retriever import OptionChainRetriever

retriever = OptionChainRetriever()


def option_chain_node(state: AgentState):

    result = retriever.retrieve(
        state["query"]
    )

    state["retrieved_context"] = result

    state["retrieval_source"] = "option_chain"

    state["retrieval_confidence"] = 1.0

    return state