Use the Tidal MCP integration to connect Cortex Agentic Assistant to a Tidal Cyber tenant and expose governed,
read-only threat and defensive context as agentic system actions.

## What does this pack do?

This pack connects to the customer-configured Tidal MCP endpoint, discovers its available tools, and lets Cortex agents
search and read Tidal objects without granting write access. Each customer supplies their own tenant URL and read-only
API token; no tenant URL or credential is embedded in the pack.

For credential safety, the configured endpoint must use HTTPS, a Tidal-managed `*.tidalcyber.com` hostname, the standard
HTTPS port, and the `/mcp` path. The integration rejects URLs containing embedded credentials, query strings, or
fragments.

## Tools

The Tidal MCP server currently exposes these tools:

- `find_tidal_objects` searches across supported Tidal object types.
- `read_tidal_object` reads a known Tidal object by type and identifier.
- `browse_defensive_coverage` browses defensive stacks and coverage maps.
- `browse_coverage_recommendations` browses prioritized coverage recommendations.
- `browse_product_registry_context` browses products, vendors, capabilities, and test results.
- `browse_threat_and_detection_context` browses threat objects, procedures, analytics, and detection context.

Tool availability and schemas are discovered from the configured server and may change as the Tidal MCP server evolves.
