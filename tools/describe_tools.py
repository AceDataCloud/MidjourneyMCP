"""Image description tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_describe_result


@mcp.tool()
async def midjourney_describe(
    image_url: Annotated[
        str,
        Field(
            description="URL of the image to describe. Must be a direct image URL (JPEG, PNG, GIF, etc.), not a web page containing an image."
        ),
    ],
) -> str:
    """Get AI-generated descriptions of an image.

    This analyzes an image and returns 4 alternative text descriptions that
    could be used as prompts to recreate similar images with Midjourney.

    Use this when:
    - You want to understand what prompts might create a similar image
    - You want to reverse-engineer an image's style or composition
    - You need inspiration for prompts based on existing artwork
    - You want to describe an image for documentation

    The descriptions include style tags and aspect ratio parameters that
    Midjourney understands.

    Returns:
        Four alternative descriptions of the image with Midjourney-compatible formatting.
    """
    result = await client.describe(
        image_url=image_url,
    )
    return format_describe_result(result)
