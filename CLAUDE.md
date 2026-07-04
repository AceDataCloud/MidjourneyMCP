# MidjourneyMCP

MCP (Model Context Protocol) server for Midjourney AI image generation via AceDataCloud API.

## Project Structure

```
core/
  config.py     — Settings dataclass (API token, base URL)
  server.py     — FastMCP server singleton
  client.py     — httpx async HTTP client
  types.py      — Literal types (MidjourneyModel, MidjourneyAction, etc.)
  exceptions.py — Error classes (AuthError, APIError, TimeoutError)
  utils.py      — Formatting helpers
tools/
  imagine_tools.py   — generate images from prompts
  edits_tools.py     — upscale, variation, reroll, inpaint
  describe_tools.py  — describe images
  translate_tools.py — translate prompts
  seed_tools.py      — seed-based generation
  video_tools.py     — generate videos
  task_tools.py      — query task status, batch query
  info_tools.py      — list models, actions
prompts/           — LLM guidance prompts
tests/             — pytest-asyncio + respx tests
```

## Sync from Docs

When invoked by the sync workflow, the Docs repo is checked out at `_docs/`. Your job:

1. **Source of truth** — `_docs/openapi/midjourney.json` is the OpenAPI spec for the MidjourneyMCP API.
2. **Compare models** — The Literal types in `core/types.py` must match the spec's model enum. Add/remove as needed.
3. **Compare parameters** — Each `@mcp.tool()` function's parameters should match the corresponding OpenAPI endpoint.
4. **Update defaults** — If a new model becomes the recommended default, update the default in `core/types.py`.
5. **Update README** — Keep the model table and feature list current.
6. **Add tests** — For new tools or parameters, add test cases in `tests/`.
7. **PR title** — Use format: `sync: <description> [auto-sync]`

## Development

```bash
pip install -e ".[dev]"
pytest --cov=core --cov=tools
ruff check .
```
