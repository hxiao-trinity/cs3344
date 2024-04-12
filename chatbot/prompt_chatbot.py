import os
from apikey import apikey
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

os.environ['OPENAI_API_KEY'] = apikey

# ** YOUR CODE HERE **
