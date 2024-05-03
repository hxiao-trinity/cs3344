import os
from apikey import apikey
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
import util


# ** YOUR CODE HERE **

chat = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key = apikey,  temperature=0)
available_ingredients = ["1 large egg", "1 cup of light-brown sugar", "2 cup of salt"]

template = PromptTemplate(
    input_variables=['dish', 'available_ingredients'],
    template="""Given that the available ingredients are: {available_ingredients}.
                What are the ingredients and quantities we need to make {dish}?
                Additionally what is the adjusted shopping list that takes into account of the ingredients we already have?"""
)

print("Welcome to the Cooking Assistant! Tell me which dish you want to make or type 'quit' to exit.")

while True:
    util.printWithColor("You: ", "red")
    dish = input()
    if dish.lower() == 'quit':
        print("-----------------------------------------------------------------------")
        break

    # Format the prompt with the current dish and available ingredients
    prompt_text = template.format(
        dish=dish,
        available_ingredients=', '.join(available_ingredients)
    )
    
    # Send the prompt to the model
    message = [HumanMessage(content=prompt_text)]
    response = chat.invoke(message)
    
    
    # Print the bot's response (ingredient list)
    util.printWithColor("Bot: ", "green")
    print(response.content)