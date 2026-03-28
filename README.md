# MCP Midjourney

<!-- mcp-name: io.github.AceDataCloud/mcp-midjourney -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-midjourney.svg)](https://pypi.org/project/mcp-midjourney/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-midjourney.svg)](https://pypi.org/project/mcp-midjourney/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI image and video generation using [Midjourney](https://midjourney.com) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI images, videos, and manage creative projects directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Image Generation** - Create AI-generated images from text prompts
- **Image Transformation** - Upscale, create variations, zoom, and pan images
- **Image Blending** - Combine multiple images into creative fusions
- **Reference-Based Generation** - Use existing images as inspiration
- **Image Description** - Get AI descriptions of images (reverse prompt)
- **Image Editing** - Edit images with text prompts and masks
- **Video Generation** - Create videos from text and reference images
- **Video Extension** - Extend existing videos to make them longer
- **Translation** - Translate Chinese prompts to English
- **Task Tracking** - Monitor generation progress and retrieve results

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the [API documentation page](https://platform.acedata.cloud/documents/e52c028d-897a-4d51-b110-60fccbe6118d)
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://midjourney.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://midjourney.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cursor / Windsurf

Add to your MCP config (`.cursor/mcp.json` or `.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### VS Code (Copilot)

Add to your VS Code MCP config (`.vscode/mcp.json`):

```json
{
  "servers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which bundles all 11 MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** → **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "midjourney": {
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```


#### Claude Code

Claude Code supports MCP servers natively:

```bash
claude mcp add midjourney --transport http https://midjourney.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cline

Add to Cline's MCP settings (`.cline/mcp_settings.json`):

```json
{
  "mcpServers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Amazon Q Developer

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Roo Code

Add to Roo Code MCP settings:

```json
{
  "mcpServers": {
    "midjourney": {
      "type": "streamable-http",
      "url": "https://midjourney.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Continue.dev

Add to `.continue/config.yaml`:

```yaml
mcpServers:
  - name: midjourney
    type: streamable-http
    url: https://midjourney.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "midjourney": {
        "url": "https://midjourney.mcp.acedata.cloud/mcp",
        "headers": {
          "Authorization": "Bearer YOUR_API_TOKEN"
        }
      }
    }
  }
}
```

#### cURL Test

```bash
# Health check (no auth required)
curl https://midjourney.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://midjourney.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-midjourney
# or
uvx mcp-midjourney

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-midjourney

# Run (HTTP mode for remote access)
mcp-midjourney --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "midjourney": {
      "command": "uvx",
      "args": ["mcp-midjourney"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-midjourney:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-midjourney:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Tools

### Image Generation

| Tool                        | Description                                           |
| --------------------------- | ----------------------------------------------------- |
| `midjourney_imagine`        | Generate images from a text prompt (creates 2x2 grid) |
| `midjourney_transform`      | Transform images (upscale, variation, zoom, pan)      |
| `midjourney_blend`          | Blend multiple images together                        |
| `midjourney_with_reference` | Generate using a reference image as inspiration       |

### Image Editing

| Tool                  | Description                                      |
| --------------------- | ------------------------------------------------ |
| `midjourney_edit`     | Edit an existing image with text prompt          |
| `midjourney_describe` | Get AI descriptions of an image (reverse prompt) |

### Video

| Tool                        | Description                                  |
| --------------------------- | -------------------------------------------- |
| `midjourney_generate_video` | Generate video from text and reference image |
| `midjourney_extend_video`   | Extend existing video to make it longer      |

### Utility

| Tool                   | Description                                   |
| ---------------------- | --------------------------------------------- |
| `midjourney_translate` | Translate Chinese text to English for prompts |
| `midjourney_get_seed`  | Get the seed value of a generated image       |

### Tasks

| Tool                         | Description                  |
| ---------------------------- | ---------------------------- |
| `midjourney_get_task`        | Query a single task status   |
| `midjourney_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool                                | Description                 |
| ----------------------------------- | --------------------------- |
| `midjourney_list_actions`           | List available API actions  |
| `midjourney_get_prompt_guide`       | Get prompt writing guide    |
| `midjourney_list_transform_actions` | List transformation actions |

## Usage Examples

### Generate Image from Prompt

```
User: Create a cyberpunk city at night

Claude: I'll generate a cyberpunk city image for you.
[Calls midjourney_imagine with prompt="Cyberpunk city at night, neon lights, rain, futuristic, detailed --ar 16:9"]
```

### Upscale an Image

```
User: Upscale the second image

Claude: I'll upscale the top-right image from the grid.
[Calls midjourney_transform with image_id and action="upscale2"]
```

### Blend Multiple Images

```
User: Blend these two images: [url1] and [url2]

Claude: I'll blend these images together.
[Calls midjourney_blend with image_urls=[url1, url2]]
```

### Generate Video

```
User: Animate this image [url] with gentle movement

Claude: I'll create a video from this image.
[Calls midjourney_generate_video with image_url and prompt="Gentle camera movement, cinematic"]
```

## Generation Modes

| Mode    | Description                              |
| ------- | ---------------------------------------- |
| `fast`  | Recommended for most use cases (default) |
| `turbo` | Faster generation, uses more credits     |
| `relax` | Slower generation, cheaper               |

## Configuration

### Environment Variables

| Variable                     | Description                 | Default                     |
| ---------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`     | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL`  | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `MIDJOURNEY_DEFAULT_MODE`    | Default generation mode     | `fast`                      |
| `MIDJOURNEY_REQUEST_TIMEOUT` | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                  | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-midjourney --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/MidjourneyMCP.git
cd MidjourneyMCP

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=core --cov=tools

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy core tools
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Project Structure

```
MidjourneyMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Midjourney API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── describe_tools.py  # Image description tools
│   ├── edits_tools.py     # Image editing tools
│   ├── imagine_tools.py   # Image generation tools
│   ├── info_tools.py      # Information tools
│   ├── task_tools.py      # Task query tools
│   ├── translate_tools.py # Translation tools
│   └── video_tools.py     # Video generation tools
├── prompts/                # MCP prompt templates
│   └── __init__.py
├── tests/                  # Test suite
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Midjourney API](https://platform.acedata.cloud):

- [Midjourney Imagine API](https://platform.acedata.cloud/documents/e52c028d-897a-4d51-b110-60fccbe6118d) - Image generation
- [Midjourney Describe API](https://platform.acedata.cloud/documents/870e973b-712a-4686-ab8b-beae27f129ce) - Image description
- [Midjourney Tasks API](https://platform.acedata.cloud/documents/58ea7cc1-c685-40c3-a619-f29f9ac5d8f4) - Task queries
- [Midjourney Edits API](https://platform.acedata.cloud/documents/midjourney-edits) - Image editing
- [Midjourney Videos API](https://platform.acedata.cloud/documents/midjourney-videos) - Video generation
- [Midjourney Translate API](https://platform.acedata.cloud/documents/e067d19b-7a66-4458-a45f-0fe88c1d5d34) - Translation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [Midjourney Official](https://midjourney.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
