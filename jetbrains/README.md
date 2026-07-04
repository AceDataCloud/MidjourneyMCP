# Midjourney MCP — JetBrains Plugin

AI Image Generation with [Midjourney](https://midjourney.com) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Midjourney server with JetBrains AI Assistant.
Once configured, AI Assistant can create, edit, blend and transform images
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**15 AI Tools** — Create, edit, blend and transform images.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.midjourney)
2. Open **Settings → Tools → Midjourney MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "midjourney": {
      "command": "uvx",
      "args": ["mcp-midjourney"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `midjourney.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "midjourney": {
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [PyPI Package](https://pypi.org/project/mcp-midjourney/)
- [Source Code](https://github.com/AceDataCloud/MidjourneyMCP)

## License

MIT
