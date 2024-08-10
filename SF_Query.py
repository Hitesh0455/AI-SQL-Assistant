# pip langchain, streamlit, OpenAI, Snowflake-python-connector
import os
from pathlib import Path
from PIL import Image
from app_secrets import OPENAI_API_KEY
import streamlit as st
from snowflake_connection import execute_sf_query
from langchain.prompts import load_prompt
from langchain_openai import OpenAI
from langchain.chains import LLMChain

# setting up env variable
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY
root_path =[p for p in Path(__file__).parents if p.parts[-1]=="OpenAI"][0]

# create front end
st.title("Connecting to Database")
# User input in the natural language
user_input= st.text_input("Enter your query:")
# create a list with the tab titles you want
tab_titles = ["Result","Query","ERD Diagram"]
#Create tabs
tabs = st.tabs(tab_titles)

# load the image
erd_image =Image.open(f'{root_path}/images/ERD_image.png')
# Put image in the tab
with tabs[2]:
    st.image(erd_image)


# Creating the prompt
prompt_template= load_prompt(f"{root_path}/prompt/tpch_prompt.yaml")
#create an instance of llm
llm = OpenAI(temperature=0)

sql_generation_chain = LLMChain(llm=llm,prompt=prompt_template,verbose=True)

if user_input:
    sql_query = sql_generation_chain(user_input)
    #Execute the sql into the database 
    result=execute_sf_query(sql_query['text'])

    #Write data to the tabs
    with tabs[0]:
        st.write(result)
    with tabs[1]:
        st.write(sql_query['text'])



