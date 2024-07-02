from langchain_openai import ChatOpenAI
from langchain.chains.openai_functions import create_structured_output_runnable
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.llms import HuggingFaceEndpoint
from prompts import routerPrompt, plannerPrompt, explainerPrompt
import os
from dotenv import load_dotenv
load_dotenv(r'langGraph\Minimal-Tutor-AI\.env.local')

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = 'gpt-3.5-turbo')
# llm = HuggingFaceEndpoint(
#         huggingfacehub_api_token=HUGGINGFACE_API_KEY,
#         repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1",
#         temperature = 0.5,
#         model_kwargs={"max_length": 200}
#         )
class Router(BaseModel):

    route: str = Field(
        description="continuation or newConcept"
    )

routerAgent = create_structured_output_runnable(
    Router, llm, routerPrompt
)


class planner(BaseModel):

    plan: str = Field(
        description="A step by step guidelines for teaching a new concept. could of varying length"
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


