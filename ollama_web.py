import streamlit as st
import numpy as np
import pandas as pd
import ollama
import os

st.set_page_config(
    page_title="Ollama"
)

with st.sidebar:
    if not(os.path.exists("models.txt")):
        os.system("ollama list > models.txt")
    
    models = pd.read_fwf("models.txt")
    models = models["NAME"].to_list()
    model = st.selectbox(
        "Lütfen model seçiniz : ",
        models
    )

    role = st.text_input("Lütfen role belirtiniz : ")

def answer(prompt):
    with st.chat_message("ai"):
        message = {'role': role, 'content': prompt}
        response = ollama.chat(model=model, messages=[message])
        response = response['message']['content']
        st.write(response)

prompt = st.chat_input("Enter Prompt")
if prompt:
    with st.chat_message("human"):
        st.write(prompt)
    
    answer(prompt)