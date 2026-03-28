# Customer Support Chatbot Report

## 1. Introduction

This project evaluates whether a local language model can support common e-commerce customer-service tasks without relying on external APIs. The chatbot runs completely offline through Ollama using the `llama3.2:3b` model and compares two prompting strategies: zero-shot prompting and one-shot prompting.

The purpose of the experiment is to measure how well a small local model can answer customer questions in a way that is relevant, coherent, and helpful. This is important for organizations that want stronger privacy guarantees and lower operating costs while still exploring AI support workflows.

## 2. Methodology

The application is implemented in Python and sends POST requests to `http://localhost:11434/api/generate`. Two prompt templates are used:

- `prompts/zero_shot_template.txt`: instructions plus the current customer query
- `prompts/one_shot_template.txt`: the same instructions plus one complete example query-response pair

The chatbot processes 20 manually adapted e-commerce queries derived from technical-support style prompts. For each query, the script generates one zero-shot response and one one-shot response and writes both to `eval/results.md`.

Manual evaluation was performed using three criteria on a 1 to 5 scale:

- Relevance: how directly the response answers the question
- Coherence: how clear and readable the response is
- Helpfulness: how actionable and useful the answer is

## 3. Results And Analysis

After reviewing the generated responses and manually scoring all 40 rows in `eval/results.md`, one-shot prompting performed better overall than zero-shot prompting.

Average scores:

- Zero-shot: Relevance `3.65`, Coherence `4.40`, Helpfulness `3.15`
- One-shot: Relevance `4.00`, Coherence `4.70`, Helpfulness `3.65`

These results show that one-shot prompting improved performance across all three metrics. The strongest gains were in helpfulness and coherence, which suggests that the example response helped the model produce more structured and customer-friendly answers.

There were several clear examples where one-shot prompting outperformed zero-shot prompting:

- Query 3, payment failure with deducted amount: the zero-shot response assumed the payment likely succeeded and redirected the user toward delivery tracking, which was not a safe conclusion. The one-shot response handled the issue more carefully by recommending account and support verification.
- Query 10, changing the shipping method: the zero-shot response invented a specific 24-hour policy window. The one-shot response stayed more conservative and simply advised contacting support before shipment.
- Query 13, delayed package: the one-shot response clearly stated that it did not have real-time shipping access and suggested checking the carrier or account updates, which made it more reliable than the zero-shot version.

The evaluation also highlighted some weaknesses in both prompting methods:

- Query 14 included unsupported details such as business hours, contact channels, or placeholder contact information.
- Query 15 one-shot invented a specific seven-day exchange policy, which violates the instruction not to make up store rules.
- Query 19 both methods confidently claimed that only one discount code could be used, even though that policy was not provided in the prompt.

This pattern shows that one-shot prompting improves consistency but does not fully prevent hallucinated policy details. The model performs best when the question can be answered with general support guidance and performs worse when the answer depends on store-specific policies or real account data.

## 4. Conclusion And Limitations

This experiment shows that `llama3.2:3b` can support a basic offline customer-service workflow for e-commerce use cases. The local Ollama setup is privacy-friendly, straightforward to run, and capable of producing usable responses for many standard support questions.

However, the system has important limitations. It cannot access real customer accounts, order history, delivery systems, or official business policies. As a result, it may produce vague answers or confidently invent rules when the prompt lacks concrete policy context.

Based on the scored evaluation, one-shot prompting is the better choice for this chatbot. It produced higher average relevance, coherence, and helpfulness, and it more consistently gave the customer a safe next step. Even so, the system would need stronger grounding, better prompt constraints, or integration with real store documentation before it could be trusted in a production setting.
