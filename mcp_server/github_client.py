"""
GitHub client wrapper using PyGithub.
Handles all direct communication with the GitHub API.
"""

import os
from dotenv import load_dotenv
from github import Github, Auth

load_dotenv()


def get_github_client() -> Github:
    """Return an authenticated GitHub client."""
    token = os.getenv("GITHUB_PAT")
    if not token:
        raise ValueError("GITHUB_PAT not found in environment variables.")
    return Github(auth=Auth.Token(token))


def get_current_user():
    """Return the authenticated GitHub user."""
    g = get_github_client()
    return g.get_user()


def list_repos() -> list[dict]:
    """List all repositories for the authenticated user."""
    user = get_current_user()
    repos = []
    for repo in user.get_repos():
        repos.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description or "No description",
            "private": repo.private,
            "url": repo.html_url,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "language": repo.language or "Unknown",
            "open_issues": repo.open_issues_count,
        })
    return repos


def get_repo_details(repo_name: str) -> dict:
    """Get detailed information about a specific repository."""
    user = get_current_user()
    full_name = f"{user.login}/{repo_name}"
    g = get_github_client()
    repo = g.get_repo(full_name)

    return {
        "name": repo.name,
        "full_name": repo.full_name,
        "description": repo.description or "No description",
        "private": repo.private,
        "url": repo.html_url,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "language": repo.language or "Unknown",
        "open_issues": repo.open_issues_count,
        "created_at": str(repo.created_at),
        "updated_at": str(repo.updated_at),
        "default_branch": repo.default_branch,
        "topics": repo.get_topics(),
    }


def get_issues(repo_name: str, state: str = "open") -> list[dict]:
    """Get issues for a specific repository."""
    user = get_current_user()
    full_name = f"{user.login}/{repo_name}"
    g = get_github_client()
    repo = g.get_repo(full_name)

    issues = []
    for issue in repo.get_issues(state=state):
        if issue.pull_request:
            continue
        issues.append({
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "url": issue.html_url,
            "created_at": str(issue.created_at),
            "body": issue.body or "No description",
            "labels": [label.name for label in issue.labels],
        })
    return issues


def create_issue(repo_name: str, title: str, body: str = "") -> dict:
    """
    Create a new issue in a specific repository.

    Args:
        repo_name: Repository name (e.g. 'github-assistant-mcp')
        title: Title of the issue
        body: Optional body/description of the issue

    Returns:
        Dict with created issue details.
    """
    user = get_current_user()
    full_name = f"{user.login}/{repo_name}"
    g = get_github_client()
    repo = g.get_repo(full_name)

    issue = repo.create_issue(title=title, body=body)

    return {
        "number": issue.number,
        "title": issue.title,
        "state": issue.state,
        "url": issue.html_url,
        "created_at": str(issue.created_at),
        "body": issue.body or "",
    }


def get_repo_stats(repo_name: str) -> dict:
    """
    Get stats for a specific repository including commit count,
    contributors, and recent commit activity.

    Args:
        repo_name: Repository name (e.g. 'github-assistant-mcp')

    Returns:
        Dict with repo stats.
    """
    user = get_current_user()
    full_name = f"{user.login}/{repo_name}"
    g = get_github_client()
    repo = g.get_repo(full_name)

    # Contributors
    try:
        contributors = [
            {
                "login": c.login,
                "contributions": c.contributions,
                "url": c.html_url,
            }
            for c in repo.get_contributors()
        ]
    except Exception:
        contributors = []

    # Recent commits (last 10)
    try:
        recent_commits = [
            {
                "sha": c.sha[:7],
                "message": c.commit.message.split("\n")[0],  # first line only
                "author": c.commit.author.name,
                "date": str(c.commit.author.date),
            }
            for c in repo.get_commits()[:10]
        ]
    except Exception:
        recent_commits = []

    # Total commit count
    try:
        total_commits = repo.get_commits().totalCount
    except Exception:
        total_commits = "Unknown"

    return {
        "name": repo.name,
        "total_commits": total_commits,
        "contributors": contributors,
        "recent_commits": recent_commits,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "open_issues": repo.open_issues_count,
        "watchers": repo.watchers_count,
        "size_kb": repo.size,
    }
