from langgraph.graph import (
    StateGraph,
    START,
    END
)

from state import AgentState

from agent.router_node import router_node

from agent.nodes.market_node import market_node
from agent.nodes.option_chain_node import option_chain_node
from agent.nodes.pdf_node import pdf_node
from agent.nodes.general_node import general_node

from agent.answer_generator import answer_node


# =====================================================
# Build Graph
# =====================================================

builder = StateGraph(AgentState)


# =====================================================
# Nodes
# =====================================================

builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "market",
    market_node
)

builder.add_node(
    "option_chain",
    option_chain_node
)

builder.add_node(
    "pdf",
    pdf_node
)

builder.add_node(
    "general",
    general_node
)

builder.add_node(
    "answer",
    answer_node)


# =====================================================
# Entry
# =====================================================

builder.add_edge(
    START,
    "router"
)


# =====================================================
# Conditional Routing
# =====================================================

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


# =====================================================
# Merge
# =====================================================

builder.add_edge(
    "market",
    "answer"
)

builder.add_edge(
    "option_chain",
    "answer"
)

builder.add_edge(
    "pdf",
    "answer"
)

builder.add_edge(
    "general",
    "answer"
)


# =====================================================
# Finish
# =====================================================

builder.add_edge(
    "answer",
    END
)


graph = builder.compile()