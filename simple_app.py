import streamlit as st
import pandas as pd
from io import StringIO
import replicate
import time

# App title
st.set_page_config(page_title="Snowflake Arctic")

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
    st.title('Snowflake Arctic')
    st.image('logo.jpg', use_column_width="always")
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.divider()
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        st.error('API token could not be loaded', icon='🚨')

# Store LLM-status
if "status_llm" not in st.session_state.keys():
    st.session_state.status_llm = {
                        "csv_file": None,
                        "status_header": "not_started", 
                        "status_not_header": "not_started", 
                        "prediction_header_data": None,
                        "prediction_no_header_data": None,
                        "prediction_vis_data": None
    }

no_csv_header = st.toggle("The CSV file does not contain a header.")
uploaded_file = st.file_uploader("Choose a CSV file (max. 200MB)", type="csv")

# Check if file is uploaded
############################################
if uploaded_file is not None:        
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    string_data=str(bytes_data,'utf-8')
    data = StringIO(string_data)
    st.write("First 250 rows")
    if no_csv_header:
        df = pd.read_csv(data, nrows=250, header=None)
        prompt = "Explains this CSV file. Indicates what the data can be used for and what might cause problems:"
        header_data = False
    else:
        df = pd.read_csv(data, nrows=250)
        prompt = "Explains this CSV file and all its columns, indicates the potential uses of this data and which columns could cause problems:"
        header_data = True
    
    st.dataframe(df)
    
    st.divider()
    st.markdown("### Info CSV file")
    input = {
        "prompt": prompt + string_data[0:1000],
        "temperature": 0.2
    }
    
    if header_data:         # If CSV file contains header      
        if st.session_state.status_llm["status_header"] == "not_started" or st.session_state.status_llm["csv_file"] != uploaded_file.name:
            # Generate LLM data
            prediction_status, prediction_data = generate_llm_data(input)
            
            if prediction_status == "succeeded": 
                st.session_state.status_llm["status_header"] = "done"
                st.markdown("".join(prediction_data))
                st.session_state.status_llm["prediction_header_data"] = prediction_data
            else:
                st.error("LLM data generation failed. Try again later.")
        else:
            st.markdown("".join(st.session_state.status_llm["prediction_header_data"]))
    
    else:                   # If CSV file does not contain header
        if st.session_state.status_llm["status_not_header"] == "not_started" or st.session_state.status_llm["csv_file"] != uploaded_file.name:
            # Generate LLM data
            prediction_status, prediction_data = generate_llm_data(input)
            
            if prediction_status == "succeeded": 
                st.session_state.status_llm["status_not_header"] = "done"
                st.markdown("".join(prediction_data))
                st.session_state.status_llm["prediction_no_header_data"] = prediction_data
            else:
                st.error("LLM data generation failed. Try again later.")    
        else:
            st.markdown("".join(st.session_state.status_llm["prediction_no_header_data"]))  

    st.divider()
    st.markdown("### Data visualization techniques")
    prompt_vis = "Discuss the pros and cons of different data visualization techniques for data analysis of this csv file in Python. Select only the ones you think are relevant."
    input_vis = {
        "prompt": prompt_vis + string_data[0:500],
        "temperature": 0.2
    }
    
    # prediction_vis
    if not st.session_state.status_llm["prediction_vis_data"] or st.session_state.status_llm["csv_file"] != uploaded_file.name:
        prediction_status, prediction_data = generate_llm_data(input_vis)

        if prediction_status == "succeeded":
            st.session_state.status_llm["prediction_vis_data"] = prediction_data
            st.markdown("".join(prediction_data))
        else:
            st.error("LLM data generation failed. Try again later.")
    
    else:
        st.markdown("".join(st.session_state.status_llm["prediction_vis_data"]))  

    # Store CSV file name
    st.session_state.status_llm["csv_file"] = uploaded_file.name
    