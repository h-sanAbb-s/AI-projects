from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from agents import superVisorAgent, plannerAgent, explainerAgent
from tools import tools

def getUserData():
    weakpoints = """
    My weakpoints are working with reactions, specially one that involves a catalyst or oxidizing or reducing agents.
    """
    sessionHistory = """
    Hasan learned about 
    1. Oxidizing agents
    2. Reducing agents
    3. Redox reactions
    4. Some commonly used oxiding and reducing agents
    Personal Remarks
    1. Learned the concept and theory behind it effectively. But had some issues when learning the reactions
    """
    return {"weakPoints":weakpoints, "sessionHistory":sessionHistory}

def planner(state):
    """
    For planning on how to handle the current ongoing session
    """
    userData = getUserData()
    weakpoints = userData["weakPoints"]
    sessionHistory = userData["sessionHistory"]
    chatHistory = state["chatHistory"]
    response = plannerAgent.invoke({"chatHistory":chatHistory,"sessionHistory":sessionHistory,"weakPoints":weakpoints})
    print("Planner Returned: ", response)
    return {"plan":response.plan, "tip":response.tip}


def superVisor(state):
    """
    for supervising the planner and explainer on how and when to act
    """
    chatHistory = state["chatHistory"]
    if state["plan"] == None:
        plan = "No plan has been made yet. YOu need to command a replan NOW"
    else:
        plan = state["plan"]

    response = superVisorAgent.invoke({"chatHistory":chatHistory,"plan":plan}) 
    print("SuperVisor Returned: ", response.route)
    return {"route":response.route}

def explainer(state):
    """
    for explaining in an interactive, friendly and step by step way. 
    """
    plan = state["plan"]
    chatHistory = state["chatHistory"]
    tip = state["tip"]
    response = explainerAgent.invoke({"chatHistory":chatHistory,"plan":plan,"tip":tip, "input":chatHistory[-1]["content"]})
    return {"response":response.response}