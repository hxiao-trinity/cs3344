import os
from apikey import apikey
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

import util
import copy

#Pathway list
pathways = ["HU: Humanities", "CE: Creative Expression", "SBS: Social/Behavioral Sciences", "NS: Natural Sciences", "QR: Quantitative Reasoning"
, "WC: Written Communication", "OVC: Oral and Visual Communication", "DL: Digital Literacy", "GA: Global Awareness", "UD: Understanding Diversity",
"FL: Foreign Language", "HP: Historical Perspective", "FE: Fitness Education"]

#Comsci website
loader = WebBaseLoader("https://www.trinity.edu/academics/cosb/csci/computer-science-bs#requirements")
data = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(openai_api_key=apikey))
retriever = vectorstore.as_retriever(k=4)
docs = retriever.invoke("What is the CS major requirement")
print(docs)

#AI set up
agent = create_csv_agent(
    ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo-0125", api_key = apikey),
    "cosb.csv",
    agent_type="openai-tools",
    verbose=False
)

#set up knowledge
setupStr = ""
setupStr = setupStr + "You are a course assistant chatbot trained to provide information about courses at Trinity Course of Study Bulletin (COSB)."
setupStr = setupStr + "When someone ask you about a course, give its course as well as associated course title"
setupStr = setupStr + "Here are some knowledge on graduation requirements: You must take one course in each pathway to graduate. Here is the list of pathway courses and their names: " + ", ".join(pathways)
setupStr = setupStr + "If a course can double dip, it can satisfy two or more pathways, more specifically, its pathway description would have a hyphen"
setupStr = setupStr + "Be positive and supportive"

chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content=(setupStr)),
    SystemMessage(content="Answer information about the computer science (CS) major with this requirement sepcification:\n\n{context}"),
    HumanMessagePromptTemplate.from_template("{text}")
  ]
)

history = []
# Memory handling
def brute_memory_trim():
  global history
  if len(history) > 10:
    history = history[:len(setup)] + history[len(setup) + 2:]

def summarize_memory_trim():
  global history
  if len(history) > 10:
    history.append(HumanMessage(content="""Distill the above chat history into a single summary message. 
    Include as many specific details as you can, especially details about the user information."""))
    summary = agent.invoke(history).get("output") 
    history = [SystemMessage(content=summary)]

print("Welcome to the Trinity COSB Course Assistant! Ask me anything about the courses. Type 'quit' to exit.")
#Chatting
while True:
    util.printWithColor("You: ", "red")
    user_input = input()
    if user_input.lower() == 'quit':
        print("----------------------------------------------------------------")
        break

    # print(chat_template.format_messages(text=user_input))
    response = agent.invoke(history + chat_template.format_messages(text=user_input, context=docs))
    # response = agent.invoke(history + [HumanMessage(content=prompt_text)]) 

    #printing AI response
    util.printWithColor("Bot: ", "green")
    print(response.get("output"))

    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content = response.get("output")))
    # brute_memoryTrim()
    # if len(history) > 10:
    #   print(history)
    summarize_memory_trim()






