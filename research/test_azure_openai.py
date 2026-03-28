"""
Test script to verify Azure OpenAI credentials are working correctly.
Run: python research/test_azure_openai.py
"""

from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

AZURE_OPENAI_API_KEY      = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT     = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION  = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

# ── Check all vars present ───────────────────────────────────────────────────
missing = []
for var, val in {
    "AZURE_OPENAI_API_KEY"       : AZURE_OPENAI_API_KEY,
    "AZURE_OPENAI_ENDPOINT"      : AZURE_OPENAI_ENDPOINT,
    "AZURE_OPENAI_API_VERSION"   : AZURE_OPENAI_API_VERSION,
    "AZURE_OPENAI_CHAT_DEPLOYMENT": AZURE_OPENAI_CHAT_DEPLOYMENT,
}.items():
    if not val:
        missing.append(var)

if missing:
    print(f"❌ Missing environment variables: {', '.join(missing)}")
    exit(1)

# ── Test connection ──────────────────────────────────────────────────────────
try:
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_CHAT_DEPLOYMENT,
        messages=[{"role": "user", "content": "Say 'Azure OpenAI connection successful!' and nothing else."}],
        max_tokens=20,
    )

    reply = response.choices[0].message.content.strip()

    print("✅ Azure OpenAI connection successful!")
    print(f"   🤖 Deployment   : {AZURE_OPENAI_CHAT_DEPLOYMENT}")
    print(f"   🌐 Endpoint     : {AZURE_OPENAI_ENDPOINT}")
    print(f"   📝 API Version  : {AZURE_OPENAI_API_VERSION}")
    print(f"   💬 Model reply  : {reply}")

except Exception as e:
    print(f"❌ Azure OpenAI connection failed: {e}")
