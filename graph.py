print("=" * 60)
print("GRAPH.PY START")
print("=" * 60)

from langgraph.graph import (
    StateGraph,
    START,
    END
)

print("[1] LangGraph imported.")

from state import AgentState
print("[2] AgentState imported.")

print("[3] Importing router...")
from agent.router_node import router_node
print("[✓] router_node imported.")

print("[4] Importing market node...")
from agent.nodes.market_node import market_node
print("[✓] market_node imported.")

print("[5] Importing option chain node...")
from agent.nodes.option_chain_node import option_chain_node
print("[✓] option_chain_node imported.")

print("[6] Importing pdf node...")
from agent.nodes.pdf_node import pdf_node
print("[✓] pdf_node imported.")

print("[7] Importing general node...")
from agent.nodes.general_node import general_node
print("[✓] general_node imported.")

print("[8] Importing answer node...")
from agent.answer_generator import answer_node
print("[✓] answer_node imported.")

print("[9] Creating StateGraph...")
builder = StateGraph(AgentState)
print("[✓] StateGraph created.")

print("[10] Adding nodes...")

builder.add_node("router", router_node)
print("    router added")

builder.add_node("market", market_node)
print("    market added")

builder.add_node("option_chain", option_chain_node)
print("    option_chain added")

builder.add_node("pdf", pdf_node)
print("    pdf added")

builder.add_node("general", general_node)
print("    general added")

builder.add_node("answer", answer_node)
print("    answer added")

print("[11] Adding entry edge...")
builder.add_edge(START, "router")

print("[12] Adding conditional routing...")

builder.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "market": "market",
        "option_chain": "option_chain",
        "pdf": "pdf",
        "general": "general"
    }
)

print("[✓] Conditional routing added.")

print("[13] Adding merge edges...")

builder.add_edge("market", "answer")
print("    market -> answer")

builder.add_edge("option_chain", "answer")
print("    option_chain -> answer")

builder.add_edge("pdf", "answer")
print("    pdf -> answer")

builder.add_edge("general", "answer")
print("    general -> answer")

print("[14] Adding END edge...")
builder.add_edge("answer", END)

print("[15] Compiling graph...")

graph = builder.compile()

print("[✓] Graph compiled successfully.")
print("=" * 60)
print("GRAPH.PY FINISHED")
print("=" * 60)
