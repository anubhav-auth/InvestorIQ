Market Insights Analyst
=======================

An autonomous, multi-agent system that emulates the workflow of a financial analyst. The system ingests and processes a variety of financial data, uses specialized agents to perform research and analysis, and generates a coherent, evidence-based narrative to answer complex user queries, thereby providing actionable market insights.

* * * * *

🚀 Features
-----------

-   **Multi-Agent System**: Utilizes a collaborative multi-agent framework where each agent has a distinct role, coordinated by a central manager.

-   **Data Ingestion**: Ingests and processes financial news from local files.

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
| **Vector Store** | FAISS (`faiss-cpu`) |
| **Web Framework** | FastAPI |
| **Embedding Model** | `BAAI/bge-large-en-v1.5` |
| **LLM** | Gemini 2.5 Pro |
| **Containerization** | Docker |
| **Frontend** | Streamlit |
| **Evaluation** | RAGAS |

Export to Sheets

* * * * *

⚙️ Getting Started
------------------

### Prerequisites

-   Python 3.8+

-   An environment with the required packages installed.

-   A Google API key for Gemini.

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

Create a `.env` file in the root directory and add your Google API key:

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

For a more robust and reproducible setup, you can use Docker. The provided `Dockerfile` will set up the entire application, including the data ingestion.

1.  **Build the Docker image:**

    From the root of the project, run the following command:

    Bash

    ```
    docker build -t market-insights-analyst .

    ```

2.  **Run the Docker container:**

    You'll need to pass your Google API key as an environment variable to the container.

    Bash

    ```
    docker run -p 8000:8000 -p 8501:8501 -e GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY" market-insights-analyst

    ```

This command will:

-   Start the container.

-   Expose port `8000` for the FastAPI backend and port `8501` for the Streamlit frontend.

-   The `start.sh` script inside the container will run both the backend and frontend services.

The Streamlit app will be available at `http://localhost:8501`.

* * * * *

🧪 Evaluation
-------------

The project includes a plan for evaluating the RAG pipeline using the RAGAS framework. You can run the evaluation script to measure metrics like **Faithfulness**, **Context Precision**, and **Answer Relevancy**. This helps to quantitatively assess the performance of the system.

To run the evaluation:

Bash

```
python evaluation/evaluate_rag.py
```