#!/bin/bash

echo "🚀 Setting up github-assistant-mcp project structure..."

# Create directories
mkdir -p mcp_server
mkdir -p agent
mkdir -p api
mkdir -p frontend

# Create Python package init files
touch mcp_server/__init__.py
touch mcp_server/server.py
touch mcp_server/github_client.py

touch agent/__init__.py
touch agent/agent.py

touch api/__init__.py
touch api/main.py

# Create frontend
touch frontend/index.html

# Create root files
touch .env
touch requirements.txt

echo "✅ Folder structure created successfully!"
echo ""
echo "📂 Structure:"
echo "github-assistant-mcp/"
echo "├── mcp_server/"
echo "│   ├── __init__.py"
echo "│   ├── server.py"
echo "│   └── github_client.py"
echo "├── agent/"
echo "│   ├── __init__.py"
echo "│   └── agent.py"
echo "├── api/"
echo "│   ├── __init__.py"
echo "│   └── main.py"
echo "├── frontend/"
echo "│   └── index.html"
echo "├── .env"
echo "└── requirements.txt"