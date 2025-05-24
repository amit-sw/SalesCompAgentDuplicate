import os
import random
import streamlit as st
from langsmith import Client
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated
from typing import TypedDict
from instructor import patch
from src.graph import salesCompAgent
import pandas as pd
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel

# Set environment variables for LangSmith
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "sales-comp-eval"  

DEBUGGING = 0

# Initialization with ChatOpenAI
client = ChatOpenAI(model=st.secrets['OPENAI_MODEL'], temperature=0, api_key=st.secrets['OPENAI_API_KEY'])
langsmith_client = Client()
dataset_name = "Sales Compensation Agent Evaluation"

EVAL_PROMPT= """You are evaluating a Sales Compensation Agent's responses to user queries.

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
    - False: Response is incomplete, incorrect, or inappropriate

    Also provide the reasoning for the score"""


def create_eval_dataset():
    print("starting create eval dataset")
    global langsmith_client, dataset_name

    examples=[
        {
          "input":[
              { "question": "Hi"}, 
              { "answer": "How are you?"},
              { "question": "What is my commission when I close a $2M deal?"},
          ],
          "output":{
             "category":"commission",
             "response": "In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I'll be able to calculate your commission."
          }
        },
        
         
        {
          "input":[
              { "question": "Hi"}, 
              { "answer": "How are you?"},
              { "question": "What is my commission when I close a $2M deal?"},
              { "answer": "In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I'll be able to calculate your commission."},
              { "question": "My OTI is $150K and Annual quota is $30M."},
          ],
          "output":{
             "category":"commission",
             "response": "In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I'll be able to calculate your commission."
          }
        },

        {
          "input":[
              { "question": "Hi"}, 
              { "answer": "How are you?"},
              { "question": "My OTI is $150K and Annual quota is $30M."},
          ],
          "output":{
             "category":"commission",
             "response": "What is the size of the deal?"
          }
        },



        {
          "input":[
              { "question": "Why can't I access the commission system?"},
          ],
          "output":{
             "category":"ticket",
             "response": "I need your full name and a valid email address. This will allow me to create a support ticket for our Sales Compensation team."
          }
        },
    ]


    # Always create/recreate the dataset
    print("Creating new dataset...")  # Debug print
    try:
        # Delete existing dataset if it exists
        if langsmith_client.has_dataset(dataset_name=dataset_name):
            existing_dataset = langsmith_client.read_dataset(dataset_name=dataset_name)
            langsmith_client.delete_dataset(dataset_id=existing_dataset.id)

        # Create new dataset
        dataset = langsmith_client.create_dataset(dataset_name=dataset_name)

        # Format examples correctly for LangSmith API
        for example in examples:
            langsmith_client.create_example(
                inputs={"input": example["input"]},
                outputs={"output": example["output"]},
                dataset_id=dataset.id
            )

        # Verify examples were created
        created_examples = list(langsmith_client.list_examples(dataset_id=dataset.id))
        print(f"Created {len(created_examples)} examples")  # Debug print

    except Exception as e:
        print(f"Error creating dataset: {str(e)}")
        raise

def convertListToMessages(message_list):
    output_list=[]
    for message in message_list:
      if message.get("question"):
        output_list.append(HumanMessage(content=message["question"]))
      elif message.get("answer"):
        output_list.append(AIMessage(content=message["answer"]))
      else:
        print("ERROR. Unexpected dictionary key for {message=}")
    return output_list

def run_graph(conversation):
    agent = salesCompAgent(os.environ['OPENAI_API_KEY'])
    thread_id = random.randint(1000, 9999)
    message_history = convertListToMessages(conversation)
    initial_message = f"{conversation[-1]}"
    thread={"configurable":{"thread_id":thread_id}}
    parameters = {'message_history': message_history, 'initialMessage': initial_message}
    print(f"Invoking agent graph {parameters=}")
    actual_response = agent.graph.invoke(parameters, thread)
    print(f"After graph invocation: {actual_response=}")
    #output_list= convertListToMessages(conversation)
    #actual_response = agent.respond_to_question(output_list)
    return actual_response

class EvalMatch(BaseModel):
    matches: bool
    reasoning: str

def llm_judge_compare(query_list,expected_response,actual_response):
    llm = ChatOpenAI(model=os.environ['OPENAI_MODEL'], temperature=0, api_key=os.environ['OPENAI_API_KEY'])
    messages = [SystemMessage(content=EVAL_PROMPT)]
    m = HumanMessage(content=f"QUERY: {query_list}\nEXPECTED RESPONSE: {expected_response}\nACTUAL RESPONSE: {actual_response}")
    messages.append(m)
    resp=llm.with_structured_output(EvalMatch).invoke(messages)
    print(f"EVAL Response: {resp}\n\n")
    return resp.matches, resp.reasoning

def final_answer_correct(query, expected_category,expected_response,actual_response):
    #print(f" FINAL-ANSWER-CORRECT: {expected_category=}, {expected_response=}, {actual_response=}")
    category_answer_correct = expected_category == actual_response['category']
    response_answer_correct, reason = llm_judge_compare(query, expected_response,actual_response['responseToUser'])
    #print(f" FINAL-ANSWER-CORRECT: {category_answer_correct=}, {response_answer_correct=}")
    return category_answer_correct, response_answer_correct, reason

def main_run():
    global langsmith_client, dataset_name
    # Get test examples from dataset and debug print
    dataset = langsmith_client.read_dataset(dataset_name=dataset_name)
    examples = list(langsmith_client.list_examples(dataset_id=dataset.id))
    print("Number of examples found:", len(examples))  # Debug print

    # Run evaluation for each test case
    results = []
    for example in examples:
        #print(f"{example.inputs=}")
        #print(f"{example.outputs=}")
        try:
            inputs = example.inputs["input"]
            #print("Inputs:", inputs)
            llm_input=convertListToMessages(inputs)
            #print("LLM inputs", llm_input)
            expected_category = example.outputs["output"]["category"]
            #print("Expected category:", expected_category)
            expected_response = example.outputs["output"]["response"]
            #print("Expected response:", expected_response)
            response = run_graph(inputs)

            #print("Actual response:", response)

            cat_result,resp_result, reason = final_answer_correct(inputs,expected_category,expected_response,response)

            question = example.inputs["input"]
            expected = example.outputs["output"]

            result_dict = {
                "example_id": f"{example.id}",
                "question": f"{question}",
                "expected": f"{expected}",
                "actual": f"{response}",
                "cat_result": cat_result,
                "resp_result": resp_result,
                "resp_reason": reason,
            }
            st.write(f"Got result {result_dict=}")
            results.append(result_dict)
        except Exception as e:
            print(f"Error processing example: {str(e)}")
            continue

    print("All results:\n\n", results)

    if results:  # Only create DataFrame if we have results
        df = pd.DataFrame(results)
        st.dataframe(df)
        df.to_csv('eval_results.csv')
        #print("DataFrame head:", df.head())
        return df
    else:
        print("No results to create DataFrame.")
        return None
    
def test_formatting():
    print("test formatting")

    str=[{'example_id': '57b2f277-8bdf-427c-b731-ae99bd47bfa8', 'question': '[{\'question\': "Why can\'t I access the commission system?"}]', 'expected': "{'category': 'ticket', 'response': 'I need your full name and a valid email address. This will allow me to create a support ticket for our Sales Compensation team.'}", 'actual': '{\'initialMessage\': \'{\\\'question\\\': "Why can\\\'t I access the commission system?"}\', \'responseToUser\': \'To help you better, I need your full name and email address. This will allow me to create a support ticket for our Sales Compensation team.\', \'lnode\': \'ticket_agent\', \'category\': \'ticket\', \'sessionHistory\': [], \'message_history\': [HumanMessage(content="Why can\'t I access the commission system?", additional_kwargs={}, response_metadata={})]}', 'cat_result': True, 'resp_result': True, 'resp_reason': "The actual response appropriately requests the user's full name and email address, which aligns with the expected response for handling system access issues. It follows security protocols by not attempting to resolve the issue directly but instead creating a support ticket. The response is clear, concise, and professional, providing the necessary next steps for the user."}, {'example_id': '989117f8-4f49-4483-a248-2db7fd3bad4d', 'question': "[{'question': 'Hi'}, {'answer': 'How are you?'}, {'question': 'My OTI is $150K and Annual quota is $30M.'}]", 'expected': "{'category': 'commission', 'response': 'What is the size of the deal?'}", 'actual': '{\'initialMessage\': "{\'question\': \'My OTI is $150K and Annual quota is $30M.\'}", \'responseToUser\': "Thanks for sharing your OTI and annual quota details! To assist you best, could you please let me know what specific information or help you\'re looking for regarding your On-Target Earnings (OTI) of $150K and your $30M annual quota? Whether it\'s understanding your compensation structure, commission rates, or performance metrics, I\'m here to help!", \'lnode\': \'small_talk_agent\', \'category\': \'smalltalk\', \'sessionHistory\': [], \'message_history\': [HumanMessage(content=\'Hi\', additional_kwargs={}, response_metadata={}), AIMessage(content=\'How are you?\', additional_kwargs={}, response_metadata={}), HumanMessage(content=\'My OTI is $150K and Annual quota is $30M.\', additional_kwargs={}, response_metadata={})]}', 'cat_result': False, 'resp_result': False, 'resp_reason': 'The expected response specifically asks for the size of the deal, which is a critical piece of information needed to proceed with any commission or bonus calculation. The actual response, while polite and professional, does not request the deal size or any specific sales performance metric. Instead, it asks a general question about what the user wants to know, which does not directly address the implied need for deal size information. Therefore, the actual response does not fully meet the criteria for commission/bonus calculations, as it fails to ask for the specific sales performance metric required.'}, {'example_id': 'e0367424-355a-4a51-98f3-da05b1147029', 'question': '[{\'question\': \'Hi\'}, {\'answer\': \'How are you?\'}, {\'question\': \'What is my commission when I close a $2M deal?\'}, {\'answer\': "In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I\'ll be able to calculate your commission."}, {\'question\': \'My OTI is $150K and Annual quota is $30M.\'}]', 'expected': '{\'category\': \'commission\', \'response\': "In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I\'ll be able to calculate your commission."}', 'actual': '{\'initialMessage\': "{\'question\': \'My OTI is $150K and Annual quota is $30M.\'}", \'responseToUser\': "Thank you for providing the details!\\n\\nHere\'s how we calculate your expected commission:\\n\\n1. Base Commission Rate (BCR) = OTI / Annual Quota = 150,000 / 30,000,000 = 0.005 (or 0.5%)\\n2. Expected Commission = BCR * Deal Value = 0.005 * 2,000,000 = $10,000\\n\\nSo, your expected commission for closing the $2M deal is $10,000. If you have any other questions or need further assistance, feel free to ask!", \'lnode\': \'commission_agent\', \'category\': \'commission\', \'sessionHistory\': [], \'message_history\': [HumanMessage(content=\'Hi\', additional_kwargs={}, response_metadata={}), AIMessage(content=\'How are you?\', additional_kwargs={}, response_metadata={}), HumanMessage(content=\'What is my commission when I close a $2M deal?\', additional_kwargs={}, response_metadata={}), AIMessage(content="In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I\'ll be able to calculate your commission.", additional_kwargs={}, response_metadata={}), HumanMessage(content=\'My OTI is $150K and Annual quota is $30M.\', additional_kwargs={}, response_metadata={})]}', 'cat_result': True, 'resp_result': True, 'resp_reason': "The actual response appropriately acknowledges the user's provided data (OTI and annual quota) and proceeds to calculate the commission based on the $2M deal value. It clearly explains the calculation steps, uses the correct inputs, and provides a concise, professional answer. The response meets the criteria for commission calculation by requesting necessary data, performing accurate calculations, and communicating clearly without contradictions. Therefore, it fully meets the expected response criteria."}, {'example_id': '3bb24183-36d6-4df2-9884-4438b07e7349', 'question': "[{'question': 'Hi'}, {'answer': 'How are you?'}, {'question': 'What is my commission when I close a $2M deal?'}]", 'expected': '{\'category\': \'commission\', \'response\': "In order to calculate your expected commission, please provide OTI and annual quota? Once I have this information, I\'ll be able to calculate your commission."}', 'actual': '{\'initialMessage\': "{\'question\': \'What is my commission when I close a $2M deal?\'}", \'responseToUser\': \'To help you calculate your commission on the $2M deal, could you please provide me with your On-Target Incentive (OTI) and your Annual Quota? This information will help me give you an accurate calculation.\', \'lnode\': \'commission_agent\', \'category\': \'commission\', \'sessionHistory\': [], \'message_history\': [HumanMessage(content=\'Hi\', additional_kwargs={}, response_metadata={}), AIMessage(content=\'How are you?\', additional_kwargs={}, response_metadata={}), HumanMessage(content=\'What is my commission when I close a $2M deal?\', additional_kwargs={}, response_metadata={})]}', 'cat_result': True, 'resp_result': True, 'resp_reason': 'The actual response correctly requests the necessary input data (OTI and annual quota) to calculate the commission on the $2M deal, aligning with the expected response. It maintains a professional tone, is clear and concise, and provides appropriate guidance for the next step. Therefore, it fully meets the criteria for commission calculation inquiries.'}]
    new_list = []
    for elem in str[:1]:
        question = elem['question']
        expected = elem['expected']
        actual = elem['actual']
        cat_result = elem['cat_result']
        resp_result = elem['resp_result']
        ex_category = expected["category"]
        ex_response = expected["response"]
        ac_category = actual["category"]
        ac_response = actual["response"]
        new_record = {'question': question, 'ex_category': ex_category, 'ac_category': ac_category, 
                      'ex_response': ex_response, 'ac_response': ac_response, 'cat_result': cat_result, 
                      'resp_result': resp_result}
        new_list.append(new_record)

    df=pd.DataFrame(new_list)
    st.table(df)

    
if __name__ == '__main__':
    #create_eval_dataset()
    #main_run()
    test_formatting()
