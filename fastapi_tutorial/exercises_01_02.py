"""
=============================================================
 FastAPI Student Exercises: Chapters 1 & 2
=============================================================
 INSTRUCTIONS:
 This file contains a series of exercises to test your 
 understanding of FastAPI Basics and Pydantic Models.
 
 Fill in the code below where you see `# TODO: ...`
 
 HOW TO RUN YOUR CODE:
   >>> uvicorn exercises_01_02:app --reload --port 8080
=============================================================
"""

from numpy.core.defchararray import title
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# ==============================================================
# EXERCISE 1: Application Setup
# ==============================================================
# TODO: Create a FastAPI application instance named 'app'.
# Give it a title of "Student Exercise API".
app = FastAPI(
  title = "student exercise API")# Replace 'None' with your code


# ==============================================================
# EXERCISE 2: Basic Routing
# ==============================================================
# TODO: Create a GET endpoint at the root path ("/") 
# that returns the dictionary: {"message": "Welcome to the Exercise API!"}
@app.get("/")
def welcome():
  return {"message": "Welcome to the Exercise API!"}


# ==============================================================
# EXERCISE 3: Path Parameters
# ==============================================================
# TODO: Create a GET endpoint at "/calculator/multiply/{num1}/{num2}"
# It should take two integers as path parameters and return 
# their product in a dictionary like: {"result": num1 * num2}
@app.get("/calculator/multiply/{num1}/{num2}")
def multipy(num1:int,num2:int):
  return {"result":num1 * num2}


# ==============================================================
# EXERCISE 4: Query Parameters
# ==============================================================
# TODO: Create a GET endpoint at "/users"
# It should accept two query parameters:
# 1. 'role' (string, default value "guest")
# 2. 'active' (boolean, default value True)
# Return a dictionary combining these: {"requested_role": role, "is_active": active}
@app.get("/users")
def users(role : str="guest",active : bool=True):
  return {"requested_role":role,"is_active":active}


# ==============================================================
# EXERCISE 5: Pydantic Models
# ==============================================================
# TODO: Create a Pydantic model named 'RecipeInput' that has:
# - title (string, required)
# - ingredients (list of strings, required)
# - preparation_time_minutes (integer, required)
# - is_vegetarian (boolean, optional, default False)
# class RecipeInput(BaseModel):
#   title : str
#   ingredients : list[str]
#   preparation_time_minutes : int
#   is_vegetarian : bool = False

# @app.post("/recipies")
# def create_recipe(recipe:RecipeInput):
#   return recipe


# TODO: Create a Pydantic model named 'RecipeOutput' that has:
# - id (integer, required)
# - title (string, required)
# - is_vegetarian (boolean, required)
# (Notice we are hiding the ingredients and preparation time in the output)

class RecipeInput(BaseModel):
  title : str
  ingredients : list[str]
  preparation_time_minutes : int
  is_vegetarian : bool = False


class RecipeOutput(BaseModel):
  title : str
  is_vegetarian : bool = False
  id:int 


    

# ==============================================================
# EXERCISE 6: Request and Response Models (POST)
# ==============================================================
# Fake database for recipes
recipes_db = {}
recipe_id_counter = 1


@app.post("/recipes",response_model=RecipeOutput)
def create_recipe(recipe:RecipeInput):
  global recipe_id_counter
  recipe1 = recipe.model_dump()
  recipe1["id"] = recipe_id_counter
  recipes_db[recipe_id_counter] = recipe1
  recipe_id_counter += 1
  return recipe1


# TODO: Create a POST endpoint at "/recipes"
# - It should expect the 'RecipeInput' model as the request body.
# - It should use 'RecipeOutput' as the response_model.
# - It should assign an ID using 'recipe_id_counter', save it to 'recipes_db',
#   increment the counter, and return the newly created recipe dictionary.
# @app.post("/recipes")




# ==============================================================
# EXERCISE 7: PUT (Update)
# ==============================================================
# TODO: Create a PUT endpoint at "/recipes/{recipe_id}"
# - It should take 'recipe_id' as a path parameter.
# - It should take 'RecipeInput' as the request body.
# - If the recipe_id exists in 'recipes_db', update it with the new data and return the dictionary.
# - If it doesn't exist, return {"error": "Recipe not found"}


