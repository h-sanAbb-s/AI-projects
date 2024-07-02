import os
from langchain_community.retrievers import WikipediaRetriever
from duckduckgo_search import DDGS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.huggingface import HuggingFaceInferenceAPI
from llama_index.core import Settings
from agents import routerAgent, plannerAgent, explainerAgent
from dotenv import load_dotenv
load_dotenv(r'langGraph\Minimal-Tutor-AI\.env.local')
embedding_api_key = os.getenv('EMBEDDINGS_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
CONTEXT = None
PLAN = None

embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=embedding_api_key,
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)

llm = HuggingFaceInferenceAPI(
    model_name="mistralai/Mistral-7B-Instruct-v0.3",
    token=HUGGINGFACE_API_KEY
)

Settings.llm = llm
Settings.embed_model = embeddings

def router(state):
    query = state['query']
    route = routerAgent.invoke(query)
    print(route.route)
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

query_engine = setup_query_engine(r"langGraph\Minimal-Tutor-AI\data")

def contextData(state):
    """
    Perform a web search using Wikipedia, DuckDuckGo, and a local vector store.

    Args:
    query (str): The search query.

    Returns:
    dict: A dictionary containing Wikipedia, DuckDuckGo, and vector store search results.
    """
    query = state["query"]
    retriever = WikipediaRetriever(top_k_results=1, doc_content_chars_max=100)

    try:
        wiki_result = retriever.invoke(query)
    except:
        wiki_result = "No relevant information found on Wikipedia."

    # DuckDuckGo search
    try:
        with DDGS() as ddgs:
            ddg_results = [r for r in ddgs.text(query, max_results=3)]
        ddg_result = "\n".join([f"Title: {r['title']}\nSnippet: {r['body']}" for r in ddg_results])

    except Exception as e:
        ddg_result = f"An unexpected error occurred during DuckDuckGo search. Error: {str(e)}"
    # Vector store query
    vector_store_result = str(query_engine.query(query))
    print(wiki_result)
    print(ddg_result)
    print(vector_store_result)
    data = {
        "wikiPedia": wiki_result,
        "duckduckGo": ddg_result,
        "userData": vector_store_result
    }
    context =  f"""User DATA (HIGHES PRIORITY FOR REFERENCE): {data['userData']}\nSecondary Sources from internet:{data['duckduckGo']}\n{data['wikiPedia']}"""
    print(context)
    return context
    
def planner(state):
    query = state['query']
    context = state['context']
    plan = plannerAgent.invoke({"query":query, "context":context})
    print(plan.plan)
    return plan.plan

def explainer(state):
    query = state['query']
    if state['context']:
        context = state['context']
        plan = state['plan']
        CONTEXT = context
        PLAN = plan
    else:
        context = CONTEXT
        plan = PLAN

    chatHistory = state['chatHistory']

    response = explainerAgent.invoke({"query":query, "context":context, "chatHistory":chatHistory,"plan":plan})
    print(response.response)
    return response.response
