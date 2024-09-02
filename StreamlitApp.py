import os
import json
import pandas as pd 
import traceback
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file ,get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
 
import streamlit as st
st.set_page_config(page_title="MCQ Generator") 
#loading json file
with open("Response.json","r") as file:
    RESPONSE_JSON=json.load(file)

 
st.title("MCQs Creator Application with Langchain")

with st.form("user_input"):
    
    uploaded_file=st.file_uploader("Upload .pdf and .txt File Here!")

    mcq_count=st.number_input("No.  of MCQS", min_value=3,max_value=10)

    subject=st.text_input("Insert Subject Here!", max_chars=25)

    tone=st.text_input("Complexity Level of the Questions",max_chars=50, placeholder="Simple")

    button=st.form_submit_button("Create MCQS")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading......"):
            try:
                text=read_file(uploaded_file)
                response=generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject":subject,
                        "tone": tone,
                        "response_json":RESPONSE_JSON
                    }
                    )
        
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                pass
                if isinstance(response,dict):
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            st.write(table_data)
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label='Review',value=response['review'])
                        else:
                            st.error("Error in the Table data ",icon="🚨")
                
                else:
                    st.write(response)