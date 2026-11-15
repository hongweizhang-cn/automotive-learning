from mcp.server import MCPServer

from tool_interface import execute_analyze_log


# Create an MCP server.
mcp = MCPServer("Automotive Log Analyzer")


# Register a tool.
@mcp.tool()
def analyze_automotive_log(file_path: str) -> dict:
    """
    Analyze an automotive CAN CSV log.

    Calculate frame counts and inter-frame intervals
    for each CAN ID.
    """
    return execute_analyze_log({
        "file_path": file_path
    })


# Start the MCP server using stdio transport.
if __name__ == "__main__":
    mcp.run()