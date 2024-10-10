import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# This function is crucial for maintaining context in an ongoing conversation with an LLM, 
# ensuring that the model has access to the full conversation history and system instructions when 
# generating its next response.
def create_llm_message(system_prompt):
    # Initialize empty list to store messages
    resp = []
    
    # Add system prompt as the first message. This will provide the overall instructions to LLM.
    resp.append(SystemMessage(content=system_prompt))
    
    # Get chat history from Streamlit's session state
    msgs = st.session_state.messages
    
    # Iterate through chat history, and based on the role (user or assistant) tag it as HumanMessage or AIMessage
    for m in msgs:
        if m['role'] == 'user':
            # Add user messages as HumanMessage
            resp.append(HumanMessage(content=m['content']))
        elif m['role'] == 'assistant':
            # Add assistant messages as AIMessage
            resp.append(AIMessage(content=m['content']))
    
    # Print the final message list for debugging
    print(f"resp is {resp}")
    
    # Return the formatted message list
    return resp