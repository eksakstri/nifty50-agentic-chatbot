from state import AgentState
from agent.router import router

def router_node(state: AgentState):

    result = router.route(
        state["query"]
    )

    state["route"] = result["route"]

    state["router_confidence"] = result["confidence"]

    state["requires_llm"] = result["requires_llm"]

    print("=" * 60)
    print("ROUTER")
    print("Query:", state["query"])
    print("Route:", state["route"])
    print("Confidence:", state.get("router_confidence"))
    print("=" * 60)

    return state
