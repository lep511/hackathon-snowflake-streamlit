import streamlit as st
import os

# App title
st.set_page_config(page_title="Hackathon - The Future of AI is Open",
                   menu_items={
                       'About': "This is a demo app for the Hackathon - **The Future of AI is Open**"
                   }
)

"""## The Future of AI is Open
### Hackathon

"""

# Generate sidebar
####################################################
with st.sidebar:
    st.image('images/logo.jpg', use_column_width="always")