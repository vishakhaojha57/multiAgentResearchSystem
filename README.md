ResearchMind 🔬

ResearchMind is a multi-agent AI research system that automates the research process from web search to a structured, critically reviewed report.

Instead of relying on a single LLM call, ResearchMind uses specialized agents for different stages of the research workflow.

✨ Features
🔍 Search Agent — searches the web for relevant and recent information.
📄 Reader Agent — scrapes and extracts detailed content from relevant sources.
✍️ Writer Chain — converts the gathered research into a structured research report.
🧐 Critic Chain — reviews the generated report and provides a score, strengths, and areas for improvement.
📥 Download Report — download the final report as a Markdown file.
⚡ Rate-limit handling — automatically retries when the API rate limit is temporarily reached.
🛡️ Input/output limits — controls research and report size to reduce unnecessary API usage.
🎨 Clean light UI — simple Streamlit interface for running the complete pipeline.
🏗️ Architecture
                    ┌─────────────────┐
                    │      User       │
                    │ Research Topic  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Search Agent   │
                    │   Web Search    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Reader Agent   │
                    │  Scrape URLs    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Writer Chain   │
                    │ Research Report │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Critic Chain   │
                    │ Review + Score   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Report   │
                    │ + Feedback      │
                    └─────────────────┘
🧠 How It Works
1. Search Agent

The user enters a research topic.

The Search Agent uses the web search tool to find relevant information and sources.

User Topic
    ↓
Search Agent
    ↓
Search Results
2. Reader Agent

The Reader Agent takes the search results and extracts deeper information from the most relevant source.

Search Results
    ↓
Reader Agent
    ↓
Detailed Scraped Content
3. Writer Chain

The collected research is passed to the Writer Chain.

It generates a structured report containing:

Introduction
Key Findings
Conclusion
Sources
Search Results + Scraped Content
              ↓
         Writer Chain
              ↓
       Research Report
4. Critic Chain

The generated report is then reviewed by the Critic Chain.

It provides:

Score out of 10
Strengths
Areas to improve
Overall verdict
Research Report
      ↓
Critic Chain
      ↓
Review + Score
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web application UI
LangChain	Agent and LLM orchestration
Groq	LLM inference
Tavily	Web search
OpenAI-compatible API	LLM interface
Python-dotenv	Environment variable management
📂 Project Structure
Multi-agent-research-system/
│
├── app.py              # Streamlit application and pipeline execution
├── agents.py           # Search, Reader, Writer and Critic components
├── tools.py            # Web search and URL scraping tools
├── requirements.txt    # Python dependencies
├── .gitignore          # Files excluded from Git
├── .env                # API keys (local only, NOT committed)
└── README.md           # Project documentation
⚙️ Installation
1. Clone the repository
git clone https://github.com/vishakhaojha57/Multi-agent-research-system.git
2. Move into the project directory
cd Multi-agent-research-system
3. Create a virtual environment
python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
🔑 API Keys

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

Run Locally

Start the Streamlit application:

streamlit run app.py

The application will open in your browser.

Enter a topic such as:

Latest developments in quantum computing

and click:

Run Research Pipeline
