"""Seed retrieval tools for Midjourney API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp


@mcp.tool()
async def midjourney_get_seed(
    image_id: Annotated[
        str,
        Field(
            description="The ID of the generated image to get the seed for. This is the 'image_id' field from a previous imagine result."
        ),
    ],
) -> str:
    """Get the seed value of a previously generated Midjourney image.

    The seed is a numeric value that controls the randomness of generation.
    Using the same seed with the same prompt will produce similar results,
    which is useful for reproducible generation or fine-tuning prompts.

    Use this when:
    - You want to reproduce a specific generation result
    - You need the seed to use with --seed parameter in prompts
    - You want to create variations with consistent base randomness

    Returns:
        The seed value for the specified image.
    """
    result = await client.get_seed(image_id=image_id)
    return json.dumps(result, ensure_ascii=False, indent=2)
