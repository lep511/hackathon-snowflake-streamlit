import streamlit as st
import os

# App title
st.set_page_config(page_title="Hackathon - The Future of AI is Open",
                   menu_items={
                       'About': "This is a demo app for the Hackathon - **The Future of AI is Open**"
                   }
)

if 'REPLICATE_API_TOKEN' in st.session_state:  
    api_token = st.session_state['REPLICATE_API_TOKEN']
    os.environ["REPLICATE_API_TOKEN"] = st.session_state['REPLICATE_API_TOKEN']

else:  
    api_token = "Enter the token"
    st.error('Enter the [Replicate api token](https://replicate.com/account/api-tokens)', icon='🚨')


"""## Data Insight App
### Introduction

The Data Insight App is a powerful tool for analyzing data. 
Whether you’re a data scientist, business analyst, or curious explorer, 
this app provides a user-friendly interface to explore, manipulate, and gain insights from your datasets.

#### Key Features:

1. **Analysing data files with LLM**: allows you to analyse data files. Supported data formats are CSV, Apache Parquet and JSON.

2. **Dissecting the code**: allows you to enter a code in SQL and choose between different data managers and obtain different action points to improve the code.

3. **SQL or NoSQL**: Assists in choosing between SQL and NoSQL databases, considering factors like structured and semi-structured data growth from IoT, web, and mobile sources.

4. **Unstructured text to JSON**: Turn unstructured text into bespoke JSON tables.


#### Used tools:

* [Streamlit](https://streamlit.io/) - A faster way to build and share data apps

* [Snowflake Arctic](https://arctic.streamlit.app/) - An efficient, intelligent, and truly open-source language model

* [REPLICATE](https://replicate.com/) - Making machine learning accessible to every software developer.

* [markdown-pdf](https://pypi.org/project/markdown-pdf/) - The free, open source Python module markdown-pdf will create a PDF file from your content in markdown format.

"""

# Generate sidebar
####################################################
with st.sidebar:

    token = st.text_input("Replicate api token", value=api_token, type="password")
    if token:
        api_token = token
        st.session_state['REPLICATE_API_TOKEN'] = token
        os.environ["REPLICATE_API_TOKEN"] = token

    try:
        st.image('images/logo.jpg', use_column_width="always", caption="Hackathon - The Future of AI is Open")
    except:
        st.error('Image logo.jpg not found', icon="🚨")