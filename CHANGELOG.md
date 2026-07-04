# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-22

### Added

- Initial release of MCP Midjourney Server
- Image generation tools:
  - `midjourney_imagine` - Generate images from text prompts
  - `midjourney_transform` - Transform images (upscale, variation, zoom, pan)
  - `midjourney_blend` - Blend multiple images together
  - `midjourney_with_reference` - Generate using reference images
- Image editing tools:
  - `midjourney_edit` - Edit images with text prompts
  - `midjourney_describe` - Get AI descriptions of images
- Video generation tools:
  - `midjourney_generate_video` - Generate videos from text and images
  - `midjourney_extend_video` - Extend existing videos
- Translation tools:
  - `midjourney_translate` - Translate Chinese to English
- Task tracking:
  - `midjourney_get_task` - Query single task status
  - `midjourney_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `midjourney_list_actions` - List available actions
  - `midjourney_get_prompt_guide` - Prompt writing guide
  - `midjourney_list_transform_actions` - Transform action reference
- Support for fast, relax, and turbo modes
- stdio and HTTP transport modes
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/MidjourneyMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/MidjourneyMCP/releases/tag/v0.1.0
