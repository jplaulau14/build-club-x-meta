"""
GitHub API tools for PydanticAI agent.

This module contains tool functions that can be used by the GitHub agent
to interact with the GitHub API. Tools are progressively uncommented
during the workshop to demonstrate incremental complexity.
"""

import httpx
from typing import Any


# ============================================================================
# STAGE 1: Single Tool - Foundation
# ============================================================================

async def search_repositories(query: str, limit: int = 5) -> dict[str, Any]:
    """
    Search GitHub repositories based on a query string.

    Args:
        query: Search query (e.g., "React", "machine learning python")
        limit: Maximum number of results to return (default: 5)

    Returns:
        Dictionary containing search results with repository information

    Example:
        >>> await search_repositories("React", limit=3)
        {
            "total_count": 50000,
            "repositories": [
                {
                    "name": "react",
                    "full_name": "facebook/react",
                    "description": "The library for web and native user interfaces",
                    "stars": 220000,
                    "language": "JavaScript",
                    "url": "https://github.com/facebook/react"
                },
                ...
            ]
        }
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit, 10)  # GitHub API max is 100, but we limit for demo
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                params=params,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "PydanticAI-Workshop"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # Format the response for better readability
            repositories = []
            for repo in data.get("items", [])[:limit]:
                repositories.append({
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo.get("description", "No description"),
                    "stars": repo["stargazers_count"],
                    "language": repo.get("language", "Unknown"),
                    "url": repo["html_url"],
                    "owner": repo["owner"]["login"]
                })

            return {
                "total_count": data["total_count"],
                "repositories": repositories
            }

        except httpx.HTTPError as e:
            return {
                "error": f"GitHub API request failed: {str(e)}",
                "total_count": 0,
                "repositories": []
            }


# ============================================================================
# STAGE 2: Multiple Tools - Decision Making
# ============================================================================
# Uncomment this tool during the workshop to demonstrate multiple tool usage

async def get_repository_info(owner: str, repo: str) -> dict[str, Any]:
    """
    Get detailed information about a specific GitHub repository.

    Args:
        owner: Repository owner username (e.g., "facebook")
        repo: Repository name (e.g., "react")

    Returns:
        Dictionary containing detailed repository information

    Example:
        >>> await get_repository_info("facebook", "react")
        {
            "name": "react",
            "full_name": "facebook/react",
            "description": "The library for web and native user interfaces",
            "stars": 220000,
            "forks": 45000,
            "language": "JavaScript",
            "open_issues": 850,
            "created_at": "2013-05-24",
            "updated_at": "2024-01-15",
            "topics": ["react", "frontend", "javascript"],
            "url": "https://github.com/facebook/react"
        }
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "PydanticAI-Workshop"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            return {
                "name": data["name"],
                "full_name": data["full_name"],
                "description": data.get("description", "No description"),
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "language": data.get("language", "Unknown"),
                "open_issues": data["open_issues_count"],
                "watchers": data["watchers_count"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "topics": data.get("topics", []),
                "url": data["html_url"],
                "homepage": data.get("homepage"),
                "license": data.get("license", {}).get("name", "No license"),
                "default_branch": data["default_branch"]
            }

        except httpx.HTTPError as e:
            return {
                "error": f"GitHub API request failed: {str(e)}"
            }


# ============================================================================
# STAGE 3: Tool Chaining - Composed Actions
# ============================================================================
# Uncomment this tool during the workshop to demonstrate tool chaining

async def get_repository_issues(
    owner: str,
    repo: str,
    state: str = "open",
    limit: int = 5
) -> dict[str, Any]:
    """
    Get issues for a specific GitHub repository.

    Args:
        owner: Repository owner username (e.g., "facebook")
        repo: Repository name (e.g., "react")
        state: Issue state - "open", "closed", or "all" (default: "open")
        limit: Maximum number of issues to return (default: 5)

    Returns:
        Dictionary containing issue information

    Example:
        >>> await get_repository_issues("facebook", "react", state="open", limit=3)
        {
            "total_issues": 850,
            "issues": [
                {
                    "number": 12345,
                    "title": "Bug in useEffect",
                    "state": "open",
                    "author": "johndoe",
                    "labels": ["bug", "needs-triage"],
                    "created_at": "2024-01-10",
                    "url": "https://github.com/facebook/react/issues/12345"
                },
                ...
            ]
        }
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": state,
        "per_page": min(limit, 10),
        "sort": "created",
        "direction": "desc"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                params=params,
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "PydanticAI-Workshop"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()

            # Filter out pull requests (GitHub API includes PRs in issues endpoint)
            issues = []
            for item in data:
                if "pull_request" not in item:  # Skip pull requests
                    issues.append({
                        "number": item["number"],
                        "title": item["title"],
                        "state": item["state"],
                        "author": item["user"]["login"],
                        "labels": [label["name"] for label in item.get("labels", [])],
                        "created_at": item["created_at"],
                        "updated_at": item["updated_at"],
                        "comments": item["comments"],
                        "url": item["html_url"],
                        "body_preview": (item.get("body") or "")[:200]  # First 200 chars
                    })

                    if len(issues) >= limit:
                        break

            return {
                "total_issues": len(issues),
                "state_filter": state,
                "issues": issues
            }

        except httpx.HTTPError as e:
            return {
                "error": f"GitHub API request failed: {str(e)}",
                "total_issues": 0,
                "issues": []
            }
