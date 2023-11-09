import streamlit
import snowflake.connector
import pandas as pd
import requests
from urllib.error import URLError
streamlit.title("My Parents New Healthy Diner")
   
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text(' 🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



fruitlist = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

fruitlist = fruitlist.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(fruitlist.index), default=['Avocado', 'Strawberries'])
fruits_to_show = fruitlist.loc[fruits_selected]
# Display the table on the page.
def Return_fruit(fruit):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
   # write your own comment -what does the next line do? 
   fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

streamlit.dataframe(fruits_to_show)

streamlit.header('Fruit advice')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
   else:
      streamlit.dataframe(Return_fruit(fruit_choice))
     
except:
   streamlit.error()






streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
      return  my_cur.fetchall()

if streamlit.button('Get all loaded fruits'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("Insert into pc_rivery_db.public.fruit_load_list values ('"+new_fruit+"')")
      return streamlit.write('Thanks for adding: ', new_fruit)
add_fruit = streamlit.text_input('What fruit would you like to add?')      
if streamlit.button('Upload new fruit'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   a = insert_row_snowflake(add_fruit)
      




