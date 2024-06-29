from langgraph.graph import StateGraph, END
from app import AgentCoder
from nodes import programmer, debugger, executer, tester, decide_to_end
workflow = StateGraph(AgentCoder)

# Define the nodes
workflow.add_node("programmer", programmer)  
workflow.add_node("debugger", debugger) 
workflow.add_node("executer", executer) 
workflow.add_node("tester", tester) 
#workflow.add_node('decide_to_end',decide_to_end)

# Build graph
workflow.set_entry_point("programmer")
workflow.add_edge("programmer", "tester")
workflow.add_edge("debugger", "executer")
workflow.add_edge("tester", "executer")
#workflow.add_edge("executer", "decide_to_end")

workflow.add_conditional_edges(
    "executer",
    decide_to_end,
    {
        "end": END,
        "debugger": "debugger",
    },
)

# Compile
app = workflow.compile()

