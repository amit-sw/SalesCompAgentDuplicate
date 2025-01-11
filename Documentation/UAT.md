USER ACCEPTANCE TESTING

1. TICKET AGENT (20/20 PASSED)

Commission Calculation Issues:
- My Q4 commission shows $0 but I closed 5 enterprise deals (PASSED)
- The system calculated my commission using old rates after the policy change (PASSED)
- My split commission with another rep isn't showing the correct 60/40 split (PASSED)
- The system isn't counting my renewal deals towards my commission target (PASSED)
- My accelerator bonus isn't triggering despite hitting 150% quota (PASSED)

Territory and Account Assignment:
- Deals from my transferred territory aren't included in my compensation (PASSED)
- Commission for my inherited accounts is going to the previous rep (PASSED)
- My global account sales are being credited to the local territory rep (PASSED)
- The system double-counted a deal after territory realignment (PASSED)
- My named accounts were reassigned but I still had active opportunities (PASSED)

Policy and Special Cases:
- My maternity leave period shows incorrect commission calculations (PASSED)
- The system isn't applying the guaranteed commission for my ramp period (PASSED)
- My draw recovery is being calculated on the wrong base salary (PASSED)
- The SPIF bonus for new product sales isn't showing in my statements (PASSED)
- My commission clawback amount seems incorrect after customer cancellation (PASSED)

System and Data Issues:
- My Salesforce opportunities aren't syncing with the commission system (PASSED)
- The exchange rate used for my international deals is incorrect (PASSED)
- My commission statement is missing deals closed last quarter (PASSED)
- The system shows different numbers in the dashboard vs. detailed report (PASSED)
- My team's roll-up numbers don't match individual rep calculations (PASSED)

2. POLICY AGENT (13/20 PASSED)

Policy Understanding and Accuracy:
- What's my base commission rate for enterprise deals? (FAILED)
- How does the accelerator bonus work after hitting 100% quota? (PASSED)
- What's the current policy on split commissions between territories? (PASSED)
- How are renewal deals counted towards my quota attainment? (FAILED)
- Can you explain the clawback policy for customer cancellations? (PASSED)

Context and Relevance:
- What commission rate applies to my EMEA territory deals? (PASSED)
- I'm a new sales rep in Q2. What's my ramp quota and guaranteed commission? (PASSED)
- As an enterprise AE, what's my quarterly vs annual quota breakdown? (PASSED)
- I just inherited accounts mid-quarter. How are commissions handled? (PASSED)
- How do SPIFs work for our new product launches? (FAILED)

Document Retrieval:
- What's our current policy on commission for multi-year deals? (FAILED)
- I need information about both draw policies and recovery schedules (PASSED)
- What's the commission structure for channel partner deals? (PASSED)
- What are the compensation terms for deals with professional services? (PASSED)
- When does the new fiscal year compensation plan take effect? (PASSED)

Response Quality:
- Can you show me the exact policy wording about accelerator thresholds? (PASSED)
- I don't understand the tiered commission structure - can you explain it simply? (PASSED)
- Where can I find the complete policy about international deal compensation? (FAILED)
- When was the commission structure last updated and what changed? (FAILED)
- What should I do if my deal structure isn't covered by the standard commission policy? (PASSED)

3. COMMISSION AGENT (0/20 TESTED)

Basic Commission Calculations:
- Calculate base commission for a $100K deal at 10% rate (PASSED)
- Process multi-tier commission with 3 different thresholds (PASSED)
- Calculate split commission between 3 sales reps (PASSED)
- Apply accelerator bonus for 120% quota achievement (PASSED)
- Calculate clawback amount for partial deal cancellation (PASSED)

Advanced Calculations:
- Process multi-currency deal with varying exchange rates (PASSED)
- Calculate commission on multi-year deal with different rates per year (PASSED)
- Apply SPIF bonus on top of regular commission (PASSED)
- Calculate pro-rated commission for mid-quarter hire (PASSED)
- Process commission with draw recovery adjustment (FAILED)

Edge Cases:
- Handle commission calculation with negative adjustments (PASSED) Note: I used prorated credit and the math was perfect.
- Process commission for deals with missing data fields (PASSED)
- Calculate commission for deals spanning multiple quarters (PASSED)
- Handle commission updates after retroactive policy changes (FAILED)
- Process commission for deals with multiple product lines (PASSED)

System Integration:
- Sync commission data with Salesforce opportunities (NOT TESTED)
- Generate accurate commission statements in PDF format (NOT TESTED)
- Update real-time dashboard with commission calculations (NOT TESTED)
- Handle batch processing of multiple commissions (NOT TESTED)
- Maintain audit trail of all commission calculations (NOT TESTED)




