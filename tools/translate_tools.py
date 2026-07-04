"""Translation tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_translate_result


@mcp.tool()
async def midjourney_translate(
    content: Annotated[
        str,
        Field(
            description="Chinese text to translate to English. This is useful for converting Chinese prompts to English for better Midjourney results."
        ),
    ],
) -> str:
    """Translate Chinese text to English for use as Midjourney prompts.

    Midjourney works best with English prompts. This tool helps translate
    Chinese descriptions to English, optimized for image generation.

    Use this when:
    - You have a Chinese description that needs translation
    - You want to convert Chinese prompts to English
    - You need English prompts for better Midjourney results

    Returns:
        Translated English text ready to use as a Midjourney prompt.
    """
    result = await client.translate(
        content=content,
    )
    return format_translate_result(result)
