from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import langchain_community.document_loaders as doc_loaders
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv(r"langGraph\Minimal-Tutor-AI\.env.local")
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = 'gpt-3.5-turbo')
tavily_retriever = TavilySearchAPIRetriever(
    api_key=os.getenv("TAVILY_API_KEY"),
    k=3,
)
search = DuckDuckGoSearchRun()


def initialize_vector_store():
    index_name = "faiss_index_metallica"
    embeddings = HuggingFaceInferenceAPIEmbeddings(
        api_key=os.getenv("EMBEDDINGS_API_KEY"),
        model_name="sentence-transformers/all-MiniLM-l6-v2",
    )
    if os.path.exists(index_name):
        print("Loading existing vector store...")
        return FAISS.load_local(index_name, embeddings, allow_dangerous_deserialization=True)
    print("Creating new vector store...")
    loader = doc_loaders.TextLoader(r"langGraph\Minimal-Tutor-AI\data\new_chapter.txt")  
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20,
        length_function=len,
    )
    docs = text_splitter.split_documents(documents)
    library = FAISS.from_documents(docs, embeddings)
    library.save_local(index_name)
    return library
vector_store = initialize_vector_store()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever())

def vector_store_search(query):
    try:
        result = qa.invoke(query)
        return result['result'] if 'result' in result else "No relevant information found in the vector store."
    except Exception as e:
        return f"An error occurred during Vector Store search: {str(e)}"
    

tools = [
    Tool(
        name='TavilySearch',
        func=tavily_retriever.invoke,
        description="use this to search for factual information"
    ),
    Tool(
        name='DuckDuckGoSearch',
        func=search.run,
        description="Use this to search for useful examples."
    ),
    Tool(
        name='VectorStoreSearch',
        func=vector_store_search,
        description="Use this to search for content from user uploaded book. Use this more often."
    )
]
