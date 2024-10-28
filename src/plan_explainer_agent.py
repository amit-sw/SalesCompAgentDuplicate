# src/plan_explainer_agent.py

from typing import List
from src.create_llm_message import create_llm_message

# When PlanExplainerAgent object is created, it's initialized with a client, a model, and an index. 
# The main entry point is the plan_explainer_agent method. You can see workflow.add_node for plan_explainer_agent 
# node in graph.py

class PlanExplainerAgent:
    
    def __init__(self, client, model, index):
        """
        Initialize the PlanExplainerAgent with necessary components.
        
        :param client: OpenAI client for API calls
        :param model: Language model for generating responses
        :param index: Pinecone index for document retrieval
        """
        self.client = client
        self.index = index
        self.model = model

    def retrieve_documents(self, query: str) -> List[str]:
        """
        Retrieve relevant documents based on the given query.
        
        :param query: User's query string
        :return: List of relevant document contents
        """
        # Generate an embedding for the query and retrieve relevant documents from Pinecone.
        embedding = self.client.embeddings.create(model="text-embedding-ada-002", input=query).data[0].embedding
        results = self.index.query(vector=embedding, top_k=3, namespace="", include_metadata=True)
        
        retrieved_content = [r['metadata']['text'] for r in results['matches']]
        return retrieved_content

    def generate_response(self, retrieved_content: List[str], user_query: str) -> str:
        """
        Generate a response based on retrieved content and user query.
        
        :param retrieved_content: List of relevant document contents
        :param user_query: Original user query
        :return: Generated response string
        """
        # Construct the prompt to guide the language model in generating a response
        plan_explainer_prompt = f"""
        You are an expert with deep knowledge of all sales compensation plan types, plan components, and how they work. 
        The user's query seems to be about compensation plan construct or mechanics. Always maintain a friendly, 
        professional, and helpful tone. 
        
        Step 1: Retrieve relevant documents from company's Sales Compensation Plans document: {retrieved_content}

        Step 2: Remember the following terms and their meanings:

            - Plan construct: There are three main plan constructs or plan types i.e., Quota plan, KSO plan, or 
              Hybrid plan. To understand plan constructs fully you need to understand additional details about the 
              plan type. In case of Quota plan, information about number of quota buckets, weights of each quota 
              buckets, incentive cap etc. In case of KSO plan, number of KSO, weights of each KSO, incentive cap etc. 
              In case of Hybrid plan, which combines both Quota plan and KSO plan, all the details related to both 
              plans, and percent of on-target incentive (OTI), tied to quota versus KSO.

            - Plan components: It includes Base Commission Rate (BCR), Accelerated Commission Rate 1 or 2 
              (ACR1 or ACR2, aka Accelerators), Kickers (aka add-on incentives), Multi-year downshift, transition
              point, Multipliers etc.

            - Plan mechanics: It means how different components work in a given plan construct. For example, if a 
              plan has kickers or not, when will ACR1 and ACR2 kick-in, how is multi-year downshift applied, etc.

        
        Step 3: Explain the plan construct, plan components, or plan mechanics using the retrieved document.

        Step 4: If you are not able to find a relevant plan details, ask them their role or title i.e., Account Executive 
        (AE), Account Manager (AM, MAM, GAM), Core Rep, Solution Consultant (SC), System Engineer (SE), Specialist Sales
        Rep (SSR), Domain Specialist (DS), Channel Business Manager (CBM), Channel SE, Business Development Rep (BDR),
        Renewal Rep, etc. Use the title to find relevant plan details document again  

        Step 5: Even after role clarity you are not able to find the relevant document then use your vast knowledge
        of sales compensation plans, terminologies, policies, and practices in a large Enterprise software company. 

        """
        # Create a well-formatted message for LLM by passing the retrieved information above to create_llm_messages
        llm_messages = create_llm_message(plan_explainer_prompt)

        # Invoke the model with the well-formatted prompt, including SystemMessage, HumanMessage, and AIMessage
        llm_response = self.model.invoke(llm_messages)

        # Extract the content attribute from the llm_response object 
        plan_explainer_response = llm_response.content

        return plan_explainer_response

    def plan_explainer_agent(self, state: dict) -> dict:
        """
        Main entry point for plan-related queries.
        
        :param state: Current state dictionary containing user's initial message
        :return: Updated state dictionary with generated response and category
        """
        # Handle plan type, construct, mechanics related queries by retrieving relevant documents and generating 
        # a response.
        
        # Retrieve relevant documents based on the user's initial message
        retrieved_content = self.retrieve_documents(state['initialMessage'])
        
        # Generate a response using the retrieved documents and the user's initial message
        full_response = self.generate_response(retrieved_content, state['initialMessage'])
        
        # Return the updated state with the generated response and the category set to 'policy'
        return {
            "lnode": "plan_explainer_agent", 
            "responseToUser": full_response,
            "category": "planexplainer"
        }
