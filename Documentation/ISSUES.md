CURRENT ISSUES AND OPEN QUESTIONS:

6. Ticket Agent (1/3): When a ticket is generated, and the agent responds by informing me and asking me if there is anything else that I need help with, if I say Thank you!, it repeats itself which is annoying.

5. Contest Agent (12/23): Two issues. It shares the process but doesn't clarify that user has to acknowledget that they understand the process. However, when the user says that they got it, the process for appointment booking continues. The problem is that once the appointment is booked and the user says "Thanks" or "Got it", the agent resends the meeting invite. It's almost impossible to get out of that loop.

4. Contest Agent: on 12/23 got this error:

RefreshError: ('invalid_grant: Token has been expired or revoked.', {'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'})

Note: I fixed the error by deleting token.pickle and re-running the app.

3. Commission calculation appears formatted sometimes but occasionally it shows up with all markup. Continues to be inconsistent. (FIXED)

2. Ticket agent is still not ending the conversation the way I want it to. I have observed two issues:
    a. It sends two emails which are sent about 4 minutes apart.
    b. At the end, when it submits the form it responds back to the user what it sent in the email to generate a ticket. Ideally, what I'd like is that it sends the email with the summary of the issue and tells the user that it has submitted the ticket without responding with the issue summary. (FIXED)

1. I get a lot of warnings which are not real issues when I run the app.
