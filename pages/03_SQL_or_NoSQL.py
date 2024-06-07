import streamlit as st
import replicate
from sqlexamples import SQLExamples
import time
import os

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

@st.cache_data
def generate_llm_data(input):
    """
    Generate LLM data
        :param input: Input to LLM
        :type input: str
        :return: Status of LLM and data
        :rtype: tuple
    """
    try:
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
    except:
        return False, False

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
        

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

if 'clicked_sec500' not in st.session_state: st.session_state.clicked_sec500 = False

st.markdown("## SQL or NoSQL *(or maybe both)*")

with st.expander("About this section..."):
    st.markdown("When businesses evaluate database structures and analytics processes, there are two primary types of databases to choose from: SQL and NoSQL.") 
    st.markdown("Given that SQL databases work with highly structured data, the problem for many enterprises is how to accommodate the growing volume of unstructured and particularly semi-structured data that is collected from both inside and outside the business.")
    st.markdown("The exponential growth in semi-structured data arising from IoT, Web and mobile devices is pushing the need for data formats that can support flexible database schemas (JSON, Parquet, XML, Avro, and ORC) to move and store that data.")
    st.markdown("*Text source: [Snowflake: What Is The Difference Between Sql And Nosql?](https://www.snowflake.com/data-warehousing-difference-sql-nosql)*")


txt_main = st.text_area(
    "Specify how you will use the data:",
    placeholder="e.g. Creating a database for an inventory system within a construction company.",
    height=200,
    key="obs"
)

col1, col2 = st.columns(2)
with col1:
    text_input_plang = st.text_input(
        "Programming languages to use:",
        placeholder="e.g. Python, Java, C++",
        key="plang"
    )
    cloud_data = st.toggle("Use the cloud for data storage.", value=True, key=12)
    unstr_data = st.toggle("Use unstructured data such as images, business documents, emails.", key=13)

with col2:
    text_input_data = st.text_input(
        "Enter the source of the data:",
        placeholder="e.g. Statistical data, census data, IoT",
        key="source"
    )
    
    data_size_opt = ["less than 250MB", "250MB-2GB", "2GB-10GB", "10GB-100GB", "100GB-500GB", "more than 500GB"]
    data_size = st.select_slider(
        "Select the data size range:",
        value=data_size_opt[2],
        options=data_size_opt
    )

st.divider()

def click_button_1():
    st.session_state.clicked_sec500 = True
    
def click_button_reset():
    st.session_state.clicked_sec500 = False
    st.session_state.obs = ''
    st.session_state.plang = ''
    st.session_state.source = ''

if not st.session_state.clicked_sec500:
    b = st.button('Generate', key=100, on_click=click_button_1)
else:
    b = None
    
    if not txt_main:
        st.write("Using the predefined data...")
        txt_main = "Creating a database for an inventory system within a construction company."
    
    prompt_gen = "Your task is to choose the best option between SQL or NoSQL according to these criteria:\n\n"
    
    prompt_gen += f"- The main idea of the project is {txt_main}\n"
    
    if cloud_data: prompt_gen += "- The data will be saved in the cloud.\n"
    if text_input_data: prompt_gen += "- The data will be from " + text_input_data + ".\n"
    
    if unstr_data: prompt_gen += "- The data will be unstructured.\n"
    else: prompt_gen += "- The data will be structured.\n"
    
    if text_input_plang: prompt_gen += "- The programming languages will be " + text_input_plang + ".\n"
    prompt_gen += "- The sizes of the data will be " + data_size + ".\n\n"
    
    prompt_gen += "Identify areas where using SQL or NoSQL can be more efficient, faster, or consume fewer resources.\n"
    prompt_gen += "Finally, it ends by recommending whether to use SQL, or use NoSQL, or use both."
    
    input = {
        "prompt": prompt_gen,
        "temperature": 0.9
    }
    
    prediction_status, prediction_data = generate_llm_data(input)
    
    if prediction_status == "succeeded": 
        st.markdown("### Generated LLM report")
        st.markdown("".join(prediction_data))
    else:
        st.error("LLM data generation failed. Try again later.")
        st.cache_data.clear()
        st.session_state.clicked_sec500 = False
        
    c = st.button('Reset', key=101, type="primary", on_click=click_button_reset)

