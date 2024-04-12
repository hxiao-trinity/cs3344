import os
from apikey import apikey
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent

os.environ['OPENAI_API_KEY'] = apikey

# ** YOUR CODE HERE **