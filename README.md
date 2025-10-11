-----

# 🤖 Intelligent Monitoring & Alerting for GenAI Systems

A proactive AIOps agent that ingests telemetry data from GenAI applications, answers natural language questions about system health, and automatically generates alerts when anomalies are detected. This project is built to demonstrate a modern, end-to-end AI engineering workflow.

-----

## 📖 Overview

Traditional monitoring systems with fixed dashboards and simple alerts are often insufficient for the dynamic and unpredictable nature of GenAI applications. It's difficult to quickly diagnose issues like cost overruns or performance degradation without deep analysis.

This project solves that problem by creating an intelligent agent that acts as a junior AI operations engineer. It can:

  - **Ingest** real-time data on cost, latency, and token usage.
  - **Analyze** this data using a suite of analytical tools.
  - **Answer** natural language questions like *"Who are the top 3 most expensive users?"*
  - **Proactively Monitor** the system and generate intelligent, human-readable alerts when performance thresholds are breached.

The entire system runs locally, using the powerful Llama 3 model via Ollama for free, reliable, and private inference, with GPU acceleration.

## ✨ Key Features

  - **REST API for Telemetry:** A robust FastAPI endpoint (`/logs`) to ingest and store usage data.
  - **AI Agent for Queries:** A multi-tool LangChain agent (`/agent/query`) that understands natural language questions and intelligently selects the right tool to answer them.
  - **Diagnostic Tools:**
      - `get_system_statistics`: Provides an overall summary of system health (total requests, cost, avg. latency).
      - `find_highest_cost_users`: Identifies top users by cost to pinpoint sources of high expense.
  - **Proactive Anomaly Detection:** A background scheduler runs every 30 seconds to check for threshold breaches (e.g., cost \> $1000/hour).
  - **AI-Generated Alerts:** When an anomaly is detected, the agent uses an LLM to generate a clear, professional alert message explaining the problem.
  - **Local & GPU-Accelerated:** Runs entirely on your local machine using Ollama and an NVIDIA GPU, ensuring privacy, speed, and zero cost.

## 🛠️ Tech Stack & Architecture

The system is designed with a clean, service-oriented architecture.

```mermaid
graph TD
    A[Log Source] -- JSON --> B(FastAPI Ingest API);
    B -- Writes Log --> C[(PostgreSQL Database w/ Docker)];
    D[User Query] -- JSON --> E(FastAPI Agent API);
    E -- Triggers --> F{LangChain Agent};
    F -- Uses Tool --> G[Analysis Functions];
    G -- Queries --> C;
    F -- Sends Prompt to --> H(Ollama LLM Server);
    H -- Returns Response --> F;
    F -- Sends Final Answer --> E;
    I[APScheduler] -- Every 30s --> G;
```

| Component         | Technology                                                                                                  | Purpose                                       |
| ----------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Backend** | \<img src="[https://img.shields.io/badge/FastAPI-0.110-green?logo=fastapi](https://www.google.com/search?q=https://img.shields.io/badge/FastAPI-0.110-green%3Flogo%3Dfastapi)" alt="FastAPI" /\>                       | High-performance REST API                     |
| **Database** | \<img src="[https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql](https://www.google.com/search?q=https://img.shields.io/badge/PostgreSQL-15-blue%3Flogo%3Dpostgresql)" alt="PostgreSQL" /\> & SQLAlchemy   | Data storage and ORM                          |
| **Containerization**| \<img src="[https://img.shields.io/badge/Docker-25.0-blue?logo=docker](https://www.google.com/search?q=https://img.shields.io/badge/Docker-25.0-blue%3Flogo%3Ddocker)" alt="Docker" /\>                         | Running the PostgreSQL database               |
| **AI Orchestration**| \<img src="[https://img.shields.io/badge/LangChain-0.2-orange?logo=langchain](https://www.google.com/search?q=https://img.shields.io/badge/LangChain-0.2-orange%3Flogo%3Dlangchain)" alt="LangChain" /\>               | Building the agent and managing tools         |
| **LLM** | \<img src="[https://img.shields.io/badge/Ollama-0.1-lightgrey?logo=ollama](https://www.google.com/search?q=https://img.shields.io/badge/Ollama-0.1-lightgrey%3Flogo%3Dollama)" alt="Ollama" /\> & Llama 3             | Local, GPU-accelerated language model         |
| **Scheduling** | \<img src="[https://img.shields.io/badge/APScheduler-3.10-purple](https://www.google.com/search?q=https://img.shields.io/badge/APScheduler-3.10-purple)" alt="APScheduler" /\>                           | Running proactive monitoring checks           |

## 🚀 Setup and Installation

### Prerequisites

  - [Git](https://git-scm.com/downloads)
  - [Python 3.10+](https://www.python.org/downloads/)
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - [Ollama](https://ollama.com/download)
  - An NVIDIA GPU with CUDA drivers is recommended for best performance.

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/ai-monitoring-agent.git
cd ai-monitoring-agent
```

### 2\. Create and Activate Virtual Environment

```bash
python -m venv ai_monitoring_env
.\ai_monitoring_env\Scripts\activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Set Up the Database with Docker

First, create a persistent volume to store the data, then run the container.

```bash
docker volume create postgres-data
docker run --name ai-monitoring-db -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -v postgres-data:/var/lib/postgresql/data -d postgres:15
```

### 5\. Download the Local LLM

This will download the Llama 3 model (this may take some time).

```bash
ollama run llama3
```

### 6\. Configure Environment Variables

Create a file named `.env` in the root of the project and add your database URL.

```env
# .env
DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/postgres"
```

## ▶️ How to Run

1.  **Start the FastAPI Server:**
    From the root directory, run:

    ```bash
    uvicorn src.main:app --reload
    ```

    The server will be running at `http://127.0.0.1:8000`.

2.  **Access the Interactive API Docs:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs`.

3.  **Send Sample Data:**
    Use the `POST /logs` endpoint in the docs to send some sample log data.

4.  **Query the Agent:**
    Use the `POST /agent/query` endpoint to ask questions in natural language, such as:

    ```json
    {
      "question": "Who are the top 3 most expensive users?"
    }
    ```

5.  **Watch for Proactive Alerts:**
    Keep an eye on the terminal where Uvicorn is running. Every 30 seconds, the scheduler will run a check. If you send a log with `cost_usd` greater than 1000, you will see an AI-generated alert appear in the terminal\!

## 📸 Demo Screenshots

**Here are the placeholders where you should insert your screenshots.** Take a screenshot of each step and replace the link. You can drag and drop images directly into a GitHub issue or comment to get a URL.

1.  **The Interactive API Docs showing all endpoints.**

2.  **DBeaver showing the log data saved in the PostgreSQL table.**

3.  **The final, summarized answer from the agent in the API docs response.**

4.  **The AI-generated alert appearing in the terminal from the proactive scheduler.**

## 🔮 Future Work

  - [ ] **More Tools:** Add more diagnostic tools, such as `find_highest_latency_users` or `get_error_rate`.
  - [ ] **Real-time Pipeline:** Replace the REST API for ingestion with a real-time streaming solution like Kafka or RabbitMQ for higher throughput.
  - [ ] **Frontend Dashboard:** Build a simple UI with Streamlit or React to visualize the data and interact with the agent.
  - [ ] **Advanced Anomaly Detection:** Implement more sophisticated statistical models (e.g., Isolation Forest) instead of simple thresholds.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
