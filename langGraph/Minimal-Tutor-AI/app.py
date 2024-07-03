from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, Any, Dict, Optional, Sequence, TypedDict, List, Tuple
from langchain_core.messages import BaseMessage
import operator

from executable import router, planner, explainer, contextData


class AgentTutor(TypedDict):
    query: str
    plan: str
    route: str
    context: str
    response: str
    chatHistory: Annotated[Sequence[BaseMessage], operator.add]

workflow = StateGraph(AgentTutor)
workflow.add_node("router", router)
workflow.add_node("getContext", contextData)
workflow.add_node("planner", planner)
workflow.add_node("explainer", explainer)

workflow.set_entry_point("router")
workflow.add_edge("getContext", "planner")
workflow.add_edge("planner", "explainer")

workflow.add_conditional_edges(
    "router",
    lambda input_data: input_data['route'],  # This lambda extracts the route key
    {"newConcept": "getContext", "continuation": "explainer"},
)

workflow.add_edge("explainer", END)


app = workflow.compile()


