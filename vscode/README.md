# Midjourney MCP

AI image generation with Midjourney — imagine, edit, blend, upscale, describe.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-midjourney?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-midjourney) [![PyPI](https://img.shields.io/pypi/v/mcp-midjourney.svg?label=PyPI)](https://pypi.org/project/mcp-midjourney/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://midjourney.mcp.acedata.cloud/mcp)

Bring Midjourney into VS Code chat. Generate 2x2 grids from prompts, upscale or vary a tile, blend multiple references, describe an image back into a prompt, and animate stills into short video.

This extension registers the **midjourney** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `midjourney` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a image task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Midjourney MCP: Set Ace Data Cloud API Key**
- **Midjourney MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://midjourney.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For screenshots, token setup, project-level and user-level `mcp.json`, and Copilot Agent Mode examples, see:

- [Midjourney MCP VS Code guide](https://platform.acedata.cloud/documents/promotion_article_mcp_midjourney_vscode)
- [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode)

### Example prompts

- "Generate an isometric pixel-art illustration of a cozy cafe. Use midjourney."
- "Upscale tile 3 of task <id>."
- "Describe https://example.com/photo.jpg and give me a Midjourney prompt."

---

## Tool Reference

**16 tools** available via this server.

| Tool | Description |
| --- | --- |
| `midjourney_imagine` | Generate AI images from a text prompt using Midjourney. |
| `midjourney_transform` | Transform an existing Midjourney image with various operations. |
| `midjourney_blend` | Blend multiple images together using Midjourney. |
| `midjourney_with_reference` | Generate images using a reference image as inspiration. |
| `midjourney_edit` | Edit an existing image using Midjourney. |
| `midjourney_describe` | Get AI-generated descriptions of an image. |
| `midjourney_generate_video` | Generate a video from text prompt and reference image using Midjourney. |
| `midjourney_extend_video` | Extend an existing Midjourney video to make it longer. |
| `midjourney_translate` | Translate Chinese text to English for use as Midjourney prompts. |
| `midjourney_shorten` | Analyze and shorten long Midjourney prompts while preserving key ideas. |
| `midjourney_get_seed` | Get the seed value of a previously generated Midjourney image. |
| `midjourney_get_task` | Query the status and result of a Midjourney generation task. |
| `midjourney_get_tasks_batch` | Query multiple Midjourney generation tasks at once. |
| `midjourney_list_actions` | List all available Midjourney API actions and corresponding tools. |
| `midjourney_get_prompt_guide` | Get guidance on writing effective prompts for Midjourney. |
| `midjourney_list_transform_actions` | List all available transformation actions for Midjourney images. |

## Supported Models

`5.2`, `6`, `6.1`, `7`, `8`

## Pricing

From $0.04 per /imagine job. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.midjourney
Server label: Midjourney MCP
Server URL  : https://midjourney.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "midjourney": {
      "type": "http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API key",
      "password": true
    }
  ]
}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

```jsonc
{
  "servers": {
    "midjourney": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-midjourney"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-midjourney`](https://pypi.org/project/mcp-midjourney/) on demand.

---

## Links

- **Hosted endpoint:** https://midjourney.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-midjourney`](https://pypi.org/project/mcp-midjourney/)
- **Source repository:** https://github.com/AceDataCloud/MidjourneyMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
