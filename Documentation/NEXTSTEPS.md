# NEXT STEPS (Updated: 1/6):

1) Complete UAT for all sub-agents. Based on the outcome, refine the RAG document and prompts. Note that in the main prompt where you have examples, you might want to add examples using Claude.

2) Exception request: TO BE DONE BY JAHANGIR
    a. Ask the user to fill out an intake form (Google Form) -- https://forms.gle/zBp6H4ApLRmAT2Cx8
    b. Inform them the rough timeline for approval workflow i.e., roughly how long it takes to get SCRC decision.

3) Plan Explainer: TO BE DONE BY JAHANGIR
    Sometimes reps ask questions about how their plan works. These questions are simply to get clarity on the mechanics of the comp plan. This sub-agent has leanred all plan constructs in the company and has deep understanding of how they work. Note: We will use RAG to upload descriptions of all comp plans by role. 

4) Feedback Collector: (Narrative generator based on email responses)
    Sometimes sales leaders want to share their feedback about what's working and what's not working in the current sales comp plan design. They may have ideas from their past experiences. The sub-agent understands all current sales comp plans, and is also an expert researcher and has the ability to go deeper and ask intriguing questions to understand exactly what problem are they trying to solve.

5) Test with Multiple LLMs: Test Sales Comp Agent using newer ChatGPT models (4o, 4o mini, o1 or o1 mini) and other LLMs, like Grok, Claude etc. Compare the time it takes for them versus ChatGPT

6) Move the prompts outside of the code in a separate data file, and save them in a data store. Keep multi-tenancy in mind.

7) Create a lighter version of Sales Comp Agent: Remove complex tasks like booking appointment which are dependent on calendar integration. Create something which a Sales Comp Leader can deploy in their company by simply signing up for a company account (free version with no ability to do RAG or a paid version with their own instance of sales comp agent with ability to do RAG) -- Tag line: Reduce your ticket volume by 30%.

7) Modify the app for multi-tenant environment, which includes deploying it on a URL and ability to create a company account. Company employees would be able to access their own version.

8) Host it on AWS or GCP.

9) Self-assessment and Continuous Improvement Loop:
Assess every user conversation for it's effectiveness and provide feedback to your developers on how to improve either the prompt or RAG documents or the flow. 