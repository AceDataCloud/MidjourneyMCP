"""Image generation tools for Midjourney API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODE, ImagineAction, MidjourneyMode, MidjourneyVersion
from core.utils import format_imagine_result


@mcp.tool()
async def midjourney_imagine(
    prompt: Annotated[
        str,
        Field(
            description="Description of the image to generate. Be descriptive about style, subject, lighting, and composition. Examples: 'A majestic lion in a savanna at sunset, cinematic lighting', 'Cyberpunk city street at night, neon lights, rain, photorealistic', 'Abstract watercolor painting of mountains and clouds'"
        ),
    ],
    mode: Annotated[
        MidjourneyMode,
        Field(
            description="Generation mode. 'fast' is recommended for most use cases. 'turbo' is faster but uses more credits. 'relax' is slower but cheaper."
        ),
    ] = DEFAULT_MODE,
    translation: Annotated[
        bool,
        Field(
            description="If true, automatically translate non-English prompts to English for better results."
        ),
    ] = False,
    split_images: Annotated[
        bool,
        Field(
            description="If true, split the 2x2 grid result into 4 separate images returned via sub_image_urls."
        ),
    ] = False,
    timeout: Annotated[
        int | None,
        Field(description="Timeout in seconds for the API to return data. Default is 480."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the image is generated."
        ),
    ] = None,
    version: Annotated[
        MidjourneyVersion | None,
        Field(
            description="Midjourney model version to use. '8' is the latest V8 Alpha with HD and ultra quality support. Leave unset to use Midjourney's default."
        ),
    ] = None,
    hd: Annotated[
        bool,
        Field(
            description="Enable HD mode (V8 only). Generates higher resolution images at 4x cost. Requires version='8'."
        ),
    ] = False,
    quality: Annotated[
        str | None,
        Field(
            description="Image quality level. For V8: '1' (standard) or '4' (ultra, 4x cost). For older versions: '.25', '.5', or '1'. HD + quality '4' = 16x cost."
        ),
    ] = None,
    style_reference: Annotated[
        bool,
        Field(
            description="Whether the prompt includes --sref style reference. In V8 this incurs 4x cost."
        ),
    ] = False,
    moodboard: Annotated[
        bool,
        Field(
            description="Whether using moodboard feature (V8 only, multiple reference images). Incurs 4x cost."
        ),
    ] = False,
) -> str:
    """Generate AI images from a text prompt using Midjourney.

    This is the primary way to create images - describe what you want and Midjourney
    will generate a 2x2 grid of 4 image variations.

    Use this when:
    - You want to create new images from a text description
    - You have a creative vision to visualize
    - You need AI-generated artwork or illustrations

    For image transformations like upscaling or variations, use midjourney_transform instead.

    Returns:
        Task ID and generated image information including URLs, dimensions, and available actions.
    """
    payload: dict = {
        "prompt": prompt,
        "mode": mode,
        "translation": translation,
        "split_images": split_images,
        "action": "generate",
    }
    if timeout is not None:
        payload["timeout"] = timeout
    if callback_url is not None:
        payload["callback_url"] = callback_url
    if version is not None:
        payload["version"] = version
    if hd:
        payload["hd"] = hd
    if quality is not None:
        payload["quality"] = quality
    if style_reference:
        payload["style_reference"] = style_reference
    if moodboard:
        payload["moodboard"] = moodboard

    result = await client.imagine(**payload)
    return format_imagine_result(result)


@mcp.tool()
async def midjourney_transform(
    image_id: Annotated[
        str,
        Field(
            description="ID of the image to transform. This is the 'image_id' field from a previous generation result."
        ),
    ],
    action: Annotated[
        ImagineAction,
        Field(
            description="Transformation action to perform. Options include:\n"
            "- upscale1/2/3/4: Upscale one of the 4 images (top-left=1, top-right=2, bottom-left=3, bottom-right=4)\n"
            "- upscale_2x/4x: Further upscale an already upscaled image by 2x or 4x\n"
            "- variation1/2/3/4: Create variations of one of the 4 images\n"
            "- variation_subtle/strong: Create subtle or strong variations after upscaling\n"
            "- reroll: Regenerate all 4 images with the same prompt\n"
            "- zoom_out_2x/1_5x: Zoom out the image by 2x or 1.5x\n"
            "- pan_left/right/up/down: Pan the image in a direction"
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Optional prompt for the transformation. Used with variation_region action."
        ),
    ] = "",
    mask: Annotated[
        str,
        Field(
            description="Base64-encoded mask image for variation_region action. White areas indicate regions to regenerate."
        ),
    ] = "",
    mode: Annotated[
        MidjourneyMode,
        Field(description="Generation mode for the transformation."),
    ] = DEFAULT_MODE,
) -> str:
    """Transform an existing Midjourney image with various operations.

    This allows you to upscale, create variations, zoom, or pan existing images
    generated by Midjourney.

    Use this when:
    - You want to upscale one of the 4 images from a generation
    - You want to create variations of a specific image
    - You want to zoom out or pan an image
    - You want to regenerate with the same prompt

    Workflow example:
    1. Generate with midjourney_imagine -> get image_id
    2. Upscale favorite: midjourney_transform(image_id, "upscale2")
    3. Further upscale: midjourney_transform(new_image_id, "upscale_4x")

    Returns:
        Task ID and transformed image information.
    """
    payload: dict = {
        "action": action,
        "image_id": image_id,
        "mode": mode,
    }

    if prompt:
        payload["prompt"] = prompt
    if mask:
        payload["mask"] = mask

    result = await client.imagine(**payload)
    return format_imagine_result(result)


@mcp.tool()
async def midjourney_blend(
    image_urls: Annotated[
        list[str],
        Field(
            description="List of image URLs to blend together. Supports 2-5 images. Images should be pure image URLs (not web pages containing images)."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of how to blend the images. Examples: 'The bear is holding the chainsaw', 'Combine the face with the background'"
        ),
    ] = "",
    mode: Annotated[
        MidjourneyMode,
        Field(description="Generation mode."),
    ] = DEFAULT_MODE,
) -> str:
    """Blend multiple images together using Midjourney.

    This allows you to combine 2-5 images into a new creative fusion.

    Use this when:
    - You want to merge elements from multiple images
    - You want to create composite images
    - You want to blend styles or subjects together

    Example:
    - Blend a bear image with a chainsaw image with prompt "The bear is holding the chainsaw"

    Returns:
        Task ID and blended image information.
    """
    # Construct prompt with image URLs at the beginning
    full_prompt = " ".join(image_urls)
    if prompt:
        full_prompt += f" {prompt}"

    result = await client.imagine(
        prompt=full_prompt,
        mode=mode,
        action="generate",
    )
    return format_imagine_result(result)


@mcp.tool()
async def midjourney_with_reference(
    reference_image_url: Annotated[
        str,
        Field(
            description="URL of the reference image to use as a base. Must be a direct image URL (not a web page)."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of how to modify or reimagine the reference image. Examples: 'an illustration of a car parked on the beach --iw 2', 'in the style of Van Gogh'"
        ),
    ],
    mode: Annotated[
        MidjourneyMode,
        Field(description="Generation mode."),
    ] = DEFAULT_MODE,
) -> str:
    """Generate images using a reference image as inspiration.

    This allows you to use an existing image as a starting point and modify it
    based on your prompt description.

    Use this when:
    - You want to reimagine an existing image with modifications
    - You want to change the style of an image
    - You want to add or change elements while keeping the composition

    Tips:
    - Use --iw parameter (image weight) to control reference influence (0-2)
    - Higher --iw values make the output more similar to the reference

    Returns:
        Task ID and generated image information.
    """
    # Construct prompt with reference image URL at the beginning
    full_prompt = f"{reference_image_url} {prompt}"

    result = await client.imagine(
        prompt=full_prompt,
        mode=mode,
        action="generate",
    )
    return format_imagine_result(result)
