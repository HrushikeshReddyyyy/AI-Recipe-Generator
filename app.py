import streamlit as st
import json
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import os


# Set your Groq API key here
os.environ["GROQ_API_KEY"] = "YOUR_API_KEY"

# Initialize Groq client
llm = ChatGroq()

# Define our database of recipes
recipes = [
    {
        "name": "Pasta Carbonara",
        "ingredients": ["pasta", "eggs", "bacon", "parmesan cheese", "black pepper"],
        "cuisine": "Italian",
        "difficulty": "Medium",
        "dietary_restrictions": ["contains_gluten", "contains_dairy", "contains_meat"]
    },
    {
        "name": "Vegetable Stir Fry",
        "ingredients": ["rice", "mixed vegetables", "soy sauce", "garlic", "ginger"],
        "cuisine": "Asian",
        "difficulty": "Easy",
        "dietary_restrictions": ["vegan", "gluten_free"]
    },
    {
        "name": "Chicken Curry",
        "ingredients": ["chicken", "curry powder", "coconut milk", "onion", "rice"],
        "cuisine": "Indian",
        "difficulty": "Medium",
        "dietary_restrictions": ["gluten_free"]
    },
    {
        "name": "Greek Salad",
        "ingredients": ["cucumber", "tomato", "feta cheese", "olives", "olive oil"],
        "cuisine": "Mediterranean",
        "difficulty": "Easy",
        "dietary_restrictions": ["vegetarian", "gluten_free"]
    },
    {
        "name": "Beef Tacos",
        "ingredients": ["beef", "tortillas", "lettuce", "tomato", "cheese"],
        "cuisine": "Mexican",
        "difficulty": "Easy",
        "dietary_restrictions": ["contains_gluten", "contains_dairy", "contains_meat"]
    }
]

# Define our database of cuisines (for validation)
cuisines = list(set(recipe["cuisine"] for recipe in recipes))

def generate_recipe_with_groq(ingredients, cuisine):
    prompt = f"""Given the following recipe database:

{json.dumps(recipes, indent=2)}

Generate a recipe based on the following ingredients and cuisine:

Ingredients: {', '.join(ingredients)}
Cuisine: {cuisine}

IMPORTANT: You must ONLY use the ingredients listed above. Do not add any additional ingredients that are not in this list. Be creative with the given ingredients to make a dish that fits the cuisine.

Please provide the recipe in the following format:
Recipe Name:
Ingredients:
- [List of ingredients with quantities, ONLY from the provided list]
Instructions:
1. [Step-by-step instructions using ONLY the listed ingredients]

Cooking Time:
Difficulty:
Dietary Notes:
"""

    messages = [HumanMessage(content=prompt)]
    chat_completion = llm(messages)
    return chat_completion.content

def validate_recipe(recipe, given_ingredients):
    given_ingredients = [ing.lower() for ing in given_ingredients]
    recipe_ingredients = []
    for line in recipe.split('\n'):
        if line.strip().startswith('-'):
            ingredient = line.split('-')[1].strip().split(',')[0].split('(')[0].strip().lower()
            recipe_ingredients.append(ingredient)
    
    invalid_ingredients = [ing for ing in recipe_ingredients if ing not in given_ingredients]
    return invalid_ingredients

def main():
    st.title("AI Recipe Generator")
    
    ingredients = st.text_input("Enter the ingredients you have (comma-separated):").lower().split(',')
    ingredients = [i.strip() for i in ingredients]
    
    cuisine = st.selectbox("Choose a cuisine:", cuisines)
    
    if st.button("Generate Recipe"):
        if ingredients and cuisine:
            with st.spinner("Generating recipe..."):
                recipe = generate_recipe_with_groq(ingredients, cuisine)
            
            invalid_ingredients = validate_recipe(recipe, ingredients)
            
            if invalid_ingredients:
                st.warning(f"The generated recipe contains ingredients not in your list: {', '.join(invalid_ingredients)}")
                st.write("You may need to substitute or omit these ingredients.")
            
            st.subheader("Here's your recipe:")
            st.write(recipe)
        else:
            st.error("Please enter ingredients and select a cuisine.")

if __name__ == "__main__":
    main()
