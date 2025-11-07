"""
GitHub Agent for PydanticAI.

This agent demonstrates progressive tool calling complexity:
- Stage 1: Single tool (search_repositories)
- Stage 2: Multiple tools (search_repositories + get_repository_info)
- Stage 3: Tool chaining (all three tools working together)
- Stage 4: With enhanced event tracking for visualization
"""

import os
from pydantic_ai import Agent, RunContext

from ..config import settings
from ..tools import github_tools

# Set Ollama base URL for the agent
os.environ["OLLAMA_BASE_URL"] = f"{settings.ollama_host}/v1"


# ============================================================================
# Agent Setup
# ============================================================================

github_agent = Agent(
    f"ollama:{settings.model_name}",
    retries=settings.ai_max_retries,
)


# ============================================================================
# System Prompt - Evolves across stages
# ============================================================================

@github_agent.system_prompt
def system_prompt() -> str:
    """
    System prompt that explains the agent's capabilities and how to use tools.

    This prompt evolves as we add more tools:
    - Stage 1: Mentions only search_repositories
    - Stage 2: Mentions both search and get_info tools
    - Stage 3: Encourages multi-step reasoning and tool chaining
    """

    # STAGE 3 PROMPT (Full capabilities with tool chaining)
    return """You are a friendly GitHub expert. When users ask about repositories, you search GitHub and present clear, helpful summaries.

When responding:
- Present search results as a clean numbered list with stars, descriptions, and links
- Answer questions directly and conversationally
- Use emojis like ⭐ for stars to make it engaging

Example response format:
"Here are the top Rust projects:

1. **rust-lang/rust** ⭐ 90,234
   The Rust programming language
   https://github.com/rust-lang/rust

2. **denoland/deno** ⭐ 85,612
   A secure runtime for JavaScript and TypeScript
   https://github.com/denoland/deno"

Tool usage:
- Use search_repositories to find projects
- Use get_repository_info for details about specific repos (needs owner/repo from full_name like "facebook/react")
- Use get_repository_issues to show issues (needs owner/repo from full_name)
- For multi-step questions: call tools ONE AT A TIME, using actual results from previous calls
"""

    # STAGE 2 PROMPT (Multiple tools, no chaining emphasis)
    # Uncomment this and comment Stage 3 for the workshop Stage 2 demo
    """
    return '''You are a helpful GitHub assistant that can search for repositories and get detailed information about specific repositories.

Your capabilities:
1. **search_repositories**: Search GitHub for repositories matching a query
   - Use this when the user wants to find repositories
   - Returns a list of repositories with basic info

2. **get_repository_info**: Get detailed information about a specific repository
   - Use this when the user wants details about a specific repo
   - Requires owner and repo name (e.g., "facebook/react")

Choose the appropriate tool based on the user's question:
- Use search_repositories for general searches ("Find React libraries")
- Use get_repository_info for specific repo questions ("Tell me about facebook/react")
'''
    """

    # STAGE 1 PROMPT (Single tool only)
    # Uncomment this and comment Stage 3 for the workshop Stage 1 demo
    """
    return '''You are a helpful GitHub assistant that can search for repositories.

You have one tool available:
- **search_repositories**: Search GitHub for repositories matching a query

Use this tool when users ask you to find repositories. Present the results in a clear, organized way.
'''
    """


# ============================================================================
# STAGE 1: Single Tool Registration
# ============================================================================

@github_agent.tool
async def search_repositories(ctx: RunContext[None], query: str, limit: int = 5) -> dict:
    """
    Search GitHub repositories based on a query string.

    Use this tool when the user wants to find repositories on GitHub.

    Args:
        ctx: PydanticAI run context
        query: Search query (e.g., "React", "machine learning python")
        limit: Maximum number of results to return (default: 5, max: 10)

    Returns:
        Dictionary with total_count and list of repositories
    """
    return await github_tools.search_repositories(query, limit)


# ============================================================================
# STAGE 2: Second Tool Registration
# ============================================================================
# For workshop: Uncomment this during Stage 2 to add the second tool

@github_agent.tool
async def get_repository_info(ctx: RunContext[None], owner: str, repo: str) -> dict:
    """
    Get detailed information about a specific GitHub repository.

    Use this tool when the user wants detailed information about a specific repository.

    Args:
        ctx: PydanticAI run context
        owner: Repository owner username (e.g., "facebook")
        repo: Repository name (e.g., "react")

    Returns:
        Dictionary with detailed repository information
    """
    return await github_tools.get_repository_info(owner, repo)


# ============================================================================
# STAGE 3: Third Tool Registration - Tool Chaining
# ============================================================================
# For workshop: Uncomment this during Stage 3 to enable tool chaining

@github_agent.tool
async def get_repository_issues(
    ctx: RunContext[None],
    owner: str,
    repo: str,
    state: str = "open",
    limit: int = 5
) -> dict:
    """
    Get issues for a specific GitHub repository.

    Use this tool when the user wants to see issues or bugs for a repository.

    Args:
        ctx: PydanticAI run context
        owner: Repository owner username (e.g., "facebook")
        repo: Repository name (e.g., "react")
        state: Issue state - "open", "closed", or "all" (default: "open")
        limit: Maximum number of issues to return (default: 5)

    Returns:
        Dictionary with issue information
    """
    return await github_tools.get_repository_issues(owner, repo, state, limit)
