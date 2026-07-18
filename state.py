from typing import TypedDict, Optional, Any


class AgentState(TypedDict):
    query: str

    route: Optional[str]
    router_confidence: Optional[float]

    retrieval_source: Optional[str]
    retrieved_context: Optional[Any]
    retrieval_confidence: Optional[float]

    answer: Optional[str]
