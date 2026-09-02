import asyncio

import demistomock as demisto
from CommonServerPython import *
from MCPApiModule import *


TIDAL_AUTH_TYPE = AuthMethods.TOKEN.value
SERVER_NAME = "Tidal MCP"


def validate_required_params(server_url: str, token: str) -> None:
    """Validate the parameters required to connect to a Tidal MCP server."""
    if not server_url.strip():
        raise ValueError("Tidal MCP Server URL must be provided.")
    if not token:
        raise ValueError("A Tidal read-only API token must be provided.")


async def main() -> None:  # pragma: no cover
    params = demisto.params()
    args = demisto.args()
    command = demisto.command()

    client = None
    try:
        server_url = (params.get("server_url") or "").strip().rstrip("/")
        token = params.get("token", {}).get("password") or ""

        validate_required_params(server_url, token)

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
