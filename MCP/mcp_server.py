from mcp.server.fastapi import FastMCP

mcp = FastMCP("Demo MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def get_weather(city: str) -> str:
    """Mock weather tool"""
    return f"The weather in {city} is sunny ☀️"

if __name__ == "__main__":
    mcp.run()
