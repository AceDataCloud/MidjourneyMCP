"""Type definitions for Midjourney MCP server."""

from typing import Literal

# Midjourney generation modes
MidjourneyMode = Literal["fast", "relax", "turbo"]

# Midjourney version
MidjourneyVersion = Literal["5.2", "6", "6.1", "7", "8"]

# Midjourney imagine actions
ImagineAction = Literal[
    "generate",
    "upscale1",
    "upscale2",
    "upscale3",
    "upscale4",
    "upscale_2x",
    "upscale_4x",
    "variation1",
    "variation2",
    "variation3",
    "variation4",
    "variation_subtle",
    "variation_strong",
    "variation_region",
    "reroll",
    "zoom_out_2x",
    "zoom_out_1_5x",
    "pan_left",
    "pan_right",
    "pan_up",
    "pan_down",
]

# Video actions
VideoAction = Literal["generate", "extend"]

# Video mode options (relax is not supported for video generation)
VideoMode = Literal["fast", "turbo"]

# Video resolution options
VideoResolution = Literal["480p", "720p"]

# Default mode
DEFAULT_MODE: MidjourneyMode = "fast"

# Default video mode
DEFAULT_VIDEO_MODE: VideoMode = "fast"

# Default version (None = use Midjourney's default)
DEFAULT_VERSION: MidjourneyVersion | None = None
