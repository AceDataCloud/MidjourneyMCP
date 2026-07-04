"""Pytest configuration and fixtures."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load .env file BEFORE any other imports
from dotenv import load_dotenv

load_dotenv(dotenv_path=project_root / ".env")

# Set default log level for tests
os.environ.setdefault("LOG_LEVEL", "DEBUG")


@pytest.fixture
def api_token():
    """Get API token from environment for integration tests."""
    token = os.environ.get("ACEDATACLOUD_API_TOKEN", "")
    if not token:
        pytest.skip("ACEDATACLOUD_API_TOKEN not configured for integration tests")
    return token


@pytest.fixture
def mock_imagine_response():
    """Mock successful imagine response."""
    return {
        "success": True,
        "task_id": "test-task-123",
        "image_id": "test-image-456",
        "image_url": "https://cdn.midjourney.com/test-image.png",
        "image_width": 1024,
        "image_height": 1024,
        "raw_image_url": "https://cdn.midjourney.com/test-image-raw.png",
        "raw_image_width": 2048,
        "raw_image_height": 2048,
        "progress": 100,
        "sub_image_urls": [
            "https://cdn.midjourney.com/sub1.png",
            "https://cdn.midjourney.com/sub2.png",
            "https://cdn.midjourney.com/sub3.png",
            "https://cdn.midjourney.com/sub4.png",
        ],
        "actions": ["upscale1", "upscale2", "upscale3", "upscale4", "variation1", "reroll"],
    }


@pytest.fixture
def mock_describe_response():
    """Mock successful describe response."""
    return {
        "descriptions": [
            "A beautiful sunset over the ocean with vibrant colors",
            "Golden hour photography of a seascape with clouds",
            "Dramatic coastal landscape with warm lighting",
            "Serene beach scene during sunset with reflection",
        ]
    }


@pytest.fixture
def mock_video_response():
    """Mock successful video response."""
    return {
        "success": True,
        "task_id": "test-video-task-123",
        "video_id": "test-video-456",
        "image_url": "https://cdn.midjourney.com/cover.png",
        "image_width": 1920,
        "image_height": 1080,
        "progress": 100,
        "video_urls": [
            "https://cdn.midjourney.com/video1.mp4",
            "https://cdn.midjourney.com/video2.mp4",
        ],
    }


@pytest.fixture
def mock_translate_response():
    """Mock successful translate response."""
    return {"content": "A beautiful mountain landscape at sunset, photorealistic, 8k"}


@pytest.fixture
def mock_task_response():
    """Mock task query response."""
    return {
        "id": "task-123",
        "type": "imagine",
        "created_at": "2025-01-21T00:00:00.000Z",
        "finished_at": "2025-01-21T00:01:00.000Z",
        "request": {
            "action": "generate",
            "prompt": "A test image",
            "mode": "fast",
        },
        "response": {
            "success": True,
            "image_id": "image-456",
            "image_url": "https://cdn.midjourney.com/test.png",
            "image_width": 1024,
            "image_height": 1024,
            "actions": ["upscale1", "upscale2"],
        },
    }


@pytest.fixture
def mock_edit_response():
    """Mock successful edit response."""
    return {
        "success": True,
        "task_id": "test-edit-123",
        "image_id": "test-edit-image-456",
        "image_url": "https://cdn.midjourney.com/edited.png",
        "image_width": 1024,
        "image_height": 1024,
        "raw_image_url": "https://cdn.midjourney.com/edited-raw.png",
        "raw_image_width": 2048,
        "raw_image_height": 2048,
        "progress": 100,
        "sub_image_urls": [],
    }


@pytest.fixture
def mock_shorten_response():
    """Mock successful shorten response."""
    return {
        "prompts": [
            "a serene mountain lake at sunrise, mist rising from the water, golden hour lighting --ar 16:9",
            "mountain lake sunrise with mist, golden light --ar 16:9 --v 6",
            "tranquil alpine lake, dawn mist, warm golden tones, cinematic --ar 16:9",
            "sunrise over a misty mountain lake, rich golden hour photography --ar 16:9 --style raw",
            "misty lake at dawn, mountains in background, golden sunrise --ar 16:9",
        ]
    }


@pytest.fixture
def mock_error_response():
    """Mock error response."""
    return {
        "success": False,
        "error": {
            "code": "invalid_request",
            "message": "Invalid parameters provided",
        },
    }
