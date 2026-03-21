"""Unit tests for utility functions."""

import json

from core.utils import (
    format_describe_result,
    format_edit_result,
    format_imagine_result,
    format_task_result,
    format_translate_result,
    format_video_result,
)


class TestFormatImagineResult:
    """Tests for format_imagine_result function."""

    def test_format_success(self, mock_imagine_response):
        """Test formatting successful imagine response."""
        result = format_imagine_result(mock_imagine_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        assert data["image_id"] == "test-image-456"
        assert "image_url" in data
        assert data["progress"] == 100
        assert len(data["sub_image_urls"]) == 4
        assert "upscale1" in data["actions"]
        assert data["mcp_async_submission"]["poll_tool"] == "midjourney_get_task"

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_imagine_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False
        assert data["error"]["code"] == "invalid_request"


class TestFormatDescribeResult:
    """Tests for format_describe_result function."""

    def test_format_success(self, mock_describe_response):
        """Test formatting successful describe response."""
        result = format_describe_result(mock_describe_response)
        data = json.loads(result)
        assert len(data["descriptions"]) == 4
        assert "sunset" in data["descriptions"][0]

    def test_format_empty(self):
        """Test formatting empty describe response."""
        response = {"descriptions": []}
        result = format_describe_result(response)
        data = json.loads(result)
        assert data["descriptions"] == []


class TestFormatVideoResult:
    """Tests for format_video_result function."""

    def test_format_success(self, mock_video_response):
        """Test formatting successful video response."""
        result = format_video_result(mock_video_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-video-task-123"
        assert data["video_id"] == "test-video-456"
        assert len(data["video_urls"]) == 2
        assert data["mcp_async_submission"]["poll_tool"] == "midjourney_get_task"

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_video_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False


class TestFormatTranslateResult:
    """Tests for format_translate_result function."""

    def test_format_success(self, mock_translate_response):
        """Test formatting successful translate response."""
        result = format_translate_result(mock_translate_response)
        data = json.loads(result)
        assert "content" in data
        assert "mountain" in data["content"]


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response):
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        data = json.loads(result)
        assert data["id"] == "task-123"
        assert data["type"] == "imagine"
        assert data["request"]["action"] == "generate"
        assert data["response"]["success"] is True
        assert data["mcp_task_polling"]["poll_tool"] == "midjourney_get_task"

    def test_format_error(self):
        """Test formatting error response."""
        error_response = {"error": {"code": "not_found", "message": "Task not found"}}
        result = format_task_result(error_response)
        data = json.loads(result)
        assert data["error"]["code"] == "not_found"


class TestFormatEditResult:
    """Tests for format_edit_result function."""

    def test_format_success(self, mock_edit_response):
        """Test formatting successful edit response."""
        result = format_edit_result(mock_edit_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-edit-123"
        assert data["image_id"] == "test-edit-image-456"
        assert data["progress"] == 100
        assert data["mcp_async_submission"]["poll_tool"] == "midjourney_get_task"

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_edit_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False
