## Tidal MCP integration

Use this integration to connect Cortex Agentic Assistant to the read-only MCP server for your Tidal Cyber tenant.
Cortex discovers the tools exposed by Tidal and creates agentic system actions for them.

### Prerequisites

- Ask your Tidal administrator to enable MCP and API-token authentication for the tenant.
- Create a customer-managed **read-only** Tidal API token for a user with the intended permissions. The MCP endpoint
  rejects full-access tokens.
- Ensure the tenant's HTTPS MCP endpoint is reachable from Cortex. The URL must use a Tidal-managed
  `*.tidalcyber.com` hostname and end in `/mcp`, for example `https://customer-hosted-api.tidalcyber.com/mcp`.

### Configure the integration

1. Enter the **Tidal MCP Server URL** for your tenant.
2. Enter the **Tidal Read-Only API Token** created for this integration instance.
3. Save and test the integration instance.

The integration uses the token only to authenticate requests to the configured tenant. Tidal Cyber does not provide or
embed a shared token. Tool visibility and results are limited by the permissions of the user who owns the token.

### Available tools

The server currently exposes six read-only tools for searching and reading threat intelligence, defensive coverage,
coverage recommendations, and product registry context. Cortex refreshes the discovered tool list after the instance is
saved and periodically thereafter, so the available actions can evolve with the Tidal MCP server.
