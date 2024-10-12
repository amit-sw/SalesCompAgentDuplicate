# src/small_talk_agent.py

from typing import List
from src.create_llm_message import create_llm_message

# When PolicyAgent object is created, it's initialized with a client, a model, and an index. 
# The main entry point is the policy_agent method. You can see workflow.add_node for policy_agent node in graph.py


class SmallTalkAgent:
    
    def __init__(self, client, model):
        
        # Initialize the PolicyAgent with an OpenAI client and a Pinecone Index
        self.client = client
        self.model = model

    def generate_response(self, user_query: str) -> str:
        # Generate a response using the retrieved content and the user's original query.
        
        # Construct the prompt to guide the language model in generating a response
        prompt_guidance = f"""
        You are an expert with deep knowledge of sales compensation. Your job is to comprehend the message from 
        the user even if it lacks specific keywords, always maintain a friendly, professional, and helpful tone. 
        If a user greets you, greet them back by mirroring user's tone and verbosity, and offer assitance. 

        """
        llm_messages = create_llm_message(prompt_guidance)

        # Invoke the model with the classifier prompt
        
        llm_response = self.model.invoke(llm_messages)

        small_talk_response = llm_response.content

        return small_talk_response


    def small_talk_agent(self, state: dict) -> dict:
        #Handle policy-related queries by retrieving relevant documents and generating a response.
        
        
        # Generate a response using the retrieved documents and the user's initial message
        full_response = self.generate_response(state['initialMessage'])
        
        # Return the updated state with the generated response and the category set to 'policy'
        return {
            "lnode": "small_talk_agent", 
            "responseToUser": full_response
        }
