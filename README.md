# Data Insight App
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

## Setup Instructions

### Prerequisites
- Python 3.8 or later 🐍
- pip3 📦

### Installation
1. **Clone this repository**
   ```bash
   git clone https://github.com/lep511/hackathon-snowflake-streamlit.git
   cd hackathon-snowflake-streamlit
   ```

2. **Install requirements**
   ```bash
      pip install -r requirements.txt
   ```

3. **Add your API token to your secrets file**\
Create a `.streamlit` folder with a `secrets.toml` file inside.
   ```bash
   mkdir .streamlit
   cd .streamlit
   touch secrets.toml
   ```
   
   Use your text editor or IDE of choice to add the following to `secrets.toml`:
      ```toml
      REPLICATE_API_TOKEN = "your API token here"
      ```
   Learn more about Streamlit secrets management in [our docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).
   
   Alternatively, you can enter your Replicate API token via the `st.text_input` widget in the app itself (once you're running the app).

4. **Run the Streamlit app**

To run enter:
   ```bash
   cd ..
   streamlit run Data_Insight_App.py
   ```

### Deployment
Host your app for free on Streamlit Community Cloud. These instructions are also available in [our docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app).

1. Sign up for a Community Cloud account or log in at [share.streamlit.io](https://share.streamlit.io/).
2. Click "New app" from the upper-right corner of your workspace.
3. Fill in your repo, branch, and file path. As a shortcut, you can also click "Paste GitHub URL" to paste a link directly to `streamlit_app.py` on GitHub.  

#### Optional: store your Replicate API token with Community Cloud secrets
Securely store your Replicate API token with Community Cloud's secrets management feature. These instructions are also available in [our docs](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).
   
##### Add secrets before deploying
1. Before clicking "Deploy", click "Advanced settings..."  
2. A modal will appear with an input box for your secrets.   
3. Provide your secrets in the "Secrets" field using TOML format. For example:
   ```toml
   REPLICATE_API_TOKEN = "your API token here"
   ```
   
##### Add secrets after deploying
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click the overflow menu icon (AKA hamburger icon) for your app.
3. Click "Settings".  
4. A modal will appear. Click "Secrets" on the left.  
5. After you edit your secrets, click "Save". It might take a minute for the update to be propagated to your app, but the new values will be reflected when the app re-runs.
