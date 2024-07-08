from app import app
response = {"response": "Hello. I am your AI tutor. How may i help you?"}
chatHistory = []
while True:
    print(response["response"])
    chatHistory.append({"role":"assistant","content":response["response"]})
    question = input("query: ")
    chatHistory.append({"role":"user","content":question})
    response = app.invoke({"chatHistory":chatHistory})
    print(type(response))
    

