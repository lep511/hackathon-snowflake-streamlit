import streamlit as st
import pandas as pd
import replicate
import json
import time

# App title
st.set_page_config(page_title="Hackathon - The Future of AI is Open",
                   menu_items={
                       'About': "This is a demo app for the Hackathon - **The Future of AI is Open**"
                   }
)

st.markdown("## Transform unstructured text into JSON.")

with st.expander("About this section..."):
    st.markdown("Turn unstructured text into bespoke JSON tables.")
    st.markdown("LLM models allow you to identify key information and determine what specific data you need to extract from the text. They could be names, dates, numbers or any other relevant information.")
    st.markdown("**IMPORTANT: Avoid entering information with confidential data or that may affect third parties.**")

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
        for i in range(3):
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
        st.image('images/logo.jpg', use_column_width="always", caption="Hackathon - The Future of AI is Open")
    except:
        st.error('Image logo.jpg not found', icon="🚨")
        
    if 'REPLICATE_API_TOKEN' in st.secrets:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        st.error('API token could not be loaded', icon='🚨')


if 'clicked_sec800' not in st.session_state: st.session_state.clicked_sec800 = False

uns_text_example = "Yesterday Michael bought 2 apples and 3 oranges at the store. Jenna bought 12 oranges, 4 kiwis, and 2 melons."

uns_data = st.text_area(
    "Enter the text",
    placeholder="e.g. " + uns_text_example,
    height=250,
    key="uns_data"
)

def click_button_1():
    st.session_state.clicked_sec800 = True

def click_button_reset():
    st.session_state.clicked_sec800 = False
    st.session_state.uns_data = ''

if not st.session_state.clicked_sec800:
    b = st.button('Generate', key=1, on_click=click_button_1)
else:
    b = None
    prompt_gen = "Your task is to take the unstructured text provided and convert it into a well-organized table format using JSON. Identify the main entities, attributes, or categories mentioned in the text and use them as keys in the JSON object. Then, extract the relevant information from the text and populate the corresponding values in the JSON object. Ensure that the data is accurately represented and properly formatted within the JSON structure. The resulting JSON table should provide a clear, structured overview of the information presented in the original text:\n\n"
    
    if uns_data: 
        prompt_gen += uns_data
    else:
        prompt_gen += uns_text_example

    input = {
        "prompt": prompt_gen,
        "temperature": 0.9
    }
    
    prediction_status, prediction_data = generate_llm_data(input)
    
    if prediction_status == "succeeded": 
        response = "".join(prediction_data)
        json_data = json.loads(response)
        st.json(json_data, expanded=True)
        json_string = json.dumps(json_data, indent=2)
        
        st.download_button(
            label="Download JSON",
            file_name="data.json",
            mime="application/json",
            data=json_string,
        )
    
    else:
        st.error("LLM data generation failed. Try again later.")
        st.cache_data.clear()
        st.session_state.clicked_sec800 = False
    
    
    c = st.button('Reset', key=101, type="primary", on_click=click_button_reset)