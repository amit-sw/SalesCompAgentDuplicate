# src/policy_agent.py

from typing import List
from src.create_llm_message import create_llm_message

class PolicyAgent:
    
    def __init__(self, client, model, index):
        
        # Initialize the PolicyAgent with an OpenAI client and a Pinecone Index
        self.client = client
        self.index = index
        self.model = model

    def retrieve_documents(self, query: str) -> List[str]:
        # Generate an embedding for the query and retrieve relevant documents from Pinecone.
        embedding = self.client.embeddings.create(model="text-embedding-ada-002", input=query).data[0].embedding
        results = self.index.query(vector=embedding, top_k=3, namespace="", include_metadata=True)
        
        retrieved_content = [r['metadata']['text'] for r in results['matches']]
        return retrieved_content

    def generate_response(self, retrieved_content: List[str], user_query: str) -> str:
        # Generate a response using the retrieved content and the user's original query.
        
        # Construct the prompt to guide the language model in generating a response
        prompt_guidance = f"""
        I have retrieved the following information related to your query:
        {retrieved_content}

       
        """
        llm_messages = create_llm_message(prompt_guidance)

        # Invoke the model with the classifier prompt
        
        llm_response = self.model.invoke(llm_messages)

        category = llm_response.content

        # Generate a response using the GPT-4 model, including system and user messages
        #llm_response = self.client.chat.completions.create(
        #    model="gpt-4o-mini",
        #    messages=[
        #        {"role": "system", "content": "You are a helpful and patient guide based in Silicon Valley."},
        #        {"role": "user", "content": prompt_guidance}
        #    ]
        #)
        
        # Extract and return the full response from the language model's output
        #full_response = llm_response.choices[0].message.content
        #return full_response

    def policy_agent(self, state: dict) -> dict:
        #Handle policy-related queries by retrieving relevant documents and generating a response.
        
        # Retrieve relevant documents based on the user's initial message
        retrieved_content = self.retrieve_documents(state['initialMessage'])
        
        # Generate a response using the retrieved documents and the user's initial message
        full_response = self.generate_response(retrieved_content, state['initialMessage'])
        
        # Return the updated state with the generated response and the category set to 'policy'
        return {
            "lnode": "policy_agent", 
            "responseToUser": full_response,
            "category": "policy"
        }
