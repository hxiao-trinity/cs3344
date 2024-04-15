import os
from apikey import apikey
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
import util

os.environ['OPENAI_API_KEY'] = apikey

# ** YOUR CODE HERE**
chat = ChatOpenAI(temperature=1)
history = []
messages = []

while True:
    util.printWithColor("You: ", "red")
    user_input = input("")
    if user_input.lower() == 'quit':
        print("--------------------------------------------------------------------------------")
        break
    messages.append(HumanMessage(content=user_input))
    response = chat.invoke(messages)
    util.printWithColor("Bot: ", "green")
    print(response.content)
    messages.append(SystemMessage(content=response.content))

chat.invoke(messages)


