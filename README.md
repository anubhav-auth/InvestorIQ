Market Insights Analyst
=======================

An autonomous, multi-agent system that emulates the workflow of a financial analyst. The system ingests and processes a variety of financial data, uses specialized agents to perform research and analysis, and generates a coherent, evidence-based narrative to answer complex user queries, thereby providing actionable market insights.

* * * * *

🚀 Features
-----------

-   **Multi-Agent System**: Utilizes a collaborative multi-agent framework where each agent has a distinct role, coordinated by a central manager.

-   **Data Ingestion**: Ingests and processes financial news, market data, and corporate filings.

-   **Specialized Agents**: Includes a Financial News Researcher Agent and a Stock Data Analyst Agent.

-   **Evidence-Based Narratives**: Generates coherent, evidence-based narratives to answer complex user queries.

-   **Web Interface**: A user-friendly web interface built with Streamlit to interact with the system.

* * * * *

🛠️ Technology Stack
--------------------

| Component | Technology |
| --- | --- |
| **Orchestration** | LangChain |
| **Data Framework** | LlamaIndex |
| **Vector Store** | FAISS (`faiss-cpu` or `faiss-gpu`) |
| **Web Framework** | FastAPI |
| **Embedding Model** | `BAAI/bge-large-en-v1.5` |
| **LLM** | Gemini 2.5 Pro |
| **Containerization** | Docker & Docker Compose |
| **Frontend** | Streamlit |
| **Evaluation** | RAGAS |

* * * * *

⚙️ Getting Started
------------------

### Prerequisites

-   Python 3.8+

-   An environment with the required packages installed.

-   API keys for Google (for Gemini) and a news source (if you modify the ingestion script).

### 1\. Clone the repository

Bash

```
git clone https://github.com/your-username/Market-Insights-Analyst.git
cd Market-Insights-Analyst

```

### 2\. Create a virtual environment and install dependencies

Bash

```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

```

### 3\. Set up your environment variables

Create a `.env` file in the root directory and add your API keys:

```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

```

### 4\. Ingest your data

Place your news articles (as `.txt` files) in the `data/news_articles` directory. Then, run the ingestion script to create the vector store:

Bash

```
python ingestion_scripts/ingest_news.py

```

### 5\. Run the application

The application consists of a FastAPI backend and a Streamlit frontend.

**To run the backend:**

Bash

```
uvicorn api.main:app --reload

```

**To run the frontend in a separate terminal:**

Bash

```
streamlit run frontend/app.py

```

Now, you can open your browser and navigate to the Streamlit URL (usually `http://localhost:8501`) to start asking financial questions!

* * * * *

🚢 Docker Deployment
--------------------

For a more robust and reproducible setup, you can use Docker and Docker Compose.

1.  **Build the Docker images:**

Bash

```
docker-compose build

```

1.  **Run the containers:**

Bash

```
docker-compose up

```

This will start both the backend and frontend services. The Streamlit app will be available at `http://localhost:8501`.

* * * * *

🧪 Evaluation
-------------

The project includes a plan for evaluating the RAG pipeline using the RAGAS framework. You can create an evaluation script in the `evaluation` directory to measure metrics like **Faithfulness**, **Context Precision**, and **Answer Relevancy**. This will help you to quantitatively assess the performance of the system.