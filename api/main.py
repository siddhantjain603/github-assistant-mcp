"""
FastAPI backend for the GitHub Assistant MCP chatbot.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
import logging
import traceback
import os

from agent.agent import ask

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="GitHub Assistant MCP",
    description="AI-powered GitHub assistant using MCP, LangChain and Azure OpenAI",
    version="1.0.0",
)

# ── In-memory chat history ────────────────────────────────────────────────────
chat_history: list = []


# ── Request / Response schemas ────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    history_length: int


class HistoryMessage(BaseModel):
    role: str
    content: str


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "GitHub Assistant MCP"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    global chat_history

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    logger.info(f"User: {request.message}")

    try:
        response = ask(request.message, chat_history)

        chat_history.append(HumanMessage(content=request.message))
        chat_history.append(AIMessage(content=response))

        logger.info(f"Agent: {response}")

        return ChatResponse(
            response=response,
            history_length=len(chat_history),
        )

    except Exception as e:
        # Log full traceback so we can see the real error
        full_trace = traceback.format_exc()
        logger.error(f"Agent error:\n{full_trace}")
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}\n\n{full_trace}")


@app.get("/history", response_model=list[HistoryMessage])
def get_history():
    return [
        HistoryMessage(
            role="user" if isinstance(msg, HumanMessage) else "assistant",
            content=msg.content,
        )
        for msg in chat_history
    ]


@app.post("/reset")
def reset_history():
    global chat_history
    chat_history = []
    return {"message": "Chat history cleared successfully."}


# ── Serve frontend ────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))
