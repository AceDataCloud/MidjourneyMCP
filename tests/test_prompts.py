"""Tests for Midjourney MCP guidance prompts."""

from pathlib import Path

from core.types import DEFAULT_VERSION
from prompts import midjourney_image_generation_guide, midjourney_workflow_examples


def test_v81_guidance_excludes_unsupported_quality_and_turbo() -> None:
    guide = midjourney_image_generation_guide()
    examples = midjourney_workflow_examples()

    assert "Quality is unsupported" in guide
    assert "Turbo is not supported in V8.1" in guide
    assert "separate resolution-based rates" in guide
    assert "do not set `quality` or use Turbo" in examples
    assert "V8.1 only. Costs 4x credits" not in guide
    assert "HD+Q4 together cost 16x" not in examples


def test_v81_tool_schema_describes_supported_controls() -> None:
    source = (Path(__file__).resolve().parents[1] / "tools" / "imagine_tools.py").read_text()

    assert "V8.1 only supports fast and relax" in source
    assert "separate SD and HD resolution-based rates" in source
    assert "This parameter is not supported in V8.1" in source
    assert source.count("selected SD/HD resolution rate") == 2
    assert DEFAULT_VERSION == "8.1"
