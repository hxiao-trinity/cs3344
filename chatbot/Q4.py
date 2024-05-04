import os
from apikey import apikey
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import util
import copy

#Pathway list
pathways = ["HU: Humanities", "CE: Creative Expression", "SBS: Social/Behavioral Sciences", "NS: Natural Sciences", "QR: Quantitative Reasoning"
, "WC: Written Communication", "OVC: Oral and Visual Communication", "DL: Digital Literacy", "GA: Global Awareness", "UD: Understanding Diversity",
"FL: Foreign Language", "HP: Historical Perspective", "FE: Fitness Education"]

#AI set up
agent = create_csv_agent(
    ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo-0125", api_key = apikey),
    "cosb.csv",
    agent_type="openai-tools",
    verbose=False
)
print("Welcome to the Trinity COSB Course Assistant! Ask me anything about the courses. Type ':q' to exit.")
# setup = []
setupStr = ""
# purpose
setupStr = setupStr + "You are a course assistant chatbot trained to provide information about courses at Trinity Course of Study Bulletin (COSB)."
# how to respond
setupStr = setupStr + "When someone ask you about a course, give its course as well as associated course title"
setupStr = setupStr + "Pathways are requirements, you must take one course in each pathway to graduate. Here is the list of pathway courses and their names: " + ", ".join(pathways)
setupStr = setupStr + "If a course can double dip, it can satisfy two or more pathways, more specifically, its pathway description would have a hyphen"
setupStr = setupStr + "Be positive and supportive"
# setup.append(SystemMessage(content=setupStr))

messages = []
template = PromptTemplate(
    input_variables=['input'],
    template= "You are a course assistant chatbot trained to provide information about courses at Trinity Course of Study Bulletin (COSB). " + "Answer this user's message: {input}"
)

# Memory handling
# messages = copy.deepcopy(setup)
def brute_memory_trim():
  global messages
  if len(messages) > (len(setup) + 12):
    messages = messages[:len(setup)] + messages[len(setup) + 2:]

def summarize_memory_trim():
  global messages
  if len(messages) > 10:
    messages.append(HumanMessage(content="Distill the above chat messages into a single summary message. Include as many specific details as you can. Especially details about the user information."))
    summary = agent.invoke(messages).get("output") 
    messages = messages[:len(setup)]
    messages.append(SystemMessage(content=summary))
    print(messages)

#Chatting
while True:
    util.printWithColor("You: ", "red")
    user_input = input()
    if user_input.lower() == 'quit':
        print("----------------------------------------------------------------")
        break
    # messages.append(HumanMessage(content=user_input))

    prompt_text = template.format(
        input=user_input
    )

    response = agent.invoke(messages + [HumanMessage(content=prompt_text)]) 

    #printing AI response
    util.printWithColor("Bot: ", "green")
    print(response.get("output"))

    messages.append(HumanMessage(content=user_input))
    messages.append(AIMessage(content = response.get("output")))
    # brute_memoryTrim()
    if len(messages) > 10:
      print(messages)
    summarize_memory_trim()






