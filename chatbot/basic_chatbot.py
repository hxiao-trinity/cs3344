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
        

    # Add the user's message to the messages list
    messages.append(HumanMessage(content=user_input))

    # Invoke the chat model with the current conversation context
    response = chat.invoke(messages)
    
    # Assuming the response is an AIMessage object, print its content
    # Note: The actual handling might need adjustments based on the implementation of `chat.invoke`
    util.printWithColor("Bot: ", "green")
    print(response.content)

    # Optionally, you can also append the AIMessage to messages if you want the bot's response
    # to also be considered as part of the context for future messages. This depends on the
    # implementation details of your ChatOpenAI class.
    messages.append(SystemMessage(content=response.content))

chat.invoke(messages)


