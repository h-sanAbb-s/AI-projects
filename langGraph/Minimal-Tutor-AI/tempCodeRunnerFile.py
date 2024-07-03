from app import app

chatHistory = []
response = "Hello. I am your tutor. How may I help you?"
while True:
  print(response)
  chatHistory.append({"role":"assistant","content":response})
  query = input("Enter your query: ")
  if query == "exit":
    break
  response = app.invoke({"query":query, "chatHistory":chatHistory})["response"]
  chatHistory.append({"role":"user","content":query})