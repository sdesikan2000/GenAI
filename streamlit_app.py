import os
import base64
import requests
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

st.set_page_config(page_title="SAAS Customer Support Bot",page_icon="🤖")

load_dotenv()
# API = st.sidebar.text_input("Add your API key:")

#OpenAI_API = os.getenv('OpenAI_API_KEY')
# os.environ['OPENAI_API_KEY'] = OpenAI_API
#os.environ['OPENAI_API_KEY'] = OpenAI_API_KEY

client = OpenAI()

def predict(prompt):
    completion = client.chat.completions.create(
        # model="ft:gpt-4o-mini-2024-07-18:personal:custom-fine-tuned-model:AbOWr1n9",
        model="ft:gpt-4o-mini-2024-07-18:personal:saas-custom-fine-tuned-model:AfOs4E02",
        messages=[
           # {"role": "system", "content": "You are a helpful assistant which acts as FAQ Support Assistant for the TMLC Guided Projects in Generative AI Program and answer to user queries."},
            {"role": "system", "content": "You are a helpful assistant which acts as Support Assistant for the SaaS Product Support Questions."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

st.markdown(f"""<h2 align="center"><font color="#1E3E59">{'SAAS Customer Support Bot'}</font></h2>""",unsafe_allow_html=True)

def set_background():
    page_bg_img = '''
    <style>
    #MainMenu, header, footer {visibility: hidden;}

    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
         width: 275px;
       }]

    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your query!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner('Responding'):
            message_placeholder = st.empty()
            full_response = ""
            try:
                llm_answer = predict(prompt)
                message_placeholder.markdown(llm_answer)
                st.session_state.messages.append({"role": "assistant", "content": llm_answer})
            except:
                st.warning("Something unexpected happened. Please try again!")