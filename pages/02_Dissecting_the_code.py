import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
import replicate
from sqlexamples import SQLExamples
import time


st.markdown("## Dissecting the code with LLM")

@st.cache_data
def generate_llm_data(input):
    """
    Generate LLM data
        :param input: Input to LLM
        :type input: str
        :return: Status of LLM and data
        :rtype: tuple
    """
    with st.spinner('LLM data generation...'):  
        prediction = replicate.models.predictions.create(
            "snowflake/snowflake-arctic-instruct",
            input=input
        )
        for i in range(5):
            prediction.reload()
            if prediction.status in {"succeeded", "failed", "canceled"}:
                break
            else:
                time.sleep(5)
        prediction_status = prediction.status
        prediction_data = prediction.output
    
    return prediction_status, prediction_data

# Generate sidebar
####################################################
with st.sidebar:
    try:
        st.image('images/logo.jpg', use_column_width="always")
    except:
        st.error('Image logo.jpg not found', icon="🚨")
        
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.divider()
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        st.error('API token could not be loaded', icon='🚨')

if 'clicked_sec1' not in st.session_state: st.session_state.clicked_sec1 = False
if 'clicked_sec2' not in st.session_state: st.session_state.clicked_sec2 = False
if 'clicked_sec3' not in st.session_state: st.session_state.clicked_sec3 = False
    
def option_func():
    st.session_state.clicked_sec1 = False
    st.session_state.clicked_sec2 = False
    st.session_state.clicked_sec3 = False
    st.session_state.obs = ''

option_format = st.selectbox(
   "Choice of data management system:",
   ("SQL", "PostgreSQL", "MySQL", "GCP BigQuery", "Azure SQL Server", "Amazon Athena", "Amazon Redshift"),
   on_change=option_func
)

sql_example = SQLExamples()
code_example = sql_example.get_sql_example(option_format)

def click_button_1():
    st.session_state.clicked_sec1 = True
    
def enable_generate_button():
    st.session_state.clicked_sec1 = False
    st.session_state.clicked_sec2 = False
    st.session_state.clicked_sec3 = False

txt_code = st.text_area(
    "Code to analyze",
    placeholder=code_example,
    height=400,
    on_change=enable_generate_button
)

txt_observations = st.text_area(
    "Observations",
    placeholder="Enter some comments about the code or leave the dialog box as it is.",
    height=80,
    on_change=enable_generate_button,
    key='obs'
)

st.divider()
st.markdown("#### Explain the code")

if not st.session_state.clicked_sec1:
    b = st.button('Generate', key=1, on_click=click_button_1)
else:
    # The message and nested widget will remain on the page
    b = None
    prompt_sec1 = f"Your task is to explain the provided {option_format} code snippet."
    prompt_sec1 += "\n\n"
    
    if txt_code:
        prompt_sec1 += txt_code
    else:
        prompt_sec1 += code_example
    
    if txt_observations:
        obs = "\n\nNote the following observations:"
        prompt_sec1 += f" {obs} {txt_observations}"
    
    input = {
        "prompt": prompt_sec1,
        "temperature": 0.2
    }
    
    prediction_status, prediction_data = generate_llm_data(input)
    
    if prediction_status == "succeeded": 
        st.markdown("".join(prediction_data))
    else:
        st.error("LLM data generation failed. Try again later.")
        st.session_state.clicked_sec1 = False


# PART 2 ############################################################
st.divider()
st.markdown("#### Suggest code improvements to optimize performance.")

def click_button_2():
    st.session_state.clicked_sec2 = True

if not st.session_state.clicked_sec2:
    c = st.button('Generate', key=2, on_click=click_button_2)
else:
    # The message and nested widget will remain on the page
    c = None
    prompt_sec2 = f"Suggest improvements to optimize the performance of the provided {option_format} code snippet."
    prompt_sec2 += "\n\n"
    
    if txt_code:
        prompt_sec2 += txt_code
    else:
        prompt_sec2 += code_example
    
    if txt_observations:
        obs = "\n\nNote the following observations:"
        prompt_sec2 += f" {obs} {txt_observations}"
    
    input = {
        "prompt": prompt_sec2,
        "temperature": 0.6
    }
    
    prediction_status, prediction_data = generate_llm_data(input)
    
    if prediction_status == "succeeded": 
        st.markdown("".join(prediction_data))
    else:
        st.error("LLM data generation failed. Try again later.")
        st.session_state.clicked_sec2 = False


# PART 3 ############################################################
st.divider()
st.markdown("#### Suggestions to reduce costs.")

def click_button_3():
    st.session_state.clicked_sec3 = True
    
if not st.session_state.clicked_sec3:
    d = st.button('Generate', key=3, on_click=click_button_3)
else:
    # The message and nested widget will remain on the page
    d = None
    prompt_sec3 = f"Suggest improvements to reduce the costs of this code provided in {option_format}."
    prompt_sec3 += "\n\n"
    
    if txt_code:
        prompt_sec3 += txt_code
    else:
        prompt_sec3 += code_example
    
    if txt_observations:
        obs = "\n\nNote the following observations:"
        prompt_sec3 += f" {obs} {txt_observations}"
    
    input = {
        "prompt": prompt_sec3,
        "temperature": 0.6
    }
    
    prediction_status, prediction_data = generate_llm_data(input)
    
    if prediction_status == "succeeded": 
        st.markdown("".join(prediction_data))
    else:
        st.error("LLM data generation failed. Try again later.")
        st.session_state.clicked_sec3 = False