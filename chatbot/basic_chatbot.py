import os
from apikey import apikey

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI
import util


# ** YOUR CODE HERE**
chat = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key = apikey,  temperature=0)
messages = []

while True:
    util.printWithColor("You: ", "red")
    user_input = input()
    if user_input.lower() == 'quit':
        print("--------------------------------------------------------------------------------")
        break
    messages.append(HumanMessage(content=user_input))
    response = chat.invoke(messages)
    util.printWithColor("Bot: ", "green")
    print(response.content)
    messages.append(AIMessage(content=response.content))

# chat.invoke(messages)


