"""
LangChain agent that connects to the MCP server
and uses Azure OpenAI to answer GitHub-related questions.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from pydantic import create_model

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

load_dotenv()

# ── Project root (always absolute) ───────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful GitHub assistant. You help users explore and understand their GitHub repositories.

You have access to the following tools:
- tool_list_repos: List all repositories for the authenticated GitHub user
- tool_get_repo_details: Get detailed information about a specific repository
- tool_get_issues: Get issues for a specific repository (open, closed, or all)
- tool_create_issue: Create a new issue in a specific repository
- tool_get_repo_stats: Get commit count, contributors and recent activity for a repo

Guidelines:
- Always use the tools to fetch real data before answering
- If the user asks about a specific repo, use tool_get_repo_details
- If the user asks about issues, use tool_get_issues
- Be concise and structured in your responses
- If a repository is not found, let the user know clearly
"""


# ── Azure OpenAI LLM ─────────────────────────────────────────────────────────
def get_llm() -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        temperature=0.3,
    )


# ── Convert MCP tools → LangChain tools ─────────────────────────────────────
async def get_langchain_tools(session: ClientSession) -> list:
    """Fetch tools from MCP server and wrap them as LangChain StructuredTools."""
    mcp_tools = await session.list_tools()
    langchain_tools = []

    for tool in mcp_tools.tools:
        tool_name = tool.name
        tool_description = tool.description or ""
        input_schema = tool.inputSchema or {}
        properties = input_schema.get("properties", {})
        required = input_schema.get("required", [])

        def make_tool_func(name):
            async def tool_func(**kwargs) -> str:
                result = await session.call_tool(name, arguments=kwargs)
                if result.content:
                    return result.content[0].text
                return "No result returned."
            return tool_func

        field_definitions = {}
        for prop_name in properties:
            default = ... if prop_name in required else None
            field_definitions[prop_name] = (str, default)

        ArgsSchema = create_model(
            f"{tool_name}_schema", **field_definitions
        ) if field_definitions else None

        lc_tool = StructuredTool(
            name=tool_name,
            description=tool_description,
            coroutine=make_tool_func(tool_name),
            args_schema=ArgsSchema,
        )
        langchain_tools.append(lc_tool)

    return langchain_tools


# ── Main agent runner ─────────────────────────────────────────────────────────
async def run_agent(user_input: str, chat_history: list = []) -> str:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        env={
            **os.environ,
            "PYTHONPATH": PROJECT_ROOT,
        },
    )

    # Change working directory to project root so module imports work
    original_cwd = os.getcwd()
    os.chdir(PROJECT_ROOT)

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools = await get_langchain_tools(session)
                llm = get_llm()

                messages = [SystemMessage(content=SYSTEM_PROMPT)]
                messages.extend(chat_history)
                messages.append(HumanMessage(content=user_input))

                agent = create_react_agent(llm, tools)
                result = await agent.ainvoke({"messages": messages})

                ai_messages = [
                    m for m in result["messages"]
                    if isinstance(m, AIMessage)
                ]

                if ai_messages:
                    return ai_messages[-1].content

                return "No response generated."
    finally:
        os.chdir(original_cwd)


# ── Helper to run from sync context ──────────────────────────────────────────
def ask(user_input: str, chat_history: list = []) -> str:
    """Run agent in a separate thread to avoid event loop conflicts with FastAPI."""
    import concurrent.futures

    def run_in_new_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(run_agent(user_input, chat_history))
        finally:
            loop.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_in_new_loop)
        return future.result(timeout=120)
