from fastmcp import FastMCP

mcp = FastMCP("Hello")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to the user"""
    return f"Hello, {name}! This is a greeting from the MCP server."

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http", 
        host="localhost", 
        port=8001
    )
    