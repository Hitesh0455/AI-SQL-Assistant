import os
from app_secrets import OPENAI_API_KEY
import streamlit as st
from snowflake_connection import execute_sf_query
from langchain_openai import OpenAI
from langchain.prompts import load_prompt
from pathlib import Path

def main():
    #setup env variable
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    #project root directory
    current_dir = Path(__file__)
    root_dir = [p for p in current_dir.parents if p.parts[-1]=='OpenAI'][0]
    #frontend
    st.title("How can I help you:")
    prompt = st.text_input("enter your query")

    prompt_template = load_prompt(f'{root_dir}/prompt/tpch_prompt.yaml')
    final_prompt = prompt_template.format(input=prompt)

    llm = OpenAI(temperature=0.9)

    if prompt:
        response = llm(prompt=final_prompt)
        with st.expander(label="SQL Query",expanded=False):
            st.write(response)
        output = execute_sf_query(response)
        st.write(output)
        

if __name__ == "__main__":
    main()

