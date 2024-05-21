import streamlit as st
import replicate
from sqlexamples import SQLExamples
import time

st.set_page_config(page_title="Hackathon - The Future of AI is Open",
                   menu_items={
                       'About': "This is a demo app for the Hackathon - **The Future of AI is Open**"
                   }
)

# Generate sidebar
####################################################
with st.sidebar:
    try:
        st.image('images/logo.jpg', use_column_width="always", caption="Hackathon - The Future of AI is Open")
    except:
        st.error('Image logo.jpg not found', icon="🚨")
        

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.markdown("## SQL or NoSQL *(or maybe both)*")

with st.expander("About this section..."):
    st.markdown("When businesses evaluate database structures and analytics processes, there are two primary types of databases to choose from: SQL and NoSQL.") 
    st.markdown("Given that SQL databases work with highly structured data, the problem for many enterprises is how to accommodate the growing volume of unstructured and particularly semi-structured data that is collected from both inside and outside the business.")
    st.markdown("The exponential growth in semi-structured data arising from IoT, Web and mobile devices is pushing the need for data formats that can support flexible database schemas (JSON, Parquet, XML, Avro, and ORC) to move and store that data.")
    st.markdown("*Text source: [Snowflake: What Is The Difference Between Sql And Nosql?](https://www.snowflake.com/data-warehousing-difference-sql-nosql)*")

col1, col2 = st.columns(2)
with col1:
    text_input_engine = st.text_input(
        "Enter some text:",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder="e.g. ",
        key=11
    )

with col2:
    text_input_data = st.text_input(
        "Enter some text:",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder="e.g. IoT",
        key=21
    )
    
data_sizes = ["less than 50MB", "50MB-250MB", "250MB-1GB", "1GB-5GB", "5GB-20GB", "more than 20GB"]
color = st.select_slider(
    "Select data size:",
    options=data_sizes
)
