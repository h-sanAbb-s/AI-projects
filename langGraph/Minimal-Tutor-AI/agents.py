from langchain_openai import ChatOpenAI
from langchain.chains.openai_functions import create_structured_output_runnable
from langchain_core.pydantic_v1 import BaseModel, Field
from prompts import routerPrompt, explainerPrompt, plannerPrompt
import os
from dotenv import load_dotenv
load_dotenv(r"langGraph\Minimal-Tutor-AI\.env.local")
os.environ['OPENAI_API_KEY']  = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model = 'gpt-3.5-turbo')

class Router(BaseModel):

    route: str = Field(
        description="continuation or newConcept"
    )

routerAgent = create_structured_output_runnable(
    Router, llm, routerPrompt
)


class planner(BaseModel):

    plan: str = Field(
        description="A step by step guidelines for teaching a new concept"
    )

plannerAgent = create_structured_output_runnable(
    planner, llm, plannerPrompt
)

class explainer(BaseModel):

    response: str = Field(
        description="a response that follows the plan and answers the query in a friendly, interactive and professional way"
    )

explainerAgent = create_structured_output_runnable(
    explainer, llm, explainerPrompt
)