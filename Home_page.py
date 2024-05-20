import streamlit as st
import os

# App title
st.set_page_config(page_title="Hackathon - The Future of AI is Open",
                   menu_items={
                       'About': "This is a demo app for the Hackathon - **The Future of AI is Open**"
                   }
)

"""## Data Insight App
### Introduction

The Data Insight App is a powerful tool for analyzing data. 
Whether you’re a data scientist, business analyst, or curious explorer, 
this app provides a user-friendly interface to explore, manipulate, and gain insights from your datasets.

#### Key Features:

1. **Analysing data files with LLM** allows you to analyse data files. Supported data formats are CSV, Apache Parquet and JSON.




"""

# Generate sidebar
####################################################
with st.sidebar:
    st.image('images/logo.jpg', use_column_width="always")