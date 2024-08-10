import os
import streamlit as st
from app_secrets import OPENAI_API_KEY
from langchain_openai import OpenAI

# setting up env variable
os.environ["OPENAI_API_KEY"]= OPENAI_API_KEY

#Create front end
st.title("---Demo Search page---")
prompt = st.text_input("Enter the question:")

#Create an instance of OpenAI
llm = OpenAI(temperature=0.9)

if prompt:
    response= llm(prompt=prompt)
    st.write(response)

