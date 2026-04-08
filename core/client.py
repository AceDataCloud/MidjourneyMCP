"""HTTP client for Midjourney API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import (
    MidjourneyAPIError,
    MidjourneyAuthError,
    MidjourneyError,
    MidjourneyTimeoutError,
)

# Dummy callback URL used to force the upstream API into async mode.
# When present, the API returns immediately with a task_id instead of blocking
# until generation completes. The health endpoint simply returns 200 OK and
# discards the callback payload — it is never actually processed.
_ASYNC_CALLBACK_URL = "https://api.acedata.cloud/health"

# Context variable for per-request API token (used in HTTP/remote mode)
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the API token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the API token from the current request context."""
    return _request_api_token.get()


class MidjourneyClient:
    """Async HTTP client for AceDataCloud Midjourney API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the Midjourney API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"MidjourneyClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise MidjourneyAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _with_async_callback(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Ensure long-running media operations are submitted asynchronously."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url"):
            request_payload["callback_url"] = _ASYNC_CALLBACK_URL
        return request_payload

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse API error response and raise the appropriate exception.

        The AceDataCloud API returns errors in the format:
            {"error": {"code": "...", "message": "..."}}
        """
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        error_obj = body.get("error", {})
        code = error_obj.get("code", f"http_{status}")
        message = (
            error_obj.get("message") or body.get("detail") or response.text or f"HTTP {status}"
        )

        logger.error(f"API error {status} [{code}]: {message}")

        if status in (401, 403):
            raise MidjourneyAuthError(message)
        raise MidjourneyAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Midjourney API.

        Args:
            endpoint: API endpoint path (e.g., "/midjourney/imagine")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            MidjourneyAuthError: If authentication fails
            MidjourneyAPIError: If the API request fails
            MidjourneyTimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"🚀 POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"📥 Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success(f"✅ Request successful! Task ID: {result.get('task_id', 'N/A')}")

                # Log summary of response
                if result.get("success"):
                    if "image_url" in result:
                        logger.info(
                            f"📊 Image generated: {result.get('image_width', 'N/A')}x{result.get('image_height', 'N/A')}"
                        )
                    elif "video_urls" in result:
                        logger.info(
                            f"📊 Videos generated: {len(result.get('video_urls', []))} video(s)"
                        )
                    elif "descriptions" in result:
                        logger.info(
                            f"📊 Descriptions: {len(result.get('descriptions', []))} description(s)"
                        )
                else:
                    logger.warning(f"⚠️ API returned success=false: {result.get('error', {})}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"⏰ Request timeout after {request_timeout}s: {e}")
                raise MidjourneyTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except MidjourneyError:
                raise

            except Exception as e:
                logger.error(f"❌ Request error: {e}")
                raise MidjourneyAPIError(message=str(e)) from e

    # Convenience methods for specific endpoints
    async def imagine(self, **kwargs: Any) -> dict[str, Any]:
        """Generate image using the imagine endpoint."""
        logger.info(f"🎨 Generating image with action: {kwargs.get('action', 'generate')}")
        return await self.request("/midjourney/imagine", self._with_async_callback(kwargs))

    async def describe(self, **kwargs: Any) -> dict[str, Any]:
        """Describe image using the describe endpoint."""
        logger.info(f"🔍 Describing image: {kwargs.get('image_url', '')[:50]}...")
        return await self.request("/midjourney/describe", kwargs)

    async def edit(self, **kwargs: Any) -> dict[str, Any]:
        """Edit image using the edits endpoint."""
        logger.info(f"✏️ Editing image with prompt: {kwargs.get('prompt', '')[:50]}...")
        return await self.request("/midjourney/edits", self._with_async_callback(kwargs))

    async def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video using the videos endpoint."""
        logger.info(f"🎬 Generating video with action: {kwargs.get('action', 'generate')}")
        return await self.request("/midjourney/videos", self._with_async_callback(kwargs))

    async def translate(self, **kwargs: Any) -> dict[str, Any]:
        """Translate content using the translate endpoint."""
        logger.info(f"🌐 Translating content: {kwargs.get('content', '')[:50]}...")
        return await self.request("/midjourney/translate", kwargs)

    async def get_seed(self, **kwargs: Any) -> dict[str, Any]:
        """Get seed value for a generated image."""
        logger.info(f"🌱 Getting seed for image: {kwargs.get('image_id', '')}")
        return await self.request("/midjourney/seed", kwargs)

    async def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        task_id = kwargs.get("id") or kwargs.get("ids", [])
        logger.info(f"🔍 Querying task(s): {task_id}")
        return await self.request("/midjourney/tasks", kwargs)


# Global client instance
client = MidjourneyClient()
