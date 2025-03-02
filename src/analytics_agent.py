import pandas as pd
import numpy as np
from typing import List
from pydantic import BaseModel
from src.create_llm_message import create_llm_message


# Data model for structuring the LLM's response
class AnalyticsResponse(BaseModel):
    analysis_result: str
    suggested_followup: str

class AnalyticsAgent:
    """
    A class to handle data analytics requests.
    This agent helps users analyze CSV data by processing uploads and answering questions about the data.
    """
    
    def __init__(self, model, client=None):
        """
        Initialize the AnalyticsAgent with necessary components.

        Args:
            model: The language model to use for generating responses.
            client: The OpenAI client for API interactions (optional).
        """
        self.model = model
        self.client = client

    def generate_response(self, csv_data: str, user_query: str) -> str:
        """
        Generate an analysis response based on the CSV data and user's query.

        Args:
            csv_data (str): The CSV data uploaded by the user.
            user_query (str): The user's question about the data.

        Returns:
            str: The generated analysis from the language model.
        """
        
        analytics_prompt = f"""
        You are an expert data analyst with deep knowledge of data analysis and visualization. Your job is to 
        analyze CSV data and provide insightful answers to user questions. Always maintain a friendly, 
        professional, and helpful tone throughout the interaction.

        The user has uploaded a CSV file with the following data:
        {csv_data}

        The user's question about this data is: "{user_query}"

        Instructions:
        1. Analyze the CSV data to answer the user's specific question
        2. Provide clear insights based on the data
        3. Include relevant statistics or patterns you observe
        4. Suggest a follow-up question the user might want to ask

        Provide your analysis in a clear, concise format.
        """
        
        # Create a well-formatted message for LLM
        llm_messages = create_llm_message(analytics_prompt)

        # Use structured output for analytics response
        llm_response = self.model.with_structured_output(AnalyticsResponse).invoke(llm_messages)

        return llm_response

    def analytics_agent(self, state: dict) -> dict:
        """
        Process the user's analytics request, handle file uploads, and generate analysis.

        Args:
            state (dict): The current state of the conversation, including the initial message.

        Returns:
            dict: An updated state dictionary with the generated response.
        """
        
        # Check if a CSV file has been uploaded
        if 'csv_data' not in state:
            # If no CSV file is uploaded yet, ask the user to upload one
            return {
                "lnode": "analytics_agent",
                "responseToUser": "I'd be happy to help you analyze some data. Please upload a CSV file so I can get started.",
                "category": "analytics",
                "waitForFileUpload": True,
                "fileUploadButton": {
                    "text": "Upload CSV File",
                    "accept": ".csv"
                }
            }
        
        # Check if the user has asked a question about the data
        if 'analytics_question' not in state:
            # If CSV is uploaded but no question asked yet
            return {
                "lnode": "analytics_agent",
                "responseToUser": "Thanks for uploading your data! What specific question would you like me to answer about this dataset?",
                "category": "analytics",
                "waitForQuestion": True
            }
        
        # Generate analysis based on the CSV data and user's question
        analysis_response = self.generate_response(state['csv_data'], state['analytics_question'])
        
        # Construct the full response to the user
        full_response = f"""
        ## Analysis Results
        
        {analysis_response.analysis_result}
        
        ## Follow-up Suggestion
        
        {analysis_response.suggested_followup}
        
        Would you like me to help with anything else about this data?
        """
        
        # Return the updated state with the generated analysis
        return {
            "lnode": "analytics_agent",
            "responseToUser": full_response,
            "category": "analytics"
        }
