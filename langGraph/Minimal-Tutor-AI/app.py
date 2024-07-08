from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, Any, Dict, Optional, Sequence, TypedDict, List, Tuple
from langchain_core.messages import BaseMessage
from executable import planner, superVisor, explainer
import operator

class AgentTutor(TypedDict):
    plan: str
    tip: str
    route: str
    response: str
    chatHistory: Annotated[Sequence[BaseMessage], operator.add]

workflow = StateGraph(AgentTutor)
workflow.add_node("superVisor", superVisor)
workflow.add_node("planner", planner)
workflow.add_node("explainer", explainer)


workflow.set_entry_point("superVisor")
workflow.add_edge("planner", "explainer")
workflow.add_conditional_edges(
    "superVisor",
    lambda input_data: input_data['route'],
    {"replan": "planner", "continue":"explainer"},
)

workflow.add_edge("explainer", END)


app = workflow.compile()