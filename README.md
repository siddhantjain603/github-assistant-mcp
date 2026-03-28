# GitHub Assistant MCP

> **AI-powered GitHub assistant** that answers questions about GitHub repositories using Model Context Protocol (MCP), LangChain, Azure OpenAI, and FastAPI.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688)](https://fastapi.tiangolo.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4)](https://azure.microsoft.com/en-us/products/ai-services/openai-service/)
[![LangChain](https://img.shields.io/badge/LangChain-Community-1f425f)](https://python.langchain.com/)
[![GitHub API](https://img.shields.io/badge/GitHub-API-181717)](https://docs.github.com/en/rest)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🎯 Overview

**GitHub Assistant MCP** is a question-answering system that lets users ask questions about their GitHub repositories and receive helpful answers. It uses an MCP server to expose GitHub tools, which are then used by a LangChain agent powered by Azure OpenAI to provide intelligent responses about repositories, issues, and statistics.

### Key Capabilities

- **GitHub API Integration**: Access to repository data, issues, and statistics via PyGitHub
- **MCP Tools**: Exposes GitHub operations as MCP tools (list repos, get details, issues, create issues, stats)
- **Azure OpenAI Agent**: Uses LangChain and Azure OpenAI to understand and answer questions
- **FastAPI Backend**: REST API for chat functionality
- **Web Frontend**: Simple HTML interface for interacting with the assistant

---

## ✨ Features

- ✅ **Repository Exploration** - List and get details about GitHub repositories
- ✅ **Issue Management** - View and create issues in repositories
- ✅ **Repository Statistics** - Get commit counts, contributors, and activity data
- ✅ **MCP Protocol** - Uses Model Context Protocol for tool exposure
- ✅ **Azure OpenAI Integration** - Leverages Azure OpenAI for natural language understanding
- ✅ **LangChain Agent** - ReAct agent that uses tools to gather information
- ✅ **FastAPI Backend** - RESTful API for chat interactions
- ✅ **Web Interface** - Simple HTML frontend for user interaction
- ✅ **Chat History** - Maintains conversation context

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Web Frontend                        │
│              (HTML/JavaScript)                       │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│               FastAPI Backend                        │
│  ┌───────────────────────────────────────────────┐  │
│  │  USER MESSAGE                                │  │
│  └──────────────┬────────────────────────────────┘  │
│                 │                                    │
│                 ▼                                    │
│  ┌───────────────────────────────────────────────┐  │
│  │  LANGCHAIN AGENT                             │  │
│  │  • Processes query with chat history         │  │
│  │  • Uses Azure OpenAI for reasoning           │  │
│  │  • Calls MCP tools as needed                │  │
│  └──────────────┬────────────────────────────────┘  │
│                 │                                    │
│                 ▼                                    │
│  ┌───────────────────────────────────────────────┐  │
│  │  MCP SERVER (GitHub Tools)                   │  │
│  │  • tool_list_repos: List user repositories   │  │
│  │  • tool_get_repo_details: Get repo info      │  │
│  │  • tool_get_issues: Fetch issues             │  │
│  │  • tool_create_issue: Create new issues      │  │
│  │  • tool_get_repo_stats: Get repo statistics  │  │
│  └──────────────┬────────────────────────────────┘  │
│                 │                                    │
│                 ▼                                    │
│  ┌───────────────────────────────────────────────┐  │
│  │  GITHUB API                                  │  │
│  │  • Repository data                           │  │
│  │  • Issues and PRs                            │  │
│  │  • Commit statistics                         │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Query**: User asks a question via web interface
2. **API Processing**: FastAPI receives message and calls LangChain agent
3. **Agent Reasoning**: Azure OpenAI processes query and determines which tools to use
4. **Tool Execution**: MCP server calls GitHub API via PyGitHub library
5. **Response Generation**: Agent synthesizes information into natural language response
6. **Display**: Response shown in web interface with chat history maintained

---

## 📦 Prerequisites

- **Python**: 3.11 or higher
- **Azure OpenAI Account** with:
  - Azure OpenAI resource created
  - GPT model deployed (e.g., gpt-4, gpt-3.5-turbo)
  - API key and endpoint information
- **GitHub Account** with:
  - Personal access token with appropriate permissions
  - Access to repositories you want to query

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/github-assistant-mcp.git
cd github-assistant-mcp
```

### Step 2: Create and Activate Virtual Environment using UV

```bash
uv init
uv venv

# Windows
source .venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Step 1: Create `.env` File

```bash
# Windows
echo. > .env

# Mac/Linux
touch .env
```

### Step 2: Add Environment Variables

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token_here

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=your_gpt_deployment_name
```

### Step 3: GitHub Token Setup

Create a GitHub Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope for private repositories
3. Copy the token to your `.env` file as `GITHUB_TOKEN`

### Step 4: Azure OpenAI Setup

1. Create an Azure OpenAI resource in the Azure portal
2. Deploy a GPT model (gpt-4 or gpt-3.5-turbo recommended)
3. Note the endpoint URL, API key, and deployment name
4. Add these to your `.env` file

---

## 💻 Usage

### Run the Application

```bash
# From the project root directory
python -m api.main
```

The application will start the FastAPI server at `http://localhost:8000`

### Using the Web Interface

1. Open `http://localhost:8000` in your browser
2. Type questions about your GitHub repositories in the chat input
3. The assistant will use GitHub tools to gather information and respond

### Example Questions

- "List all my repositories"
- "Tell me about the github-assistant-mcp repository"
- "What are the open issues in my project?"
- "Create an issue titled 'Bug fix needed' in my repo"
- "Get statistics for the main repository"

### API Endpoints

- `GET /health` - Health check endpoint
- `POST /chat` - Send a chat message
- `GET /history` - Get chat history
- `POST /reset` - Clear chat history

---

## 📂 Project Structure

```
github-assistant-mcp/
│
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Python dependencies
├── setup.sh                # Setup script for project structure
├── LICENSE                 # Apache License 2.0
├── README.md               # This file
│
├── mcp_server/            # MCP server implementation
│   ├── __init__.py
│   ├── server.py           # MCP server with GitHub tools
│   └── github_client.py    # GitHub API client functions
│
├── agent/                  # LangChain agent
│   ├── __init__.py
│   └── agent.py            # Azure OpenAI agent with MCP tool integration
│
├── api/                    # FastAPI backend
│   ├── __init__.py
│   └── main.py             # FastAPI app with chat endpoints
│
├── frontend/               # Web frontend
│   └── index.html          # HTML interface for the chat
│
└── research/               # Testing and experimentation
    ├── test_agent.py       # Test agent pipeline
    ├── test_azure_openai.py # Test Azure OpenAI connection
    └── test_github.py      # Test GitHub API integration
```

### Key Files

| File | Purpose |
|------|---------|
| `mcp_server/server.py` | MCP server exposing GitHub tools via stdio transport |
| `agent/agent.py` | LangChain ReAct agent using Azure OpenAI and MCP tools |
| `api/main.py` | FastAPI application serving chat API and static files |
| `frontend/index.html` | Web interface for interacting with the assistant |
| `requirements.txt` | All required Python packages |

---

## 🔧 Troubleshooting

**Problem**: `ImportError` or missing dependencies
```bash
pip install -r requirements.txt
```

**Problem**: GitHub API authentication failed
```
Solution: Ensure GITHUB_TOKEN is correctly set in .env file
and has appropriate permissions for the repositories you're accessing.
```

**Problem**: Azure OpenAI connection failed
```
Solution: Verify AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY,
and AZURE_OPENAI_CHAT_DEPLOYMENT are correctly configured in .env
```

**Problem**: MCP server connection issues
```
Solution: Ensure the MCP server can be launched as a subprocess.
Check that mcp_server/server.py is executable and all imports work.
```

**Problem**: Web interface not loading
```
Solution: Make sure the FastAPI server is running on port 8000
and there are no firewall issues blocking the connection.
```

---

## 🔐 Security Notes

1. **Never commit `.env`** — it contains your GitHub token and Azure OpenAI credentials
2. **Use strong GitHub tokens** — limit token scope to only necessary permissions
3. **Monitor API usage** — Azure OpenAI and GitHub API have usage limits and costs

---

## 📝 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | ✅ | GitHub Personal Access Token |
| `AZURE_OPENAI_ENDPOINT` | ✅ | Azure OpenAI resource endpoint URL |
| `AZURE_OPENAI_API_KEY` | ✅ | Azure OpenAI API key |
| `AZURE_OPENAI_API_VERSION` | ✅ | API version (e.g., 2024-02-15-preview) |
| `AZURE_OPENAI_CHAT_DEPLOYMENT` | ✅ | Name of your GPT model deployment |

---

## 📄 License

This project is licensed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

**Last Updated**: March 2026
**Python**: 3.11+
**Status**: Active
