"""Video generation tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODE, VideoMode, VideoResolution
from core.utils import format_video_result


@mcp.tool()
async def midjourney_generate_video(
    image_url: Annotated[
        str,
        Field(
            description="URL of the first frame reference image. This image will be used as the starting point for the video."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of the video to generate. Examples: 'A cat walking on a table', 'Ocean waves crashing on the shore', 'Timelapse of clouds moving'"
        ),
    ],
    mode: Annotated[
        VideoMode,
        Field(description="Generation mode. 'fast' is recommended for most use cases."),
    ] = DEFAULT_MODE,
    resolution: Annotated[
        VideoResolution,
        Field(description="Video resolution. '720p' or '480p'."),
    ] = "720p",
    end_image_url: Annotated[
        str,
        Field(
            description="Optional URL of the last frame reference image. Use this to control where the video ends."
        ),
    ] = "",
    loop: Annotated[
        bool,
        Field(
            description="If true, generate a looping video where the end seamlessly connects to the beginning."
        ),
    ] = False,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video is generated."
        ),
    ] = None,
) -> str:
    """Generate a video from text prompt and reference image using Midjourney.

    This creates an AI-generated video based on your description and a starting
    frame image. You can optionally specify an ending frame for more control.

    Use this when:
    - You want to animate a still image
    - You want to create short video clips from descriptions
    - You need AI-generated video content

    The generation process returns 4 video variations.

    Returns:
        Task ID and video information including cover image and video URLs.
    """
    payload: dict = {
        "action": "generate",
        "prompt": prompt,
        "image_url": image_url,
        "mode": mode,
        "resolution": resolution,
        "loop": loop,
        "callback_url": callback_url,
    }

    if end_image_url:
        payload["end_image_url"] = end_image_url

    result = await client.generate_video(**payload)
    return format_video_result(result)


@mcp.tool()
async def midjourney_extend_video(
    video_id: Annotated[
        str,
        Field(
            description="ID of the video to extend. This is the 'video_id' field from a previous video generation result."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description for the video extension. This guides how the video should continue."
        ),
    ],
    video_index: Annotated[
        int,
        Field(
            description="Index of the video to extend from the video_urls array. 0-indexed, default is 0 (first video)."
        ),
    ] = 0,
    mode: Annotated[
        VideoMode,
        Field(description="Generation mode."),
    ] = DEFAULT_MODE,
    end_image_url: Annotated[
        str,
        Field(
            description="Optional URL of an image to use as the final frame of the extended video."
        ),
    ] = "",
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the video extension is complete."
        ),
    ] = None,
) -> str:
    """Extend an existing Midjourney video to make it longer.

    This allows you to continue a previously generated video by adding more
    frames based on your prompt description.

    Use this when:
    - You want to make a video longer
    - You want to continue the story or motion from an existing video
    - You need to add more content to a short clip

    Returns:
        Task ID and extended video information including new video URLs.
    """
    payload: dict = {
        "action": "extend",
        "video_id": video_id,
        "video_index": video_index,
        "prompt": prompt,
        "mode": mode,
        "callback_url": callback_url,
    }

    if end_image_url:
        payload["end_image_url"] = end_image_url

    result = await client.generate_video(**payload)
    return format_video_result(result)
