"""Tests for hosted MCP OAuth behavior."""

from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlparse

import fakeredis
import fakeredis.aioredis
import pytest
from mcp.server.auth.provider import AuthorizationParams, OAuthClientInformationFull
from pydantic import AnyUrl
from starlette.requests import Request


def test_normalize_scopes_defaults_to_mcp_access():
    from core.oauth import MCP_ACCESS_SCOPE, _normalize_scopes

    assert _normalize_scopes(None) == [MCP_ACCESS_SCOPE]
    assert _normalize_scopes([]) == [MCP_ACCESS_SCOPE]


@pytest.mark.asyncio
async def test_direct_api_token_gets_mcp_access_scope(monkeypatch):
    from core import oauth

    captured = {}
    monkeypatch.setattr(
        oauth,
        "set_request_api_token",
        lambda token: captured.setdefault("token", token),
    )

    provider = oauth.AceDataCloudOAuthProvider()
    access_token = await provider.load_access_token("test-api-token")

    assert captured["token"] == "test-api-token"
    assert access_token.scopes == [oauth.MCP_ACCESS_SCOPE]


@pytest.mark.asyncio
async def test_oauth_state_and_code_exchange_cross_replicas(monkeypatch):
    from core import oauth
    from core.config import settings

    monkeypatch.setattr(settings, "server_url", "https://midjourney.mcp.acedata.cloud")
    monkeypatch.setattr(settings, "oauth_client_id", "upstream-client")
    redis_server = fakeredis.FakeServer()
    first_redis = fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
    second_redis = fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
    first = oauth.AceDataCloudOAuthProvider(first_redis, "0" * 64)
    second = oauth.AceDataCloudOAuthProvider(second_redis, "0" * 64)
    client = OAuthClientInformationFull(
        client_id="client-1",
        redirect_uris=[AnyUrl("https://client.example.com/callback")],
    )
    await first.register_client(client)
    registered = await second.get_client("client-1")
    assert registered.redirect_uris == client.redirect_uris

    auth_url = await second.authorize(
        registered,
        AuthorizationParams(
            state="client-state",
            scopes=["mcp:access"],
            code_challenge="client-challenge",
            redirect_uri=client.redirect_uris[0],
            redirect_uri_provided_explicitly=True,
        ),
    )
    state = parse_qs(urlparse(auth_url).query)["state"][0]
    first._exchange_code_for_jwt = AsyncMock(return_value="upstream-jwt")
    first._get_user_credential = AsyncMock(return_value="durable-token")
    response = await first.handle_callback(
        Request(
            {
                "type": "http",
                "query_string": f"state={state}&code=upstream-code".encode(),
            }
        )
    )
    assert response.status_code == 302
    code = parse_qs(urlparse(response.headers["location"]).query)["code"][0]
    loaded = await second.load_authorization_code(registered, code)
    token = await second.exchange_authorization_code(registered, loaded)
    assert token.access_token == "durable-token"
    assert await first.load_authorization_code(registered, code) is None
