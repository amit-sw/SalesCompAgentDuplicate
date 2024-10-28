
# NEXT STEPS (Updated: 10/22):

1) SPIF and Sales Contests: 
    a. Ask the user to fill out an intake form (Google Form) -- (https://forms.gle/KmKgwZXSj4aR1Pqn8)
    b. Book an appointment with Sales Comp Team using Google Calendar.

2) Exception request: 
    a. Ask the user to fill out an intake form (Google Form) -- https://forms.gle/zBp6H4ApLRmAT2Cx8
    b. Inform them the rough timeline for approval workflow i.e., roughly how long it takes to get SCRC decision.

3) Plan Explainer: 
    Sometimes reps ask questions about how their plan works. These questions are simply to get clarity on the mechanics of the comp plan. This sub-agent has leanred all plan constructs in the company and has deep understanding of how they work. Note: We will use RAG to upload descriptions of all comp plans by role. 

4) Feedback Collector: 
    Sometimes sales leaders want to share their feedback about what's working and what's not working in the current sales comp plan design. They may have ideas from their past experiences. The sub-agent understands all current sales comp plans, and is also an expert researcher and has the ability to go deeper and ask intriguing questions to understand exactly what problem are they trying to solve.

5) Insights and Analytics: 
    A user can ask high level questions about sales comp data. How many people achieved their quota YTD? What was the E:B ratio in the last 3 quarters? Note: We have to be thoughtful about what data are we making accessible. It can't confidential personal data or company's financial performance data.

6) Something to do with reading Inbox ...






# Flow of Execution

1) User Input and Initial Classifier:
The user input is passed to the graph.stream method.
The initial_classifier method is invoked since the entry point is set to "classifier".

2) Returning from Initial Classifier:
The initial_classifier method classifies the input and returns a state with the category.
The returned state includes "category": category, where category could be "policy", "commission", etc.

3) Routing in Main Router:
The main_router method receives the state and returns the category, which corresponds to the next node in the state graph.

4) StateGraph Handles Transitions:
The StateGraph framework automatically transitions to the node corresponding to the returned category.
It then calls the method associated with that node.

# Why do we need both initial_classifier and main_router?

initial_classifier: Focuses solely on classifying the user input. It doesn't decide what to do next.

main_router: Takes the classification result and determines the next state in the graph. 

This decouples the classification logic from the routing logic.

# RAG script

1) RAG script is in the file called _rag.py

2) When you run the script, it will authenticate with Google Drive using the client_secrets.json file, download the specified files from Google Drive, convert them to text, generate embeddings, and upload those embeddings to Pinecone.

3) The script will output a message in the Streamlit app indicating that the documents have been processed and embeddings uploaded to Pinecone. You can monitor the progress in your terminal or the Streamlit web interface.

4) You should see something like this in your Streamlit app: Documents processed and embeddings uploaded to Pinecone.

# How to obtain 'client_secrets.json'

1) Create a Project in Google Cloud Console:

Go to the Google Cloud Console.
Create a new project or select an existing project.

2) Enable Google Drive API:

In the Cloud Console, navigate to APIs & Services > Library.
Search for "Google Drive API" and click Enable.

3) Create OAuth 2.0 Credentials:

Go to APIs & Services > Credentials.
Click on Create Credentials > OAuth 2.0 Client IDs.
Set the Application type to "Desktop app" or "Web application" depending on your use case.
Fill in the required fields and click Create.

4) Download client_secrets.json:

After creating the credentials, download the client_secrets.json file.
Save this file in the root directory of your project.