import asyncio
from urllib.parse import urlsplit, urlunsplit

import demistomock as demisto
from CommonServerPython import *
from MCPApiModule import *


TIDAL_AUTH_TYPE = AuthMethods.TOKEN.value
SERVER_NAME = "Tidal MCP"
TIDAL_HOST_SUFFIX = ".tidalcyber.com"


def validate_and_normalize_server_url(server_url: str) -> str:
    """Validate and normalize a Tidal-hosted MCP server URL."""
    value = server_url.strip()
    if not value:
        raise ValueError("Tidal MCP Server URL must be provided.")

    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as error:
        raise ValueError("Tidal MCP Server URL is invalid.") from error

    hostname = (parsed.hostname or "").rstrip(".").lower()
    if parsed.scheme.lower() != "https":
        raise ValueError("Tidal MCP Server URL must use HTTPS.")
    if not hostname:
        raise ValueError("Tidal MCP Server URL must include a hostname.")
    if parsed.username or parsed.password:
        raise ValueError("Tidal MCP Server URL must not contain credentials.")
    if parsed.query or parsed.fragment:
        raise ValueError("Tidal MCP Server URL must not contain a query string or fragment.")
    if parsed.path not in ("/mcp", "/mcp/"):
        raise ValueError("Tidal MCP Server URL must end in /mcp.")
    if not hostname.endswith(TIDAL_HOST_SUFFIX):
        raise ValueError("Tidal MCP Server URL must use a Tidal Cyber hostname.")
    if port not in (None, 443):
        raise ValueError("Tidal MCP Server URL must use the standard HTTPS port.")

    return urlunsplit(("https", hostname, "/mcp", "", ""))


def validate_required_token(token: str) -> None:
    """Validate the token required to connect to a Tidal MCP server."""
    if not token:
        raise ValueError("A Tidal read-only API token must be provided.")


async def main() -> None:  # pragma: no cover
    params = demisto.params()
    args = demisto.args()
    command = demisto.command()

    client = None
    try:
        server_url = validate_and_normalize_server_url(params.get("server_url") or "")
        token = params.get("token", {}).get("password") or ""
        validate_required_token(token)

        client = Client(
            base_url=server_url,
            auth_type=TIDAL_AUTH_TYPE,
            token=token,
        )
        demisto.debug(f"Command being called is {command}")

        if command == "test-module":
            result = await client.test_connection()
            return_results(result)
        elif command == "list-tools":
            result = await client.list_tools(SERVER_NAME)
            return_results(result)
        elif command == "call-tool":
            result = await client.call_tool(args["name"], args.get("arguments", ""))
            return_results(result)
        else:
            raise NotImplementedError(f"Command {command} is not implemented")
    except BaseException as error:
        root_message = extract_root_error_message(error)
        return_error(f"Failed to execute {command} command.\nError:\n{root_message}")
    finally:
        if client:
            demisto.debug(f"Closing client connection for {command}")
            await client.close()


if __name__ in ("__main__", "__builtin__", "builtins"):
    asyncio.run(main())
