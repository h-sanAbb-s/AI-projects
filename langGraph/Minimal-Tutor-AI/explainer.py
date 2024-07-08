from tools import tools
from agents import llm
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from prompts import explainerSystemPrompt, explainerPrompt
memory = ConversationBufferWindowMemory(
    memory_key='chatHistory',
    k=3,
    return_messages=True
)


# create our agent
explainerAgent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory
)


prompt = explainerAgent.agent.llm_chain.prompt.messages[0].prompt = explainerPrompt
print(prompt.input_variables)
# print(explainerAgent)