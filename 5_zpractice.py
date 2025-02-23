import streamlit as st 
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def create_llm_message(system_prompt):
    resp = []
    resp.append(SystemMessage(content=system_prompt))
    msgs = st.session_state.messages
    for m in msgs:
        if m['role'] == "user":
            resp.append(HumanMessage(content=m['content']))
        elif m['role'] == "assistant":
            resp.append(AIMessage(content=m['content']))
    return resp