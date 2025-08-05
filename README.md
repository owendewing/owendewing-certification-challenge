# 🎓 Student Loan AI Assistant

A modern chatbot application that helps users understand student loan repayment plans, with a focus on the new RAP (Repayment Assistance Plan) introduced in the megabill. Built with React frontend and FastAPI backend, using LangChain and LangGraph for intelligent responses.

## Demo

Link to Demo: https://www.loom.com/share/f25edc9ac0ad4b6895af94f617c214ad

## Features

- 🤖 **AI-Powered Chatbot**: Uses GPT-4.1 with LangGraph for intelligent conversations
- 📚 **Expert Knowledge**: Specialized in student loan repayment plans (SAVE, PAYE, IBR, RAP)
- 🔍 **Real-time Search**: Integrates Tavily search for latest news and updates
- 📊 **Plan Comparison**: Expert tool to compare existing plans with the new RAP plan
- ⏱️ **Timeline Simulation**: Tool to simulate loan repayment timelines
- 📝 **Form Processing**: Handles user financial information for personalized analysis
- 🎨 **Modern UI**: Beautiful, responsive chat interface

## Tech Stack

### Frontend
- React 18
- Axios for API calls
- Modern CSS with gradients and animations

### Backend
- FastAPI (Python)
- LangChain & LangGraph
- OpenAI GPT-4.1
- Tavily Search API

### Infrastructure
- Docker & Docker Compose
- Multi-container architecture

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Tavily API key

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd owendewing-certification-challenge
```

### 2. Set up Environment Variables

**Important**: You must create your own `.env` file. The `.env` file is not included in the repository for security reasons.

Copy the example environment file and fill in your API keys:

```bash
cp env.example .env
```

Edit the `.env` file with your actual API keys:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_actual_openai_api_key_here

# Tavily Search API (for real-time information)
TAVILY_API_KEY=your_actual_tavily_api_key_here

# Optional: LangSmith Configuration (for tracing and debugging)
# LANGSMITH_API_KEY=your_langsmith_api_key_here
# LANGSMITH_PROJECT=student-loan-assistant
# LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# Application Configuration
APP_ENV=development
LOG_LEVEL=INFO
MAX_TOKENS=4000
TEMPERATURE=0.7
```

### 3. Run with Docker

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development Setup

### Using uv (Recommended)

This project uses `uv` for Python dependency management. If you don't have `uv` installed:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

#### Backend Development with uv

```bash
# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows

# Run the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Jupyter Notebooks

The project includes Jupyter notebooks for advanced RAG evaluation and experimentation:

```bash
# Install Jupyter dependencies
uv sync

# Start Jupyter
jupyter lab

# Or start Jupyter notebook
jupyter notebook
```

**Important**: When using the notebooks, you'll need to:
1. Select the correct kernel (should be the project's virtual environment)
2. Enter your API keys when prompted by the notebooks
3. The notebooks are in the root directory:
   - `Certification_Challenge.ipynb` - Main challenge notebook
   - `Advanced_Retrieval.ipynb` - Advanced RAG evaluation

### Traditional Python Setup

If you prefer using pip:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### POST /chat
Send a message to the AI assistant.

**Request:**
```json
{
  "message": "What is the new RAP plan?",
  "history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "assistant", 
      "content": "Hi! How can I help you with student loans?"
    }
  ]
}
```

**Response:**
```json
{
  "response": "The RAP (Repayment Assistance Plan) is...",
  "tools_used": ["tavily_search_results_json", "tool_comparison_tool"]
}
```

### GET /health
Health check endpoint.

## Available Tools

The AI assistant has access to several specialized tools:

1. **Tavily Search**: Gets latest news and updates about student loans
2. **Tool Comparison Tool**: Expert comparison of existing plans vs RAP
3. **Timeline Tool**: Simulates loan repayment timelines
4. **Complete Form Tool**: Processes user financial information

## Example Questions

Try asking the assistant:

- "What is the new RAP plan?"
- "How does SAVE compare to the new RAP plan?"
- "What are the latest updates on student loan forgiveness?"
- "Can you simulate my loan repayment timeline?"
- "What are the differences between PAYE and IBR?"

## Project Structure

```
owendewing-certification-challenge/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Styles
│   │   └── index.js        # React entry point
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── data/                   # PDF documents (mounted volume)
├── docker-compose.yml      # Multi-container setup
├── pyproject.toml         # uv project configuration
├── uv.lock               # uv dependency lock file
├── env.example           # Environment variables template
├── Certification_Challenge.ipynb  # Main challenge notebook
├── Advanced_Retrieval.ipynb       # Advanced RAG evaluation
└── README.md             # This file
```

## Troubleshooting

### Common Issues

1. **API Keys Not Working**
   - Ensure your `.env` file is in the root directory
   - Check that API keys are valid and have sufficient credits
   - Verify the `.env` file format (no spaces around `=`)

2. **Docker Build Fails**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild: `docker-compose build --no-cache`

3. **Frontend Can't Connect to Backend**
   - Check that both containers are running: `docker-compose ps`
   - Verify backend is accessible: `curl http://localhost:8000/health`

4. **uv sync Issues**
   - Make sure you're in the project root directory
   - Try: `uv sync --reinstall`
   - Check Python version: `uv python --version`

5. **Jupyter Kernel Issues**
   - Ensure you've run `uv sync` first
   - Check available kernels: `jupyter kernelspec list`
   - Install the project kernel: `uv run jupyter kernelspec install-self`

### Logs

View logs for debugging:

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes as part of the AI Makerspace Certification Challenge.

## Support

For issues related to:
- **API Keys**: Contact OpenAI or Tavily support
- **Docker**: Check Docker documentation
- **uv**: Check [uv documentation](https://docs.astral.sh/uv/)
- **Application**: Review logs and check the troubleshooting section above
