from unittest.mock import AsyncMock

import pytest

from TidalMCP import (
    SERVER_NAME,
    TIDAL_AUTH_TYPE,
    main,
    validate_and_normalize_server_url,
    validate_required_token,
)


VALID_PARAMS = {
    "server_url": "https://customer-hosted-api.tidalcyber.com/mcp/",
    "token": {"password": "customer-read-only-token"},
}


@pytest.mark.parametrize(
    ("server_url", "expected_url"),
    [
        (
            "https://customer-hosted-api.tidalcyber.com/mcp",
            "https://customer-hosted-api.tidalcyber.com/mcp",
        ),
        (
            "  https://CUSTOMER-hosted-api.tidalcyber.com:443/mcp/  ",
            "https://customer-hosted-api.tidalcyber.com/mcp",
        ),
    ],
)
def test_validate_and_normalize_server_url_accepts_tidal_urls(server_url: str, expected_url: str):
    # ACT
    result = validate_and_normalize_server_url(server_url)

    # ASSERT
    assert result == expected_url


@pytest.mark.parametrize(
    ("server_url", "message"),
    [
        ("", "Server URL must be provided"),
        ("http://customer-hosted-api.tidalcyber.com/mcp", "must use HTTPS"),
        ("https:///mcp", "must include a hostname"),
        ("https://user:password@customer-hosted-api.tidalcyber.com/mcp", "must not contain credentials"),
        ("https://customer-hosted-api.tidalcyber.com/mcp?tenant=customer", "must not contain a query"),
        ("https://customer-hosted-api.tidalcyber.com/mcp#tools", "must not contain a query"),
        ("https://customer-hosted-api.tidalcyber.com/api", "must end in /mcp"),
        ("https://attacker.example/mcp", "must use a Tidal Cyber hostname"),
        ("https://customer-hosted-api.tidalcyber.com.attacker.example/mcp", "must use a Tidal Cyber hostname"),
        ("https://127.0.0.1/mcp", "must use a Tidal Cyber hostname"),
        ("https://customer-hosted-api.tidalcyber.com:8443/mcp", "must use the standard HTTPS port"),
        ("https://customer-hosted-api.tidalcyber.com:invalid/mcp", "Server URL is invalid"),
    ],
)
def test_validate_and_normalize_server_url_rejects_unsafe_urls(server_url: str, message: str):
    # ACT / ASSERT
    with pytest.raises(ValueError, match=message):
        validate_and_normalize_server_url(server_url)


def test_validate_required_token_rejects_missing_token():
    # ACT / ASSERT
    with pytest.raises(ValueError, match="read-only API token"):
        validate_required_token("")


@pytest.mark.asyncio
async def test_main_tests_connection_and_closes_client(mocker):
    # ARRANGE
    client = AsyncMock()
    client.test_connection.return_value = "ok"
    client_class = mocker.patch("TidalMCP.Client", return_value=client)
    mocker.patch("TidalMCP.demisto.params", return_value=VALID_PARAMS)
    mocker.patch("TidalMCP.demisto.args", return_value={})
    mocker.patch("TidalMCP.demisto.command", return_value="test-module")
    return_results = mocker.patch("TidalMCP.return_results")

    # ACT
    await main()

    # ASSERT
    client_class.assert_called_once_with(
        base_url="https://customer-hosted-api.tidalcyber.com/mcp",
        auth_type=TIDAL_AUTH_TYPE,
        token="customer-read-only-token",
    )
    client.test_connection.assert_awaited_once_with()
    return_results.assert_called_once_with("ok")
    client.close.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_main_lists_tools_and_closes_client(mocker):
    # ARRANGE
    client = AsyncMock()
    client.list_tools.return_value = {"tools": ["find_tidal_objects"]}
    mocker.patch("TidalMCP.Client", return_value=client)
    mocker.patch("TidalMCP.demisto.params", return_value=VALID_PARAMS)
    mocker.patch("TidalMCP.demisto.args", return_value={})
    mocker.patch("TidalMCP.demisto.command", return_value="list-tools")
    return_results = mocker.patch("TidalMCP.return_results")

    # ACT
    await main()

    # ASSERT
    client.list_tools.assert_awaited_once_with(SERVER_NAME)
    return_results.assert_called_once_with({"tools": ["find_tidal_objects"]})
    client.close.assert_awaited_once_with()


@pytest.mark.asyncio
@pytest.mark.parametrize("arguments", ['{"query": "ransomware"}', None])
async def test_main_calls_tool_with_optional_arguments(mocker, arguments):
    # ARRANGE
    command_args = {"name": "find_tidal_objects"}
    if arguments is not None:
        command_args["arguments"] = arguments
    client = AsyncMock()
    client.call_tool.return_value = {"result": "success"}
    mocker.patch("TidalMCP.Client", return_value=client)
    mocker.patch("TidalMCP.demisto.params", return_value=VALID_PARAMS)
    mocker.patch("TidalMCP.demisto.args", return_value=command_args)
    mocker.patch("TidalMCP.demisto.command", return_value="call-tool")
    return_results = mocker.patch("TidalMCP.return_results")

    # ACT
    await main()

    # ASSERT
    client.call_tool.assert_awaited_once_with("find_tidal_objects", arguments or "")
    return_results.assert_called_once_with({"result": "success"})
    client.close.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_main_returns_unknown_command_error_and_closes_client(mocker):
    # ARRANGE
    client = AsyncMock()
    mocker.patch("TidalMCP.Client", return_value=client)
    mocker.patch("TidalMCP.demisto.params", return_value=VALID_PARAMS)
    mocker.patch("TidalMCP.demisto.args", return_value={})
    mocker.patch("TidalMCP.demisto.command", return_value="unknown-command")
    mocker.patch("TidalMCP.extract_root_error_message", return_value="not implemented")
    return_error = mocker.patch("TidalMCP.return_error")

    # ACT
    await main()

    # ASSERT
    return_error.assert_called_once_with("Failed to execute unknown-command command.\nError:\nnot implemented")
    client.close.assert_awaited_once_with()


@pytest.mark.asyncio
async def test_main_returns_client_error_and_closes_client(mocker):
    # ARRANGE
    client = AsyncMock()
    client.test_connection.side_effect = RuntimeError("connection failed")
    mocker.patch("TidalMCP.Client", return_value=client)
    mocker.patch("TidalMCP.demisto.params", return_value=VALID_PARAMS)
    mocker.patch("TidalMCP.demisto.args", return_value={})
    mocker.patch("TidalMCP.demisto.command", return_value="test-module")
    mocker.patch("TidalMCP.extract_root_error_message", return_value="connection failed")
    return_error = mocker.patch("TidalMCP.return_error")

    # ACT
    await main()

    # ASSERT
    return_error.assert_called_once_with("Failed to execute test-module command.\nError:\nconnection failed")
    client.close.assert_awaited_once_with()
