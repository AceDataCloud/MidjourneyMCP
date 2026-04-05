"""Informational tools for Midjourney API."""

from core.server import mcp


@mcp.tool()
async def midjourney_list_actions() -> str:
    """List all available Midjourney API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Midjourney MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    # Last updated: 2026-04-05
    return """Available Midjourney Actions and Tools:

Image Generation:
- midjourney_imagine: Generate images from a text prompt (creates 2x2 grid)
- midjourney_transform: Transform existing images (upscale, variation, zoom, pan)
- midjourney_blend: Blend multiple images together
- midjourney_with_reference: Generate using a reference image as inspiration

Image Editing:
- midjourney_edit: Edit an existing image with a text prompt
- midjourney_describe: Get AI descriptions of an image (reverse prompt)

Video Generation:
- midjourney_generate_video: Generate video from text and reference image
- midjourney_extend_video: Extend an existing video to make it longer

Translation:
- midjourney_translate: Translate Chinese text to English for prompts

Task Management:
- midjourney_get_task: Check status of a single generation
- midjourney_get_tasks_batch: Check status of multiple generations

Information:
- midjourney_list_actions: Show this action reference (you are here)
- midjourney_get_prompt_guide: Show how to write effective prompts

Workflow Examples:
1. Quick image: midjourney_imagine → midjourney_transform (upscale)
2. Image variations: midjourney_imagine → midjourney_transform (variation)
3. Image fusion: midjourney_blend with multiple image URLs
4. Style transfer: midjourney_with_reference with style prompt
5. Video creation: midjourney_generate_video → midjourney_extend_video
"""


@mcp.tool()
async def midjourney_get_prompt_guide() -> str:
    """Get guidance on writing effective prompts for Midjourney.

    Shows how to structure prompts and use parameters for best results.
    Following this guide helps Midjourney understand your creative vision.

    Returns:
        Complete guide with prompt structure, parameters, and examples.
    """
    # Last updated: 2026-04-05
    return """Midjourney Prompt Guide:

Prompt Structure:
- Start with the main subject
- Add descriptive details (style, lighting, mood)
- Include artistic references if desired
- Add parameters at the end

Common Parameters:
- --ar X:Y: Aspect ratio (e.g., --ar 16:9 for widescreen, --ar 9:16 for portrait)
- --v 5/5.1/5.2/6: Model version (higher = newer)
- --q 0.25/0.5/1/2: Quality (higher = more detail, slower)
- --s 0-1000: Stylize amount (higher = more artistic)
- --iw 0-2: Image weight for reference images (higher = more similar)
- --no X: Negative prompt (exclude elements)
- --tile: Create seamless tileable patterns

Example Prompts by Style:

Photorealistic:
"Professional headshot of a business executive, studio lighting, neutral background, 8k, photorealistic --ar 1:1 --v 6"

Digital Art:
"Futuristic cyberpunk city at night, neon lights reflecting on wet streets, flying cars, highly detailed --ar 16:9 --s 750"

Oil Painting:
"Serene countryside landscape with rolling hills and a small cottage, impressionist oil painting style, warm golden hour lighting --ar 3:2"

Fantasy:
"Ancient dragon perched on a mountain peak, scales shimmering with magical energy, epic fantasy art, detailed --ar 2:3 --s 500"

Abstract:
"Flowing liquid metal forms intertwining, iridescent colors, abstract sculpture, studio lighting --ar 1:1 --s 1000"

Product Photography:
"Luxury watch on black velvet, studio product photography, dramatic lighting, reflections --ar 4:5 --q 2"

Tips for Best Results:
1. Be specific about what you want
2. Include lighting descriptions (golden hour, dramatic, soft, studio)
3. Mention camera/lens style for photos (35mm, wide angle, macro)
4. Reference art styles or artists for creative work
5. Use negative prompts (--no) to exclude unwanted elements
6. Experiment with stylize values for different aesthetics
7. Try different aspect ratios for different compositions
"""


@mcp.tool()
async def midjourney_list_transform_actions() -> str:
    """List all available transformation actions for Midjourney images.

    Reference guide for transform actions used with midjourney_transform tool.

    Returns:
        Detailed list of all transformation actions and when to use them.
    """
    # Last updated: 2026-04-05
    return """Midjourney Transform Actions:

From 2x2 Grid (after initial generation):
- upscale1: Upscale top-left image
- upscale2: Upscale top-right image
- upscale3: Upscale bottom-left image
- upscale4: Upscale bottom-right image
- variation1: Create variations of top-left image
- variation2: Create variations of top-right image
- variation3: Create variations of bottom-left image
- variation4: Create variations of bottom-right image
- reroll: Regenerate all 4 images with same prompt

After Upscaling:
- upscale_2x: Upscale the image by 2x (double resolution)
- upscale_4x: Upscale the image by 4x (quadruple resolution)
- variation_subtle: Create subtle variations
- variation_strong: Create stronger variations
- zoom_out_2x: Zoom out by 2x (expand canvas)
- zoom_out_1_5x: Zoom out by 1.5x
- pan_left: Expand image to the left
- pan_right: Expand image to the right
- pan_up: Expand image upward
- pan_down: Expand image downward

Special Actions:
- variation_region: Regenerate specific region using mask
  (requires mask parameter with Base64-encoded image)

Typical Workflow:
1. Generate: midjourney_imagine("prompt")
2. Select: midjourney_transform(image_id, "upscale2")
3. Enhance: midjourney_transform(new_id, "upscale_4x")
4. Expand: midjourney_transform(new_id, "zoom_out_2x")
"""
