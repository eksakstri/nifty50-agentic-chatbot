from state import GraphState
from agent.router import router


def router_node(state: GraphState):

    result = router.route(
        state["query"]
    )

    state["route"] = result["route"]

    state["router_confidence"] = result["confidence"]

    state["requires_llm"] = result["requires_llm"]

    return state