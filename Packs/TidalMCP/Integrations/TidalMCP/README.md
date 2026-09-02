Connect Cortex agents to a Tidal Cyber tenant through its read-only Model Context Protocol (MCP) server.
This integration was integrated and tested with the latest version of Tidal MCP.

## Configure Tidal MCP in Cortex

| **Parameter** | **Description** | **Required** |
| --- | --- | --- |
| Tidal MCP Server URL | The externally reachable HTTPS MCP endpoint for your Tidal tenant. The URL must use a Tidal-managed *.tidalcyber.com hostname, use the standard HTTPS port, contain no credentials, query string, or fragment, and end in /mcp. | True |
| Tidal Read-Only API Token | A customer-managed read-only API token for the Tidal tenant. Full-access tokens are not accepted by the MCP endpoint. | True |

## Commands

You can execute these commands from the CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.

### list-tools

***
Retrieves the tools available from the Tidal MCP server.

#### Base Command

`list-tools`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

There is no context output for this command.

### call-tool

***
Calls a Tidal MCP tool with optional input parameters.

#### Base Command

`call-tool`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| name | The name of the Tidal MCP tool to call. | Required |
| arguments | JSON parameters for the tool execution. | Optional |

#### Context Output

There is no context output for this command.
