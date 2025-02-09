import json
import streamlit as st
from src.google_firestore_integration import get_prompts, update_prompt_by_name
import pandas as pd 
from google.oauth2 import service_account

def get_google_cloud_credentials():
    """
    Gets and sets up Google Cloud credentials for authentication.
    This function:
    1. Retrieves the Google service account key from Streamlit secrets
    2. Converts the JSON string to a Python dictionary
    3. Creates a credentials object that can be used to authenticate with Google services
    
    Returns:
        service_account.Credentials: Google Cloud credentials object
    """
    # Get Google Cloud credentials from Streamlit secrets
    js1 = st.secrets["GOOGLE_KEY"]
    #print(" A-plus Google credentials JS: ", js1)
    credentials_dict=json.loads(js1)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)   
    st.session_state.credentials = credentials
    return credentials

def set_up_credentials():
    if 'credentials' not in st.session_state:
        credentials = get_google_cloud_credentials()
        st.session_state['credentials']=credentials
    return st.session_state['credentials']

def show_all(creds):
    s1=get_prompts(creds)
    df=pd.DataFrame(s1)
    st.dataframe(df, hide_index=True)

def show_one_detail(creds):
    s1=get_prompts(creds)
    prompt_names=[s.get('prompt_name') for s in s1]
    prompt_values=[s.get('prompt_value') for s in s1]
    prompt_map=dict(zip(prompt_names,prompt_values))
    option = st.selectbox("Prompt",prompt_names,index=None)
    if option:
        prv=prompt_map[option]
        st.text(f"{prv}")


def update_one(creds):
    prompt_name=st.text_input("Prompt name")
    prompt_value=st.text_area("Prompt text")
    if st.button("Upsert"):
        s=update_prompt_by_name(creds,'default', prompt_name,prompt_value)
        st.write(s)

def main():
    creds=set_up_credentials()
    col1,col2,col3=st.tabs(['List','Review','Upsert'])
    with col1:
        show_all(creds)
    with col2:
        show_one_detail(creds)
    with col3:
        update_one(creds)



main()