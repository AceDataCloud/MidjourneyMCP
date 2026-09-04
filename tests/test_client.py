"""Unit tests for async submission behavior in the HTTP client."""

from inspect import signature
from unittest.mock import AsyncMock

import pytest

from core.client import MidjourneyClient, client
from core.server import mcp
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


@pytest.mark.asyncio
async def test_long_running_tool_schemas_expose_public_async_parameter() -> None:
    """The MCP schema should expose the OpenAPI name without leaking Python's suffix."""
    tools = {tool.name: tool for tool in await mcp.list_tools()}

    for name in (
        "midjourney_imagine",
        "midjourney_edit",
        "midjourney_generate_video",
        "midjourney_extend_video",
    ):
        properties = tools[name].inputSchema["properties"]
        assert "async" in properties
        assert "async_" not in properties


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "arguments", "endpoint"),
    [
        ("midjourney_imagine", {"prompt": "test image"}, "/midjourney/imagine"),
        (
            "midjourney_edit",
            {"image_url": "https://example.com/image.png", "prompt": "add rain"},
            "/midjourney/edits",
        ),
        (
            "midjourney_generate_video",
            {"image_url": "https://example.com/image.png", "prompt": "move"},
            "/midjourney/videos",
        ),
        (
            "midjourney_extend_video",
            {"video_id": "video-1", "prompt": "continue"},
            "/midjourney/videos",
        ),
    ],
)
async def test_fastmcp_dispatch_maps_public_async_parameter(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    arguments: dict[str, str],
    endpoint: str,
) -> None:
    """FastMCP should map the public async field to async_ before invocation."""
    request = AsyncMock(return_value={"task_id": "task-1"})
    monkeypatch.setattr(client, "request", request)

    for overrides, expected in (({}, True), ({"async": False}, False)):
        result = await mcp.call_tool(tool_name, arguments | overrides)

        assert result
        request.assert_awaited_once()
        called_endpoint, payload = request.await_args.args
        assert called_endpoint == endpoint
        assert payload["async"] is expected
        request.reset_mock()
