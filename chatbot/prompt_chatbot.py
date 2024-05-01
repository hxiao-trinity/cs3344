import os
from apikey import apikey
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

os.environ['OPENAI_API_KEY'] = apikey

# ** YOUR CODE HERE **

chat = ChatOpenAI(temperature=0.9)

template = PromptTemplate(
    input_variables=['dish', 'available_ingredients'],
    template="""Given that the available ingredients are: {available_ingredients}.
                What additional ingredients and quantities are needed to make {dish}?"""
)

# Initialize variables to track conversation history and available ingredients
history = []
available_ingredients = []

print("Welcome to the Cooking Assistant! Tell me which dish you want to make or type 'quit' to exit.")

while True:
    dish = input("You: ")
    if dish.lower() == 'quit':
        print("-----------------------------------------------------------------------")
        break

    # Format the prompt with the current dish and available ingredients
    prompt_text = template.format(
        dish=dish,
        available_ingredients=', '.join(available_ingredients)
    )
    
    # Send the prompt to the model
    messages = [SystemMessage(content=prompt_text)]
    response = chat.invoke(messages)
    
    # Print the bot's response (ingredient list)
    print("Bot:", response.content)