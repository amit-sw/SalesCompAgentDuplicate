from contest_agent import ContestAgent
from langchain_openai import ChatOpenAI
import json
from datetime import datetime

def load_test_prompts():
    """Load test prompts from a JSON file"""
    test_prompts = [
        "I want to start a sales contest",
        "I'd like to create a SPIF program. My name is John Doe, email: john@example.com",
        "Can I schedule an appointment for next week?",
        "I want to book the 2pm slot tomorrow",
        "I want to start a sales contest",
        "How do I create a SPIF program?",
        "I'd like to set up a sales incentive. My name is John Doe, email: john@example.com",
        "Can you help me with contest setup?",
        "I need to schedule a consultation for a sales contest",
        "What's the process for starting a contest?",
        "Book appointment for contest discussion",
        "I want to create a Q2 sales incentive program",
        "Need help with SPIF setup. I'm Jane Smith (jane@example.com)",
        "Looking to schedule a meeting about sales contest",
        "What are the steps to create a contest?",
        "I want to book the 2pm slot tomorrow",
        "Contest setup help needed urgently",
        "SPIF program consultation request",
        "Need guidance on sales incentive structure",
        "Want to discuss contest rules and setup",
        "Schedule meeting for SPIF program discussion",
        "Sales contest implementation help",
        "Request for contest consultation",
        "Need to set up Q3 sales incentive",
        "Looking for contest approval process info",
        "Help with sales motivation program",
        "Contest setup consultation needed",
        "SPIF program guidance required",
        "Sales incentive meeting request"
]

    return test_prompts

def evaluate_responses(responses):
    """Analyze the responses"""
    metrics = {
        "total_prompts": len(responses),
        "successful_responses": 0,
        "failed_responses": 0,
        "response_types": {
            "BookAppointment": 0,
            "ConfirmAppointment": 0,
            "Other": 0
        }
    }
    
    for resp in responses:
        if resp.get("error"):
            metrics["failed_responses"] += 1
        else:
            metrics["successful_responses"] += 1
            # Count response types
            if "category" in resp and resp["category"] == "contest":
                metrics["response_types"]["BookAppointment"] += 1

    return metrics

def run_evaluation():
    # Initialize the model and agent
    model = ChatOpenAI(temperature=0)
    agent = ContestAgent(model)
    
    test_prompts = load_test_prompts()
    responses = []
    
    # Create dummy files needed by the agent
    #with open('contestrules.txt', 'w') as f:
    #    f.write("Test contest rules")
    #with open('contesturl.txt', 'w') as f:
    #    f.write("http://test-contest-url.com")
    
    # Process each prompt
    for prompt in test_prompts:
        try:
            state = {
                "userMessage": prompt,
                "conversationHistory": []
            }
            response = agent.contest_agent(state)
            responses.append(response)
        except Exception as e:
            responses.append({"error": str(e), "prompt": prompt})
    
    # Evaluate results
    metrics = evaluate_responses(responses)
    
    # Print results
    print("\n=== Evaluation Results ===")
    print(f"Total prompts tested: {metrics['total_prompts']}")
    print(f"Successful responses: {metrics['successful_responses']}")
    print(f"Failed responses: {metrics['failed_responses']}")
    print("\nResponse types:")
    for rtype, count in metrics['response_types'].items():
        print(f"- {rtype}: {count}")

if __name__ == "__main__":
    run_evaluation()