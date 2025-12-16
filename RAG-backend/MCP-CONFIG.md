# MCP Server Configuration

This project uses Model Context Protocol (MCP) servers to enhance development capabilities.

## Configured Servers

### GitHub Copilot
- **URL**: https://api.githubcopilot.com/mcp/
- **Type**: HTTP
- **Authentication**: Bearer token in Authorization header

### Context7
- **URL**: https://mcp.context7.com/mcp
- **Type**: HTTP
- **Authentication**: CONTEXT7_API_KEY header

## Managing MCP Servers

To view configured servers:
```bash
claude mcp list
```

To add a server:
```bash
claude mcp add --transport http <name> <url> --header "Header-Name: Value"
```

To remove a server:
```bash
claude mcp remove <name>
```

For more information:
```bash
claude mcp --help
```

## Troubleshooting

If servers fail to connect:
1. Verify network connectivity
2. Check authentication credentials
3. Ensure the server URLs are accessible
4. Run `claude mcp list` to see detailed status