"""
Test the full agent pipeline without FastAPI.
Run: python research/test_agent.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.agent import ask

print("Testing agent pipeline...")
print("=" * 50)

response = ask("List all my repositories")
print("Response:", response)