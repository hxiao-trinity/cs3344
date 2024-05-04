import os
from apikey import apikey
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import util

#Pathway list
pathways = ["HU: Humanities", "CE: Creative Expression", "SBS: Social/Behavioral Sciences", "NS: Natural Sciences", "QR: Quantitative Reasoning"
, "WC: Written Communication", "OVC: Oral and Visual Communication", "DL: Digital Literacy", "GA: Global Awareness", "UD: Understanding Diversity",
"FL: Foreign Language", "HP: Historical Perspective", "FE: Fitness Education"]

#AI set up
agent = create_csv_agent(
    ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo", api_key = apikey),
    "cosb.csv",
    agent_type="openai-tools",
    verbose=False
)


print("Welcome to the Trinity COSB Course Assistant! Ask me anything about the courses. Type ':q' to exit.")
setup = []
setup.append(SystemMessage(content="When someone ask you for the course, give its course as well as associated course title"))
setup.append(SystemMessage(content="Pathways are requirements Here is the list of pathway courses and their names: " + ", ".join(pathways)))
setup.append(SystemMessage(content="If a course can double dip, it can satisfy two or more pathways, more specifically, its pathway description would have a hyphen"))
# setup.append([SystemMessage(content="Remember to includes hello world at the end of every sentences")])
messages = setup

#Chatting
while True:
    util.printWithColor("You: ", "red")
    user_input = input()
    if user_input.lower() == 'quit':
        print("----------------------------------------------------------------")
        break
    messages.append(HumanMessage(content=user_input))
    response = agent.invoke(messages) 
    #printing AI response
    util.printWithColor("Bot: ", "green")
    print(response.get("output"))
    messages.append(AIMessage(content = response.get("output")))

