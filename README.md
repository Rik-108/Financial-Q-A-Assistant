# Financial Literacy Q\&A Assistant 💰📈

## 📌 Project Overview

**Financial Literacy Q\&A Assistant** is an AI-driven, full-stack web application designed to democratize financial education. Built with a Flask backend and an interactive frontend, the system acts as a virtual financial advisor tailored specifically for the Indian market. By leveraging the **Meta Llama-3 (8B Instruct)** model via **IBM Watsonx**, the assistant simplifies complex financial concepts—such as mutual funds, taxation, and stock market basics—into easily digestible, beginner-friendly advice.

## 🚀 Key Features

  * **Enterprise AI Integration:** Utilizes IBM Watsonx.ai to host and query the `meta-llama/llama-3-8b-instruct` foundation model, ensuring high-quality, conversational responses.
  * **Domain-Specific Expertise:** The model is rigidly constrained via advanced system prompts to act as an expert in **Indian Personal Finance**, preventing hallucinations and off-topic conversations.
  * **Asynchronous Chat Interface:** Features a clean, responsive frontend built with **Tailwind CSS** and custom CSS gradients, utilizing JavaScript `fetch` for real-time, non-blocking AI communication.
  * **Robust Backend Routing:** Powered by **Flask** and `flask-cors`, the backend seamlessly handles API requests, parses the LLM output, and cleans the generated text before delivering it to the user UI.

-----

## 🏗️ Architecture Details

### The Application Backend (`app.py`)

The server-side acts as a secure bridge between the user interface and the IBM Watsonx cloud.

  * **Framework:** Uses `Flask` for lightweight routing and `flask-cors` to enable secure cross-origin resource sharing between the frontend UI and the API endpoints.
  * **Response Parsing:** Includes custom Python logic to parse the nested JSON responses from Watsonx and explicitly strip out the original prompt, ensuring the user only sees the finalized answer.

### The Cognitive Engine (`ibm_watsonx_ai`)

The core intelligence relies on zero-shot prompting and strict decoding parameters.

  * **Foundation Model:** `meta-llama/llama-3-8b-instruct`
  * **Decoding Strategy:** Employs `greedy` decoding with a 500-token limit and a repetition penalty of 1.1 to ensure the financial advice is concise, factual, and strictly on-topic.

-----

## 🧠 Prompt Engineering & Guardrails

Unlike open-ended chatbots, this system is engineered for safety and accuracy in the financial domain. The AI's behavior is governed by a strict system prompt:

1.  **Persona Assignment:** Forced to act as an "expert financial advisor for the Indian market."
2.  **Target Audience Constraint:** Instructed to explain concepts simply, assuming the user is a beginner.
3.  **Scope Limitation:** Strictly limited to answering questions related to personal finance, savings, mutual funds, taxation, and stock market basics.
4.  **Refusal Mechanism:** Programmed to politely decline any queries outside of the financial domain, ensuring the tool remains professional and purpose-driven.

-----

## 🛠️ Technology Stack

  * **Backend Framework:** Python 3, Flask, Flask-CORS
  * **AI & LLM:** IBM Watsonx.ai, Meta Llama-3 (8B)
  * **Frontend UI:** HTML5, Tailwind CSS, Vanilla JavaScript
  * **Environment Management:** `python-dotenv`

-----

**Environment Variables Required (`.env`):**

  * `WATSONX_API_KEY`
  * `WATSONX_PROJECT_ID`
  * `WATSONX_URL` (e.g., *[https://us-south.ml.cloud.ibm.com](https://www.google.com/search?q=https://us-south.ml.cloud.ibm.com)*)

-----

## 👥 Contributors


  * **Anik Basu** – Lead Developer, Prompt Engineering, & Full-Stack Integration
