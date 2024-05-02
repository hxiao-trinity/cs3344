import os
from apikey import apikey
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent

os.environ['OPENAI_API_KEY'] = apikey

# ** YOUR CODE HERE **
agent = create_csv_agent(
    ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo"),
    "old_cosb.csv",
    agent_type="openai-tools",
    verbose=True
)

print("Welcome to the Trinity COSB Course Assistant! Ask me anything about the courses. Type 'quit' to exit.")


while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        print("----------------------------------------------------------------")
        break
    agent.run("ssssssss")
    messages = [HumanMessage(content=user_input)]
    response = agent.invoke(messages) 
