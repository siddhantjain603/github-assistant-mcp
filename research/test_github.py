"""
Test script to verify GitHub PAT is working correctly.
Run: python research/test_github.py
"""

from dotenv import load_dotenv
import os
from github import Github

load_dotenv()

GITHUB_PAT = os.getenv("GITHUB_PAT")

if not GITHUB_PAT:
    print("❌ GITHUB_PAT not found in .env file")
    exit(1)

try:
    g = Github(GITHUB_PAT)
    user = g.get_user()

    print("✅ GitHub connection successful!")
    print(f"   👤 Username     : {user.login}")
    print(f"   📛 Name         : {user.name}")
    print(f"   📦 Public Repos : {user.public_repos}")
    print(f"   👥 Followers    : {user.followers}")
    print()

    print("📂 Your repositories:")
    for repo in user.get_repos():
        print(f"   - {repo.name} ({'private' if repo.private else 'public'})")

except Exception as e:
    print(f"❌ GitHub connection failed: {e}")
