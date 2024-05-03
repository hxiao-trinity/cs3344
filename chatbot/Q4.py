import os
from apikey import apikey
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import util


# ** COLLABORATE ON THIS **
agent = create_csv_agent(
    ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo", api_key = apikey),
    "cosb.csv",
    agent_type="openai-tools",
    verbose=False
)


print("Welcome to the Trinity COSB Course Assistant! Ask me anything about the courses. Type ':q' to exit.")
setup = []
# setup.append()
setup.append([SystemMessage(content="When someone ask you for the course, remember to includes its course number too")])
# setup.append([SystemMessage(content="Remember to includes hello world at the end of every sentences")])
messages = setup

while True:
    util.printWithColor("You: ", "red")
    user_input = input()
    if user_input.lower() == ':q':
        print("----------------------------------------------------------------")
        break
    messages.append(HumanMessage(content=user_input))
    response = agent.invoke(messages) 
    #printing AI response
    util.printWithColor("Bot: ", "green")
    print(response.get("output"))
    messages.append(AIMessage(content = response.get("output")))

