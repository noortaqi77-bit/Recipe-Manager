import streamlit as st
import pandas as pd 
import functions
import datetime
import time as t


data=functions.load_data('recipes.csv')
st.set_page_config(layout="wide")
st.title("Delicious Recipes 🍴")


tab0,tab1, tab2, tab3, tab4, tab5, tab6 , tab7, tab8= st.tabs(["Home", "Add New Recipes", "Find Recipes", "All Recipes", "Random Recipes", "Recipe's Rate", "Shopping List" , "Cooking History", "Smart Chef"])

with tab0:
    st.text("Welcome !...")
    st.image("https://static.vecteezy.com/system/resources/previews/022/727/413/original/cookbook-of-recipes-baking-ingredients-products-and-kitchen-tools-for-cooking-cartoon-illustration-vector.jpg", width=450)

#Add a new recipe to the collection  
with tab1:
    st.subheader("Add New Recipe")
    recipe=st.text_input("Recipe name 🍽️:")
    ingredients=st.text_area("The Ingredients 🫕:")
    ingredient1=ingredients.replace(",", "\n")
    ingredient=ingredient1.split("\n")
    time=st.slider("Preparation time 'in minutes' ⏱️", min_value=1, max_value=300, value=10)
    step=st.text_area("Cooking instructions 🔢:")
    level_=st.radio("Level 🎚️", ["Easy", "Medium", "Hard"])
    category= st.selectbox("category 🍴",["breakfast", "lunch", "dinner","desert"], index=None,placeholder="Select category",
    accept_new_options=True)
    sentiment_mapping = [1, 2, 3, 4, 5]
    st.markdown("Rating 👍👎")
    rate = st.feedback("stars")
    if rate is not None:
         st.markdown(f"You selected {sentiment_mapping[rate]} star(s).")
    date=st.date_input("Last cooked date: 📅")
    Date=str(date)



    buttom=st.button("Save The Recipe")
    
    if buttom:
        if recipe and ingredient and time and step and level_ and category and rate:
            
            row={"Recipe":recipe,
                        "Ingredients":", ".join(ingredient),
                        "Time (in minutes)":time,
                         "instructions":step,
                         "Level":level_,
                         "Category":category, 
                         "Rate":rate, 
                         "Last Date":Date
                        }
            
            row_df=pd.DataFrame([row])
            # new=pd.concat(row_df, rn)
            row_df.to_csv("recipes.csv", mode="a", header=False, index=False)
            st.success("Recipe saved successfully")
            t.sleep(5)
            st.rerun()
        else:
            st.error("Please fill required fields!!")
            
            

#1. The program asks for an ingredient to search for  
#2. The program displays all recipes that contain that ingredient 
with tab2:
    st.header("Find Recipes by ingredients 🔎!")
    find=st.text_input("Enter an ingradient : ")
    button2=st.button("Search..")
    search=functions.search_recipe(find, data)

    if button2:
        if search.empty:
            st.error("There is no recipe with this ingradient!")
        else:
            st.write(search)
            
    st.divider()
    st.subheader("Search From Another Data")
    dash=st.text_input("Enter the dash ")
    if st.button("search"):
        if dash:
            lis=functions.search_api(dash)
            if lis is None:
                st.text("No recipes found with this name")
            else:
                #new_list2=pd.DataFrame([lis])
                new_list=st.dataframe(lis)
                #new_list2=new_list.T
                # if st.button("save"):
                #     new_list2.to_csv("recipes.csv", mode="a", header=False, index=False)
                #     st.success("Recipe saved successfully")
                #     t.sleep(5)
                #     st.rerun()            

# The program displays a list of all recipe names with their preparation times         
with tab3:
    st.header("All Recipes 🍽️")
    st.table(data[["Recipe","Time (in minutes)"]].sort_values(by="Time (in minutes)").reset_index(drop=True))
    #st.dataframe(r, hide_index=True, use_container_width=True)
    
#random recipes
with tab4:
    st.header("Random Recipes ")
    st.dataframe(functions.show_random(data))

# The program allows users to rate recipes and sort by rating  
with tab5:
    st.header("Recpies by Rating ⭐ ")
    st.dataframe(data.sort_values("Rate", ascending=False).reset_index(drop=True))

#4. The program can generate a shopping list based on selected recipes  
with tab6:
    st.header("Shopping list 🛒 ")
    lists=st.selectbox("choose recipe", options=data["Recipe"])
    if lists:
        shop=functions.shopping_list(lists, data)
        st.text("Your Ingredients List 📋")
        for i in shop:
            st.checkbox(i)
    st.divider()
    st.suheader("scale ingredient")
    if st.button("scale serving"):
        serving=st.number_input("Number Of Servings")
        if serving and lists:
            scale=fuctions.serving_recipe(shop, serving)
            st.text(f"Your Ingredients List for {serving} serving  📋")
            for i in scale:
                st.checkbox(i)

#The program can track cooking history and suggest recipes you haven't made recently 
with tab7:
    st.header(" Track Cooking History ")
    st.text("Update Date for a Recipe")
    selected_recipe=st.selectbox("select recipe", data["Recipe"].unique())
    new_date=st.date_input("new date")
    if st.button("Update.."):
        functions.last_cooked(selected_recipe, new_date, data)
        st.success(f"Updated {selected_recipe} date successfully! ")
        t.sleep(5)
        st.rerun()
    
    st.divider()
    
    st.subheader("Oldest recipes..")
    st.write(functions.oldest_recipe(data))

    
#Ai help
with tab8:
    st.subheader("How can I help you 🤖")
    respone=st.text_input("Enter your Ingrediends")
    
    click=st.button("Ask AI")
    if click:
        if respone:
            result=functions.get_llm(respone)
            st.write(result)
        else:
            st.warning("please enter your ingrediens")

# with tab9:
#     select_recipe=st.selectbox("choose recipe to scale :", data["Recipe"])
#     serving=st.number_input("How many serving do ypu want ? ")
#     scale=st.button("Scale Serving")
#     if scale :
#         st.write(functions.scale_recipe(select_recipe,serving, data))
        


