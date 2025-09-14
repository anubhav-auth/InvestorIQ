Of course. Here is a comprehensive project documentation for the **Market Insights Analyst** system, using Gemini 2.5 Pro as the core LLM. This blueprint provides a detailed, step-by-step guide to help you start working immediately.

* * * * *

### **Project Documentation: The Market Insights Analyst**

#### **1\. Project Vision & Goal**

**Problem Statement:** Retail investors and financial analysts are often overwhelmed by the sheer volume of financial news, market data, and corporate filings. Standard RAG (Retrieval-Augmented Generation) systems can retrieve isolated facts but often fail to synthesize information from multiple disparate sources to answer complex, multi-step questions (e.g., "How has the recent semiconductor shortage impacted both Nvidia's stock price and its strategic focus according to its latest earnings call?").

**Project Goal:** To build an autonomous, multi-agent system that emulates the workflow of a financial analyst. The system will ingest and process a variety of financial data, use specialized agents to perform research and analysis, and generate a coherent, evidence-based narrative to answer complex user queries, thereby providing actionable market insights.

#### **2\. System Architecture**

The system is designed around a collaborative multi-agent framework where each agent has a distinct role, coordinated by a central manager. This "separation of concerns" allows for a more robust and scalable solution.

**Architectural Flow:**

1.  **User Query**: The process begins with a user submitting a complex financial question through the frontend.

2.  **API Endpoint (FastAPI)**: The query is received by a FastAPI backend, which validates the request.

3.  **Manager Agent (LangChain)**: The query is passed to a Manager Agent. Its job is to decompose the complex query into a logical sequence of tasks.

4.  **Task Delegation**: The Manager Agent delegates these tasks to specialized agents:

    -   **Financial News Researcher Agent**: This agent is tasked with finding relevant news articles. It queries a dedicated FAISS vector store containing up-to-date news.

    -   **Stock Data Analyst Agent**: This agent retrieves historical and current stock price data using a tool built around the `yfinance` library. It can perform basic analyses like calculating moving averages or identifying recent price volatility.

    -   **SEC Filing Researcher Agent (Optional but recommended for complexity)**: This agent queries a separate vector store containing corporate filings (e.g., 10-K, 10-Q reports) to extract official company statements and financial figures.

5.  **Data Aggregation**: The Manager Agent collects the structured outputs (e.g., JSON objects with retrieved text, data points, and sources) from the specialized agents.

6.  **Synthesis by Writer Agent**: The aggregated, multi-source information is passed to a final **Writer Agent**. This agent's sole purpose is to synthesize all the provided context into a comprehensive, well-structured, and easy-to-read report.

7.  **Response**: The final report is sent back through the API to the frontend for the user to view.

#### **3\. Technology Stack**

| Component | Technology | Rationale & Key Features |
| --- | --- | --- |
| **Orchestration** | LangChain | Essential for its powerful agent creation tools (`create_openai_functions_agent`), tool definition capabilities, and managing complex chains of logic. |
| **Data Framework** | LlamaIndex | Chosen for its superior and specialized data connectors and indexing capabilities, perfect for ingesting and structuring news articles and PDFs of financial reports. |
| **Vector Store** | FAISS (`faiss-cpu` or `faiss-gpu`) |

Offers high-speed similarity search required for a responsive system handling large volumes of text data. More performant than ChromaDB at scale^1^^1^^1^^1^.

 |
| **Web Framework** | FastAPI |

Provides a high-performance, asynchronous API backend with automatic data validation via Pydantic and interactive documentation^2^^2^^2^^2^.

 |
| **Embedding Model** | `BAAI/bge-large-en-v1.5` | A top-tier, open-source embedding model from the MTEB leaderboard that will provide the nuanced semantic understanding necessary for financial text. |
| **LLM** | Gemini 2.5 Pro (via `langchain-google-genai`) | The core reasoning engine for all agents. Its advanced instruction-following and synthesis capabilities are critical for the Manager and Writer agents. |
| **Containerization** | Docker & Docker Compose |

For creating a reproducible and isolated environment for the multi-service application (backend, frontend, etc.), simplifying deployment^3^.

 |
| **Frontend** | Streamlit | Allows for the rapid development of a clean, interactive, and data-centric user interface with minimal frontend code. |
| **Evaluation** | RAGAS |

A specialized framework to quantitatively measure the performance of the RAG pipeline using metrics like

 |

**Faithfulness**, **Context Precision**, and **Answer Relevancy**^4^.

 |

#### **4\. Step-by-Step Implementation Plan**

##### **Phase 1: Data Pipeline & RAG Foundation (Est. 6-8 hours)**

1.  **Project Setup**:

    -   Create a virtual environment and a `requirements.txt` file with all the necessary libraries.

    -   Set up a `.env` file for your API keys (Google API Key, NewsAPI key, etc.).

    -   Structure your project with directories for `data`, `ingestion_scripts`, `api`, `frontend`, and `evaluation`.

2.  **Data Ingestion Scripts (using LlamaIndex)**:

    -   Create `ingest_news.py`: This script will fetch news articles from a news API for a predefined list of tickers (e.g., AAPL, NVDA, GOOG).

    -   Use LlamaIndex's `BeautifulSoupWebReader` or a similar tool to load the content from the article URLs.

    -   Process the text using `SentenceSplitter`.

    -   Load the `bge-large-en-v1.5` embedding model.

    -   Create a FAISS vector index from the news article chunks and save it to disk (e.g., `vector_stores/faiss_news_index`).

    -   (Optional) Create `ingest_filings.py`: Download a few recent 10-K PDF reports and use LlamaIndex's `PDFReader` to ingest them into a separate FAISS index (`vector_stores/faiss_filings_index`).

##### **Phase 2: The Multi-Agent System (using LangChain) (Est. 7-9 hours)**

1.  **Tool Definition (`tools/financial_tools.py`)**:

    -   **News Retriever Tool**: Create a function that loads the persisted FAISS news index and performs a similarity search. Decorate it with LangChain's `@tool` decorator.

    -   **Stock Data Tool**: Create a function using the `yfinance` library that takes a stock ticker and returns the latest price, volume, and key historical data points. Decorate it as a tool.

    -   **(Optional) Filings Retriever Tool**: Create a tool to search the FAISS index for corporate filings.

2.  **Agent Creation (`agents/analyst_agents.py`)**:

    -   **Prompt Engineering**: For each agent, design a detailed system prompt that defines its persona, capabilities, and constraints. For example, the Research Agent's prompt should emphasize breaking down questions and using its tools effectively.

    -   **Specialized Agents**: Use LangChain's `create_openai_functions_agent` (which also works with Gemini models that support function calling) to create the **Financial News Researcher** and **Stock Data Analyst** agents, providing them with their respective tools.

    -   **Writer Agent**: This agent may not need complex tools. Its prompt should instruct it to synthesize the context it receives from the Manager into a final report and to *not* use its own knowledge.

3.  **Orchestration (`agents/manager.py`)**:

    -   This is the most complex part. Use LangChain's LangGraph or a custom chain to manage the workflow.

    -   The Manager Agent will receive the initial query. Its LLM call should be prompted to create a plan and identify which specialized agent to call first.

    -   The output from the first agent is then fed back into the Manager, which decides the next step (e.g., call another agent or pass the aggregated info to the Writer).

##### **Phase 3: Backend, Frontend, and Containerization (Est. 6-8 hours)**

1.  **FastAPI Backend (`api/main.py`)**:

    -   Set up the FastAPI app instance.

    -   Define Pydantic models for your API request and response to ensure data integrity^5^.

    -   Create a `/analyze` endpoint that accepts a user query.

    -   This endpoint will invoke your Manager Agent, wait for the final response from the Writer Agent, and return it.

    -   Use FastAPI's

        `lifespan` events to load your agents and FAISS indexes into memory on startup to avoid cold starts on each request^6^.

2.  **Streamlit Frontend (`frontend/app.py`)**:

    -   Create a simple UI with `st.title`, `st.text_input`, and `st.button`.

    -   When the button is clicked, use the `requests` library to make a POST call to your FastAPI backend.

    -   Display a loading spinner while waiting for the response.

    -   Render the final report using `st.markdown` for a nicely formatted output.

3.  **Dockerization**:

    -   `api/Dockerfile`: Create a Dockerfile for the FastAPI backend.

    -   `frontend/Dockerfile`: Create a Dockerfile for the Streamlit frontend.

    -   `docker-compose.yml`: In the root directory, create a `docker-compose` file to define and link the `backend` and `frontend` services, managing networking and environment variables.

##### **Phase 4: Evaluation (Est. 2-3 hours)**

1.  **Create an Evaluation Suite (`evaluation/evaluate_rag.py`)**:

    -   Define a small dataset of at least 5-10 complex questions.

    -   For each question, manually prepare the "ground truth" context---the key pieces of information that the RAG system *should* retrieve to answer the question accurately.

    -   Programmatically run your Research Agent against each question.

    -   Use the RAGAS library to compare the agent's retrieved context against your ground truth to calculate `Context Precision` and `Context Recall`.

    -   Use RAGAS to evaluate the generated answer from the Writer Agent for `Faithfulness` to the retrieved context.

2.  **Document Results**:

    -   Add an "Evaluation" section to your `README.md`.

    -   Present the results in a table and explain what they mean. This demonstrates a rigorous, engineering-focused approach to building AI.

* * * * *