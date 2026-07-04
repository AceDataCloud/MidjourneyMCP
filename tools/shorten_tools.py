"""Prompt shortening tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_shorten_result


@mcp.tool()
async def midjourney_shorten(
    prompt: Annotated[
        str,
        Field(
            description="The prompt to analyze and shorten. Midjourney's prompt analyzer reads the prompt, highlights the highest-weighted tokens and produces up to 5 shortened candidate prompts that preserve the dominant ideas."
        ),
    ],
) -> str:
    """Shorten and analyze a Midjourney prompt using Midjourney's built-in prompt analyzer.

    This tool helps optimize long or complex prompts by identifying the most
    important elements and producing up to 5 shortened candidate prompts that
    preserve the dominant ideas.

    Use this when:
    - You have a long prompt and want to identify the most impactful words
    - You want to understand which parts of your prompt carry the most weight
    - You need to simplify a complex prompt while keeping its essence

    Returns:
        Up to 5 shortened candidate prompts derived from the original.
    """
    result = await client.shorten(prompt=prompt)
    return format_shorten_result(result)
