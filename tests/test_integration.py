"""
Integration tests for Midjourney MCP Server.

These tests make REAL API calls to verify all tools work correctly.
Run with: pytest tests/test_integration.py -v -s

Note: These tests require ACEDATACLOUD_API_TOKEN to be set.
They are skipped in CI environments without the token.
"""

import json
import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Check if API token is configured
HAS_API_TOKEN = bool(os.getenv("ACEDATACLOUD_API_TOKEN"))

# Decorator to skip tests that require API token
requires_api_token = pytest.mark.skipif(
    not HAS_API_TOKEN,
    reason="ACEDATACLOUD_API_TOKEN not configured - skipping integration test",
)


class TestImagineTools:
    """Integration tests for image generation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_imagine_basic(self) -> None:
        """Test basic image generation with real API."""
        from tools.imagine_tools import midjourney_imagine

        result = await midjourney_imagine(
            prompt="A simple red circle on white background, minimal",
            mode="fast",
        )

        print("\n=== Imagine Result ===")
        print(result)

        assert "task_id" in result


class TestTranslateTools:
    """Integration tests for translation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_translate(self) -> None:
        """Test Chinese to English translation."""
        from tools.translate_tools import midjourney_translate

        result = await midjourney_translate(content="一只可爱的猫咪在草地上玩耍")

        print("\n=== Translate Result ===")
        print(result)

        assert len(result) > 0


class TestInfoTools:
    """Integration tests for informational tools."""

    @pytest.mark.asyncio
    async def test_list_actions(self) -> None:
        """Test midjourney_list_actions tool."""
        from tools.info_tools import midjourney_list_actions

        result = await midjourney_list_actions()

        print("\n=== List Actions Result ===")
        print(result)

        assert "midjourney_imagine" in result
        assert "midjourney_describe" in result
        assert "midjourney_translate" in result

    @pytest.mark.asyncio
    async def test_get_prompt_guide(self) -> None:
        """Test midjourney_get_prompt_guide tool."""
        from tools.info_tools import midjourney_get_prompt_guide

        result = await midjourney_get_prompt_guide()

        print("\n=== Prompt Guide Result ===")
        print(result)

        assert len(result) > 0
        assert "prompt" in result.lower() or "midjourney" in result.lower()

    @pytest.mark.asyncio
    async def test_list_transform_actions(self) -> None:
        """Test midjourney_list_transform_actions tool."""
        from tools.info_tools import midjourney_list_transform_actions

        result = await midjourney_list_transform_actions()

        print("\n=== Transform Actions Result ===")
        print(result)

        assert (
            "upscale" in result.lower()
            or "variation" in result.lower()
            or "action" in result.lower()
        )


class TestTaskTools:
    """Integration tests for task query tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_get_task_with_real_id(self) -> None:
        """Test querying a task - first generate, then query."""
        from tools.imagine_tools import midjourney_imagine
        from tools.task_tools import midjourney_get_task

        # Generate an image first
        gen_result = await midjourney_imagine(
            prompt="A simple blue square, minimal",
            mode="fast",
        )

        print("\n=== Generate Result ===")
        print(gen_result)

        gen_data = json.loads(gen_result)
        task_id = gen_data.get("task_id")
        if task_id:
            # Query the task
            task_result = await midjourney_get_task(task_id=task_id)
            print("\n=== Task Result ===")
            print(task_result)
            assert task_id in task_result
