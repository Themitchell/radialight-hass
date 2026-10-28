"""Unit tests for RadialightAPIClient construction."""

from unittest.mock import MagicMock

from helpers import load_radialight_module

api = load_radialight_module("api")
RadialightAPIClient = api.RadialightAPIClient


def test_api_client_initialized_with_urls_and_refresh_token() -> None:
    """Client is constructed with endpoint URLs and refresh token, not const imports."""
    session = MagicMock()
    client = RadialightAPIClient(
        "key",
        "refresh-token",
        session,
        "https://api.example",
        "https://token.example/v1/token",
    )

    assert client.session is session
    assert client.base_url == "https://api.example"
    assert client.firebase_token_url == "https://token.example/v1/token"
    assert client.firebase_api_key == "key"
    assert client.refresh_token == "refresh-token"
