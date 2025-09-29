# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw:Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your Smoothie will be:", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert Snowpark Dataframe to Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingedients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    
    # 📓 Changing the LIST to a STRING
    ingredients_string = ''

    # 📓 How a FOR LOOP Block Works
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        # st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width=True)

    # st.write(ingredients_string)

    # 🥋 Build a SQL Insert Statement & Test It

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order )
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # -- STOP
    # st.stop()
    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order} !', icon="✅")

    



    
    
