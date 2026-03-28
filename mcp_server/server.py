"""
MCP Server exposing GitHub tools.
Tools:
    - tool_list_repos
    - tool_get_repo_details
    - tool_get_issues
    - tool_create_issue
    - tool_get_repo_stats
"""

import json
import sys
import os

# Ensure project root is in path when run as subprocess
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
from mcp_server.github_client import (
    list_repos,
    get_repo_details,
    get_issues,
    create_issue,
    get_repo_stats,
)

# ── Initialise MCP server ────────────────────────────────────────────────────
mcp = FastMCP("github-assistant")


# ── Tool 1: list_repos ───────────────────────────────────────────────────────
@mcp.tool()
def tool_list_repos() -> str:
    """
    List all GitHub repositories for the authenticated user.
    Returns repository name, description, language, visibility, stars and forks.
    """
    try:
        repos = list_repos()
        if not repos:
            return "No repositories found."
        return json.dumps(repos, indent=2)
    except Exception as e:
        return f"Error fetching repositories: {str(e)}"


# ── Tool 2: get_repo_details ─────────────────────────────────────────────────
@mcp.tool()
def tool_get_repo_details(repo_name: str) -> str:
    """
    Get detailed information about a specific GitHub repository.

    Args:
        repo_name: The name of the repository (e.g. 'medical-rag-chatbot-aws-bedrock')
    """
    try:
        details = get_repo_details(repo_name)
        return json.dumps(details, indent=2)
    except Exception as e:
        return f"Error fetching repo details for '{repo_name}': {str(e)}"


# ── Tool 3: get_issues ───────────────────────────────────────────────────────
@mcp.tool()
def tool_get_issues(repo_name: str, state: str = "open") -> str:
    """
    Get issues for a specific GitHub repository.

    Args:
        repo_name: The name of the repository (e.g. 'github-assistant-mcp')
        state: Filter issues by state - 'open', 'closed', or 'all'. Defaults to 'open'.
    """
    try:
        issues = get_issues(repo_name, state=state)
        if not issues:
            return f"No {state} issues found in '{repo_name}'."
        return json.dumps(issues, indent=2)
    except Exception as e:
        return f"Error fetching issues for '{repo_name}': {str(e)}"


# ── Tool 4: create_issue ─────────────────────────────────────────────────────
@mcp.tool()
def tool_create_issue(repo_name: str, title: str, body: str = "") -> str:
    """
    Create a new issue in a specific GitHub repository.

    Args:
        repo_name: The name of the repository (e.g. 'github-assistant-mcp')
        title: The title of the issue
        body: Optional description or body of the issue
    """
    try:
        issue = create_issue(repo_name, title=title, body=body)
        return json.dumps(issue, indent=2)
    except Exception as e:
        return f"Error creating issue in '{repo_name}': {str(e)}"


# ── Tool 5: get_repo_stats ───────────────────────────────────────────────────
@mcp.tool()
def tool_get_repo_stats(repo_name: str) -> str:
    """
    Get statistics for a specific GitHub repository including
    commit count, contributors, and recent commit activity.

    Args:
        repo_name: The name of the repository (e.g. 'github-assistant-mcp')
    """
    try:
        stats = get_repo_stats(repo_name)
        return json.dumps(stats, indent=2)
    except Exception as e:
        return f"Error fetching stats for '{repo_name}': {str(e)}"


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")
