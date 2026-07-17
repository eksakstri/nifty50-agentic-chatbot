from state import AgentState

def general_node(state: AgentState):

    state["retrieved_context"] = None

    state["retrieval_source"] = "general"

    state["retrieval_confidence"] = 1.0

    return state