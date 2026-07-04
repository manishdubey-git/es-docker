from mcp.server.fastmcp import FastMCP

from config import es
from tools import register_all

mcp = FastMCP("Elastic MCP Server")

register_all(mcp, es)

if __name__ == "__main__":
    mcp.run()
