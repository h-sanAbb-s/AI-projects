import os
from langchain_community.retrievers import WikipediaRetriever
from duckduckgo_search import DDGS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.core import Settings
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchRun

from agents import routerAgent, plannerAgent, explainerAgent
from dotenv import load_dotenv
load_dotenv(r'langGraph\Minimal-Tutor-AI\.env.local')

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.getenv('EMBEDDINGS_API_KEY'),
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)

llm = HuggingFaceInferenceAPI(
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    token=os.getenv('HUGGINGFACE_API_KEY')
)


Settings.llm = llm
Settings.embed_model = embeddings

def router(state):
    print("\nRouting... ")
    query = state['query']
    chatHistory = state['chatHistory']
    route = routerAgent.invoke({"query":query,"chatHistory":chatHistory})
    return {"route":route.route}

def setup_query_engine(path):
    """
    Set up or load the vector store index and return a query engine.
    """
    PERSIST_DIR = "VectorIndex"
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader(path).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    retriever = VectorIndexRetriever(index=index, similarity_top_k=3)
    return RetrieverQueryEngine(retriever=retriever)


def contextData(state):
    print("\nFinding context ...")
    """
    Perform a web search using Wikipedia, DuckDuckGo, and a local vector store.
    Args:
    query (str): The search query.
    Returns:
    str: A string containing combined search results from Wikipedia, DuckDuckGo, and vector store.
    """
    query = state["query"]
    # Wikipedia search
    wikipedia = WikipediaAPIWrapper(top_k_results = 1, doc_content_chars_max = 500)
    search = DuckDuckGoSearchRun()
    try:
        wiki_result = wikipedia.run(query)
    except Exception as e:
        wiki_result = f"An error occurred during Wikipedia search: {str(e)}"
    # DuckDuckGo search
    try:
        ddg_result = search.run(query)
    except Exception as e:
        ddg_result = f"An error occurred during DuckDuckGo search: {str(e)}"
    # Vector store search (placeholder)
    try:
        query_engine = setup_query_engine(r"langGraph\Minimal-Tutor-AI\data")
        vector_store_result = str(query_engine.get_relevant_documents(query))
    except Exception as e:
        vector_store_result = f"An error occurred during vector store search: {str(e)}"
    data = {
        "wikiPedia": wiki_result,
        "duckduckGo": ddg_result,
        "userData": vector_store_result
    }
    context = f"""User DATA (HIGHEST PRIORITY FOR REFERENCE): {data['userData']}\nSecondary Sources from internet:\nDUCKDUCKGO SAYS: {data['duckduckGo']}\nWIKIPEDIA SAYS: {data['wikiPedia']}"""
    return {"context":context}

def planner(state):
    print("\nPLANNING Ahead ...")
    query = state['query']
    context = state['tableOfContent']
    chatHistory = state['chatHistory']
    plan = plannerAgent.invoke({"query":query, "context":context, "chatHistory":chatHistory})
    return {"plan":plan.plan}

def explainer(state):
    print("\nResponding...\n")
    query = state['query']
    route = state['route']
    context = state["context"]
    plan = state['plan']
    chatHistory = state['chatHistory']

    response = explainerAgent.invoke({"query":query, "context":context, "chatHistory":chatHistory,"plan":plan})
    return {"response":response.response}
