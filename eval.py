import streamlit as st
import asyncio
from langsmith import Client
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated
from typing import TypedDict
from instructor import patch
from src.graph import salesCompAgent
import pandas as pd

# Replace OpenAI client initialization with ChatOpenAI
client = ChatOpenAI(model=st.secrets['OPENAI_MODEL'], temperature=0, api_key=st.secrets['OPENAI_API_KEY'])

def init_chat_model(model=st.secrets['OPENAI_MODEL'], temperature=0):
    """Initialize the chat model with instructor patch
    Returns: ChatOpenAI instance for making API calls"""
    return client

def eval():
    """Main evaluation function that:
    1. Sets up the testing environment
    2. Creates test datasets
    3. Runs evaluations
    4. Displays results"""

    # Initialize chat history in Streamlit session
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    st.title("Sales Compensation Agent Evaluation")
    
    # Initialize LangSmith client for evaluation tracking
    langsmith_client = Client()

    # Define test cases with questions and expected responses
    examples = [
        {
            "question": "What would be my commission when I close a $2M deal?",
            "response": "To help you calculate your expected commission, I'll need a bit more information. Could you please provide your OTI and annual quota? Once I have this information, I'll be able to calculate your commission.",
        },
        {
            "question": "I can't access the commission system",
            "response": "I will need your Full Name and Email address to create a support ticket",
        },
    ]
    
    dataset_name = "Sales Compensation Agent Evaluation"

    # Create dataset if it doesn't exist
    if not langsmith_client.has_dataset(dataset_name=dataset_name):
        dataset = langsmith_client.create_dataset(dataset_name=dataset_name)
        langsmith_client.create_examples(
            inputs=[{"question": ex["question"]} for ex in examples],
            outputs=[{"response": ex["response"]} for ex in examples],
            dataset_id=dataset.id
        )

    def run_graph(question: str):
        """Runs a single test through the Sales Compensation Agent
        Args:
            question: The test question to ask
        Returns:
            dict: Contains the agent's response"""
        agent = salesCompAgent(api_key=st.secrets['OPENAI_API_KEY'])
        response = agent.graph.invoke({
            "question": question,
            "responseToUser": "",
            "sessionState": {
                "messages": [
                    {"role": "user", "content": question}
                ],
                "currentMessage": question,
            },
            "initialMessage": question,
            "sessionHistory": []
        })
        return {"response": response.get("responseToUser", "")}

    class Grade(TypedDict):
        """Defines the structure for evaluation results"""
        reasoning: Annotated[str, "Detailed analysis of the agent's response quality and appropriateness"]
        is_correct: Annotated[bool, "Whether the response meets sales compensation query handling standards"]

    # Instructions for GPT-4 on how to evaluate responses
    eval_instructions = """You are evaluating a Sales Compensation Agent's responses to user queries.

    Context: This agent handles questions about sales commissions, quotas, bonuses, and related systems.

    You will analyze:
    QUERY: The user's sales compensation related question
    EXPECTED RESPONSE: The standard correct response
    ACTUAL RESPONSE: The agent's response to evaluate

    Evaluation Criteria:

    1. Commission/Bonus Calculations:
       - Verifies all required input data is requested
       - Asks for specific sales performance metrics
       - Maintains accuracy in calculation prerequisites

    2. System Access Issues:
       - Requests appropriate user identification
       - Follows security protocols
       - Provides clear next steps

    3. Information Requests:
       - Asks for relevant data only
       - Provides clear guidance
       - Maintains professional tone

    4. Response Quality:
       - Clear and concise communication
       - No contradictory information
       - Appropriate level of detail

    Score as:
    - True: Response fully meets criteria and effectively handles the query
    - False: Response is incomplete, incorrect, or inappropriate"""

    def final_answer_correct(inputs: dict, outputs: dict, reference_outputs: dict) -> bool:
        """Evaluates if the agent's response is correct using GPT-4
        Args:
            inputs: The test question
            outputs: The agent's response
            reference_outputs: The expected correct response
        Returns:
            bool: True if response meets criteria, False otherwise"""
        
        user = f"""QUERY: {inputs['question']}
        EXPECTED RESPONSE: {reference_outputs['response']}
        ACTUAL RESPONSE: {outputs['response']}"""

        response = client.invoke([
            {"role": "system", "content": eval_instructions},
            {"role": "user", "content": user}
        ])
        
        # Extract the content from the response
        result = response.content
        return "true" in result.lower()

    # Create button to start evaluation
    if st.button("Start Sales Comp Agent Evaluation"):
        with st.spinner("Evaluating agent responses..."):
            # Initialize evaluation run in LangSmith
            run = langsmith_client.create_run(
                project_name="sales-comp-eval",
                name="Sales Comp Agent Evaluation",
                inputs={"evaluation": "Sales Compensation Agent"},
                run_type="chain",
            )
            
            # Get test examples from dataset
            dataset = langsmith_client.read_dataset(dataset_name=dataset_name)
            examples = langsmith_client.list_examples(dataset_id=dataset.id)
            
            # Run evaluation for each test case
            results = []
            for example in examples:
                response = run_graph(example.inputs["question"])
                eval_result = final_answer_correct(
                    example.inputs,
                    response,
                    example.outputs
                )
                
                results.append({
                    "question": example.inputs["question"],
                    "expected": example.outputs["response"],
                    "actual": response["response"],
                    "final_answer_correct": eval_result
                })
            
            # Display results in Streamlit interface
            df = pd.DataFrame(results)
            st.subheader("Evaluation Results")
            st.dataframe(df)
            
            # Calculate and display success rate
            success_rate = (df['final_answer_correct'].value_counts(normalize=True).get(True, 0) * 100)
            st.metric("Agent Response Success Rate", f"{success_rate:.2f}%")

# Entry point of the script
if __name__ == '__main__':
    eval()