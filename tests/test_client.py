"""Unit tests for async submission behavior in the HTTP client."""

from inspect import signature

from core.client import MidjourneyClient
from tools.edits_tools import midjourney_edit
from tools.imagine_tools import midjourney_imagine
from tools.video_tools import midjourney_extend_video, midjourney_generate_video


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running Midjourney operations should default to async submission."""
    client = MidjourneyClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "generate"})
    assert payload["async"] is True


def test_with_async_callback_preserves_explicit_callback() -> None:
    """User-provided callbacks should not be overwritten."""
    client = MidjourneyClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback(
        {"action": "generate", "callback_url": "https://example.com/webhook"}
    )
    assert payload["callback_url"] == "https://example.com/webhook"


def test_with_async_callback_preserves_explicit_false() -> None:
    """The OpenAPI async control must allow synchronous requests."""
    client = MidjourneyClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "generate", "async": False})
    assert payload["async"] is False


def test_long_running_tools_expose_openapi_async_parameter() -> None:
    """OpenAPI asynchronous request controls must be usable through MCP."""
    for tool in (
        midjourney_imagine,
        midjourney_edit,
        midjourney_generate_video,
        midjourney_extend_video,
    ):
        assert "async_" in signature(tool).parameters


def test_imagine_exposes_openapi_image_parameters() -> None:
    """OpenAPI image-based generation fields must be usable through MCP."""
    parameters = signature(midjourney_imagine).parameters
    assert {"image_id", "mask"} <= parameters.keys()
