"""Prompt templates for Midjourney MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def midjourney_image_generation_guide() -> str:
    """Guide for choosing the right Midjourney tool for image generation."""
    return """# Midjourney Image Generation Guide

When the user wants to generate images, choose the appropriate tool based on their needs:

## Basic Image Generation
**Tool:** `midjourney_imagine`
**Use when:**
- User gives a description of what they want to see
- User wants to create new images from scratch
- Simple text-to-image generation

**Example:** "Create a sunset over mountains"
→ Call `midjourney_imagine` with prompt="Breathtaking sunset over mountain range, golden hour, dramatic clouds, landscape photography"

## Image Transformation
**Tool:** `midjourney_transform`
**Use when:**
- User wants to upscale one of the 4 generated images
- User wants variations of a specific image
- User wants to zoom out or pan an image

**Example:** "Upscale the second image"
→ Call `midjourney_transform` with image_id and action="upscale2"

## Image Blending
**Tool:** `midjourney_blend`
**Use when:**
- User wants to combine multiple images
- User provides multiple image URLs to merge
- Creative image fusion is needed

**Example:** "Blend these two images together"
→ Call `midjourney_blend` with list of image URLs and optional prompt

## Reference-Based Generation
**Tool:** `midjourney_with_reference`
**Use when:**
- User provides a reference image to modify
- User wants to apply a new style to an existing image
- User wants to reimagine an image with changes

**Example:** "Make this photo look like a watercolor painting"
→ Call `midjourney_with_reference` with reference_image_url and style prompt

## Image Editing
**Tool:** `midjourney_edit`
**Use when:**
- User wants to edit a specific image with AI
- User provides an image URL and edit instructions
- Targeted modifications to existing images

## Image Description
**Tool:** `midjourney_describe`
**Use when:**
- User wants to understand what prompts would recreate an image
- Reverse prompt engineering
- Getting inspiration from existing artwork

## Important Notes:
1. Image generation is async - always return the task_id to the user
2. Default mode is 'fast' (good balance of speed and credits)
3. Use 'turbo' for faster results (more credits)
4. Use 'relax' for slower, cheaper generation

## Midjourney V8 (Alpha) Features:
- **V8 is the latest model** - use `version='8'` for the newest capabilities
- **HD Mode** (`hd=True`): Generates 2K resolution images. V8 only. Costs 4x credits.
- **Quality 4** (`quality='4'`): Ultra-detail mode. V8 only. Costs 4x credits.
- **HD + Q4 combined**: Maximum quality. Costs 16x credits.
- **Style Reference** (`style_reference=True`): When prompt uses --sref. V8 premium feature, costs 4x.
- **Moodboard** (`moodboard=True`): Blending multiple reference images. V8 premium feature, costs 4x.
- V8 does NOT support --iw (image weight) parameter.
"""


@mcp.prompt()
def midjourney_workflow_examples() -> str:
    """Common workflow examples for Midjourney image generation."""
    return """# Midjourney Workflow Examples

## Workflow 1: Quick Image Generation
1. User: "Create a cyberpunk city"
2. Call `midjourney_imagine(prompt="Cyberpunk city at night, neon lights, rain, futuristic, detailed --ar 16:9")`
3. Return task_id and image_url to user
4. User can check status with `midjourney_get_task(task_id)`

## Workflow 2: Upscaling Best Image
1. Generate initial image with `midjourney_imagine`
2. User picks favorite from the 2x2 grid (e.g., "I like the top right one")
3. Call `midjourney_transform(image_id, action="upscale2")`
4. For even higher resolution: `midjourney_transform(new_image_id, action="upscale_4x")`

## Workflow 3: Creating Variations
1. Generate initial image with `midjourney_imagine`
2. User wants more options like a specific image
3. Call `midjourney_transform(image_id, action="variation3")`
4. This generates 4 new variations based on that image

## Workflow 4: Image Blending
1. User provides multiple image URLs
2. Call `midjourney_blend(image_urls=[url1, url2], prompt="Combine the face with the background")`
3. Return blended result

## Workflow 5: Style Transfer
1. User provides reference image URL
2. User describes new style: "Make it look like Van Gogh"
3. Call `midjourney_with_reference(reference_image_url, prompt="in the style of Van Gogh, Starry Night, swirling brushstrokes")`

## Workflow 6: Video from Image
1. User has an image they want to animate
2. Call `midjourney_generate_video(image_url, prompt="Gentle wind blowing through the scene")`
3. For longer video: `midjourney_extend_video(video_id, prompt="Continue the motion")`

## Tips:
- Always be descriptive in prompts - include style, lighting, mood, composition
- Use aspect ratio parameter (--ar) for specific dimensions
- Use --no parameter to exclude unwanted elements
- For Chinese speakers, offer translation with `midjourney_translate`
- For V8: use `version='8'` and consider `hd=True` for 2K, `quality='4'` for ultra detail
- V8 premium features (sref, moodboard, HD, Q4) cost 4x credits each; HD+Q4 together cost 16x
"""


@mcp.prompt()
def midjourney_style_suggestions() -> str:
    """Style and prompt writing suggestions for Midjourney."""
    return """# Midjourney Style Prompt Guide

## Effective Prompt Components

A good prompt includes:
- **Subject:** The main focus of the image
- **Style:** Artistic style or medium
- **Lighting:** How the scene is lit
- **Mood:** Emotional atmosphere
- **Details:** Specific elements to include
- **Parameters:** Technical specifications

## Example Prompts by Category

**Portraits:**
"Beautiful woman with flowing red hair, renaissance oil painting, dramatic chiaroscuro lighting, ornate golden frame, masterpiece --ar 2:3 --s 500"

**Landscapes:**
"Misty mountain valley at dawn, pine forests, lake reflection, atmospheric perspective, landscape photography by Ansel Adams --ar 16:9"

**Architecture:**
"Futuristic skyscraper with organic curves, glass and steel, sunset lighting, architectural visualization, ultra detailed --ar 9:16"

**Product:**
"Luxury perfume bottle, crystal clear, studio lighting, reflections on black surface, commercial photography --ar 1:1 --q 2"

**Fantasy:**
"Ancient wizard casting spell, magical energy, floating runes, dark forest background, epic fantasy art, detailed --ar 2:3"

**Sci-Fi:**
"Astronaut on alien planet, two moons in sky, bioluminescent plants, concept art, cinematic --ar 21:9"

**Abstract:**
"Flowing liquid metal, iridescent colors, organic shapes, abstract sculpture, studio lighting --ar 1:1 --s 1000"

## Style Keywords by Category

**Artistic Styles:**
oil painting, watercolor, digital art, concept art, illustration, anime, manga, photorealistic, hyperrealistic

**Photography Styles:**
portrait, landscape, street photography, macro, aerial, documentary, fashion, product

**Lighting:**
golden hour, blue hour, dramatic, soft, rim lighting, studio, natural, neon, chiaroscuro

**Moods:**
serene, dramatic, mysterious, joyful, melancholic, epic, intimate, ethereal

## Negative Prompts
Use --no to exclude elements:
- --no text, watermark, signature
- --no blurry, low quality
- --no people, faces
- --no modern, contemporary

## Aspect Ratios
- 1:1 - Square (Instagram, avatars)
- 16:9 - Widescreen (YouTube, presentations)
- 9:16 - Vertical (Stories, mobile)
- 2:3 - Portrait (prints, posters)
- 3:2 - Landscape (photography)
- 21:9 - Ultrawide (cinematic)
"""
