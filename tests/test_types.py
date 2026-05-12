"""Unit tests for Midjourney type definitions."""

from typing import get_args

from core.types import MidjourneyVersion


def test_midjourney_version_includes_v81() -> None:
    """Midjourney version enum should include the latest 8.1 model."""
    assert "8.1" in get_args(MidjourneyVersion)
