"""Task query tools for Midjourney API."""

import asyncio
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_task_result


@mcp.tool()
async def midjourney_get_task(
    task_id: Annotated[
        str,
        Field(
            description="The task ID returned from a generation request. This is the 'task_id' field from any midjourney_imagine, midjourney_describe, midjourney_edit, or midjourney_generate_video tool response."
        ),
    ],
) -> str:
    """Query the status and result of a Midjourney generation task.

    Use this to check if a generation is complete and retrieve the resulting
    image/video URLs and metadata.

    Use this when:
    - You want to check if a generation has completed
    - You need to retrieve URLs from a previous generation
    - You want to get the full details of a generated image or video
    - You used async callback and want to check results later

    Returns:
        Task status and generation result including URLs, dimensions, and available actions.
    """
    result = await client.query_task(
        id=task_id,
        action="retrieve",
    )
    # Throttle polling: sleep 5s for incomplete tasks so LLM clients
    # don't burn through poll attempts in seconds.
    response = result.get("response", {})
    is_complete = response.get("success", False)
    if not is_complete:
        await asyncio.sleep(5)
    return format_task_result(result)


@mcp.tool()
async def midjourney_get_tasks_batch(
    task_ids: Annotated[
        list[str],
        Field(description="List of task IDs to query. Maximum recommended batch size is 50 tasks."),
    ],
) -> str:
    """Query multiple Midjourney generation tasks at once.

    Efficiently check the status of multiple tasks in a single request.
    More efficient than calling midjourney_get_task multiple times.

    Use this when:
    - You have multiple pending generations to check
    - You want to get status of several images/videos at once
    - You're tracking a batch of generations

    Returns:
        Status and result information for all queried tasks.
    """
    result = await client.query_task(
        ids=task_ids,
        action="retrieve_batch",
    )

    if "error" in result:
        error = result.get("error", {})
        return f"Error: {error.get('code', 'unknown')} - {error.get('message', 'Unknown error')}"

    lines = [f"Total Tasks: {result.get('count', 0)}", ""]

    for item in result.get("items", []):
        response_info = item.get("response", {})
        lines.extend(
            [
                f"=== Task: {item.get('id', 'N/A')} ===",
                f"Type: {item.get('type', 'N/A')}",
                f"Created At: {item.get('created_at', 'N/A')}",
                f"Success: {response_info.get('success', False)}",
            ]
        )

        if "image_url" in response_info:
            lines.append(f"  Image: {response_info.get('image_url', 'N/A')}")
        elif "descriptions" in response_info:
            lines.append(f"  Descriptions: {len(response_info.get('descriptions', []))} options")

        lines.append("")

    return "\n".join(lines)
