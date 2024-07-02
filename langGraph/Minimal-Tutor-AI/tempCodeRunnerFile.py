from agents import routerAgent, plannerAgent, explainerAgent
from executable import router, planner, explainer, contextData

chatHistory = [
    {"role":"user", "content":"What is the best os for me?"},
    {"role":"assistant","content":"It truly depends on what you want the most. Speed? Security? it depends"}
    ]

query = "OK. What are different types of OS?"

plan = """
•  Conductor Chaos: Explain a computer is like an orchestra needing a conductor. The OS is the conductor, telling each part (keyboard, mouse) what to do.
•  Click & Play Magic: Show them their device and ask, "See how we click icons or tap apps? That's the OS helping us use games and videos!"

•  Boss Buddies: Point out their device's OS (Windows, macOS, Android, iOS) and say, "These are different bosses (OS) for different devices, but they all help us play and work!"
"""
context = """
Here's some information about different types of OS: 

Windows: The most popular OS for personal computers, known for its user-friendly interface.
macOS: The operating system used on Apple computers, known for its sleek design and tight integration with Apple hardware.
Android: The dominant OS for smartphones and tablets, known for its openness and wide variety of apps.
iOS: The OS used exclusively on iPhones and iPads, known for its smooth user experience and tight integration with Apple products.unity (used only on iPhones and iPads). It's known for its tight integration with Apple devices for a smooth experience. Imagine it as a private playground with everything perfectly designed to work together (Apple devices and apps).
"""

# response = explainerAgent.invoke({"query":query,"chatHistory":chatHistory, "context":context, "plan":plan})
# print(response)
docs = contextData(query)


docs