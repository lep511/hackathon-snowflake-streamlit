import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
import replicate
import time

# App title
st.set_page_config(page_title="Snowflake Arctic")

class SampleData:
    """
    Class to generate sample data
    """
    def __init__(self, type_file):
        self.type_file = type_file
        self.name = "sample-" + type_file

    def load_sample_data(self):
        """
        Generate sample data
        """
        if self.type_file == "CSV":
            self.sample_data = pd.read_csv("data/country_codes.csv")
        elif self.type_file == "Apache Parquet":
            self.sample_data = pd.read_parquet("data/house_price.parquet")
        elif self.type_file == "JSON":
            self.sample_data = pd.read_json("data/sample_data.json")

        return self.sample_data

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
                        "data_file": None,
                        "status_header": "not_started", 
                        "status_not_header": "not_started", 
                        "prediction_header_data": None,
                        "prediction_no_header_data": None,
                        "prediction_sec_data": None,
                        "prediction_vis_data": None
    }

option_format = st.selectbox(
   "Select an extension file:",
   ("CSV", "Apache Parquet", "JSON")
)

type_file = {"CSV": "csv", "Apache Parquet": "parquet", "JSON": ["js", "json"]}
sample_data = st.toggle("Use sample data file.")

if sample_data:
    uploaded_file = SampleData(option_format)

else:
    uploaded_file = st.file_uploader(f"Choose a {option_format} file (max. 50MB)", type=type_file[option_format])
    if option_format == "CSV":
        no_csv_header = st.toggle("The CSV file does not contain a header.")
    else:
        no_csv_header = False

# Check if file is uploaded
############################################
if uploaded_file is not None:        
    prompt = f"Explains this {option_format} file and all its columns, indicates the potential uses of this data and which columns could cause problems:"
    header_data = True
    
    if option_format == "CSV":       
        
        if sample_data:
            df = uploaded_file.load_sample_data()
            string_data = df.to_string()
            
        else:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            string_data=str(bytes_data,'utf-8')
            data = StringIO(string_data)
        
            if no_csv_header:
                df = pd.read_csv(data, header=None)
                prompt = f"Explains this {option_format} file. Indicates what the data can be used for and what might cause problems:"
                header_data = False
            else:
                df = pd.read_csv(data)
        
    elif option_format == "Apache Parquet":
        if sample_data:
            df = uploaded_file.load_sample_data()
            string_data = df.to_string()
        else:
            bytes_data = uploaded_file.getvalue()
            data = BytesIO(bytes_data)
            df = pd.read_parquet(data)
            string_data = df.to_string()
        
    elif option_format == "JSON":
        if sample_data:
            df = uploaded_file.load_sample_data()
            string_data = df.to_string()
        else:
            bytes_data = uploaded_file.getvalue()
            string_data=str(bytes_data,'utf-8')
            data = StringIO(string_data)
            df = pd.read_json(data)
        
    st.dataframe(df)
    
    st.divider()
    st.markdown(f"### Info {option_format} file")
    input = {
        "prompt": prompt + string_data[0:1000],
        "temperature": 0.2
    }
    
    if header_data:         # If CSV file contains header      
        if st.session_state.status_llm["status_header"] == "not_started" or st.session_state.status_llm["data_file"] != uploaded_file.name:
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
        if st.session_state.status_llm["status_not_header"] == "not_started" or st.session_state.status_llm["data_file"] != uploaded_file.name:
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
    st.markdown("### Security issues")
    prompt_sec = f"Look for any leaks of sensitive personal data. Discuss the security issues in this {option_format} file in Python. Select only the ones you think are relevant."
    input_sec = {
        "prompt": prompt_sec + string_data[0:500],
        "temperature": 0.4
    }
    
    # prediction_sec
    if not st.session_state.status_llm["prediction_sec_data"] or st.session_state.status_llm["data_file"] != uploaded_file.name:
        prediction_status, prediction_data = generate_llm_data(input_sec)

        if prediction_status == "succeeded":
            st.session_state.status_llm["prediction_sec_data"] = prediction_data
            st.markdown("".join(prediction_data))
        else:
            st.error("LLM data generation failed. Try again later.")
    
    else:
        st.markdown("".join(st.session_state.status_llm["prediction_sec_data"]))  
    
    
    st.divider()
    st.markdown("### Data visualization techniques")
    prompt_vis = f"Discuss the pros and cons of different data visualization techniques for data analysis of this {option_format} file in Python. Select only the ones you think are relevant."
    input_vis = {
        "prompt": prompt_vis + string_data[0:500],
        "temperature": 0.9
    }
    
    # prediction_vis
    if not st.session_state.status_llm["prediction_vis_data"] or st.session_state.status_llm["data_file"] != uploaded_file.name:
        prediction_status, prediction_data = generate_llm_data(input_vis)

        if prediction_status == "succeeded":
            st.session_state.status_llm["prediction_vis_data"] = prediction_data
            st.markdown("".join(prediction_data))
        else:
            st.error("LLM data generation failed. Try again later.")
    
    else:
        st.markdown("".join(st.session_state.status_llm["prediction_vis_data"]))  

    # Store CSV file name
    if not sample_data:
        st.session_state.status_llm["data_file"] = uploaded_file.name
    