import pandas as pd
import datetime 
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
import streamlit as st

# 1. Initialize the client by api key: 
load_dotenv('key')
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= st.secrets['key']

)

#data file
def load_data(path):
    df=pd.read_csv(path, names=["Recipe", "Ingredients", "Time (in minutes)", "instructions", "Level", "Category", "Rate", "Last Date"], header=0)
    return df

# 5-random recipes:
def show_random(df):
    return df.sample()

  
# def search_recipes(find, df):
#     index_list = []
#     for index, row in df.iterrows():
#         ingredients_list=row['Ingredients'].split(",")
#         for ing in row['Ingredients']:
#            if ing.lower() == find.lower():
#               index_list.append(index)
#     return df.iloc[index_list,:]  

# 3 seach by ingredients
def search_recipe(find, df):
    search=df[df["Ingredients"].str.contains(find, case=False)]
    return search

# shopping list step
def shopping_list(selected, df):
    shop=[]
    filter_recipe=df[df["Recipe"]==selected]
    for i in filter_recipe["Ingredients"]:
        #split the row it self
        item=str(i).split(",")
        for j in item:
            if j:
                shop.append(j)
    return shop

#track recipes history
def last_cooked(recipe,date, df):
    data_new=str(date)
    df.loc[df["Recipe"]==recipe , "Last Date"]=data_new
    df.to_csv("recipes.csv", index=False)

#find oldest dates
def oldest_recipe(df):
    oldest=df.sort_values(by ="Last Date")
    return oldest.head(2)

# Assistant:
def get_llm(prompt):
    completion = client.chat.completions.create(
        model="cohere/north-mini-code:free",
        
        messages=[
            {
                "role": "system",
                "content": "You are a chef assistant . provide a recipes ideas by the ingredients",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    response = completion.choices[0].message.content
    return response

def search_api(dash):
    url="https://themealdb.com/api/json/v1/1/search.php"
    response = requests.get(url,
                    params={"s": dash, 'format':'json'}) 
    api=response.json()
    if api["meals"] is None:
        return None
    meal=api["meals"][0]
    list_ingre=[]
#random number 25
    for i in range(1,25):
         item=meal.get(f"strIngredient{i}")
         if item and item != "":
             list_ingre.append(item)
             dateframe_api={
                "Recipe":meal["strMeal"],
                        "Ingredients":", ".join(list_ingre),
                        "Time (in minutes)":30,
                         "instructions":meal["strInstructions"],
                         "Level":"medium",
                         "Category":meal.get("strCategory", ""),
                         "Rate":None, 
                         "Last Date":meal.get("datemodified") or "N/A"
            }
    return dateframe_api

 
# def scale_recipe(select_recipe, serving, df):
#     ingredient_list=[]
#     filter_recipe=df[df["Recipe"]==select_recipe]
#     split_item=filter_recipe["Ingredients"].values[0]

#     for item in split_item:
#         splits=item.split()
#         num=float(splits[1])
#         new_intrgre=" ".join(splits[1:])
#         new_scale=num*serving
#         ingredient_list.append(f"{new_scale} {new_intrgre}")
#     return ", ".join(ingredient_list)

       
def serving_recipe(items, serving):
    scale=[]
    for item in items:
        shop=item.spilt(" ", 1)
        new=float(shop[0])*serving
        rest=shop[1]
        scale.append(f"{new} {rest}")
    return scale
        
    
        


    
