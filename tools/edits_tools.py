"""Image editing tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODE, MidjourneyMode
from core.utils import format_edit_result


@mcp.tool()
async def midjourney_edit(
    image_url: Annotated[
        str,
        Field(description="URL of the image to edit. Must be a direct image URL (not a web page)."),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of how to edit the image. Examples: 'A cat sitting on a table', 'Add a sunset in the background', 'Make it look like a watercolor painting'"
        ),
    ],
    mode: Annotated[
        MidjourneyMode,
        Field(description="Generation mode. 'fast' is recommended."),
    ] = DEFAULT_MODE,
    split_images: Annotated[
        bool,
        Field(
            description="If true, split the result into separate images returned via sub_image_urls."
        ),
    ] = False,
    mask: Annotated[
        str,
        Field(
            description="Optional Base64-encoded mask image. White areas indicate regions to edit and regenerate."
        ),
    ] = "",
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the edit is complete."
        ),
    ] = None,
) -> str:
    """Edit an existing image using Midjourney.

    This allows you to modify an existing image based on a text prompt,
    optionally using a mask to specify which regions to edit.

    Use this when:
    - You want to modify an existing image with AI
    - You want to add or change elements in an image
    - You want to apply style changes to an image
    - You need to edit specific regions using a mask

    For masks:
    - White areas in the mask indicate regions to regenerate
    - Black areas will be preserved from the original

    Returns:
        Task ID and edited image information including URLs and dimensions.
    """
    payload: dict = {
        "action": "generate",
        "image_url": image_url,
        "prompt": prompt,
        "mode": mode,
        "split_images": split_images,
        "callback_url": callback_url,
    }

    if mask:
        payload["mask"] = mask

    result = await client.edit(**payload)
    return format_edit_result(result)
