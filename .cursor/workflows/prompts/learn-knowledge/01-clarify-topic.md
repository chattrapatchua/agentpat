# Step 1 — Clarify topic

You are running workflow **learn-knowledge**.

If `topic` was not provided in workflow inputs, ask the user:

> What knowledge do you want to learn? Describe the topic, scope, and any constraints (market, geography, timeframe).

Wait for the user's reply before researching. Treat everything the user adds in this chat thread as **user-provided evidence** for the research step.

When the topic is clear, record it as `workflow.topic` for this session and proceed to the **research** step.
