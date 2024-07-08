from langchain.chains.openai_functions import create_structured_output_runnable
from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain import PromptTemplate
# from langchain.chains import LLMMathChain, LLMChain
from langchain_openai import ChatOpenAI
# from tools import tools
from prompts import superVisorPrompt, explainerPrompt, plannerPrompt
import os
from dotenv import load_dotenv
load_dotenv(r"langGraph\Minimal-Tutor-AI\.env.local")
os.environ['OPENAI_API_KEY']  = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model = 'gpt-3.5-turbo')

######################################################
class superVisor(BaseModel):

    route: str = Field(
        description="replan or continue"
    )

superVisorAgent = create_structured_output_runnable(
    superVisor, llm, superVisorPrompt)

#######################################################
class planner(BaseModel):

    plan: str = Field(
        description="A step by step plan"
    )
    tip: str = Field(
        description="A small list of tips addressing teaching style and user specific needs"
    )
plannerAgent = create_structured_output_runnable(
    planner, llm, plannerPrompt
)

########################################################
# agent = create_react_agent(llm, tools, explainerPrompt)
# explainerAgent = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
# llmMath = LLMMathChain(llm=llm)
class explainer(BaseModel):

    response: str = Field(
        description="Explaing concept, solving problem or an advice"
    )

explainerAgent = create_structured_output_runnable(
    explainer, llm, explainerPrompt
)

