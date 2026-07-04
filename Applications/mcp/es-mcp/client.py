import asyncio
import sys

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def main():
    # Start the MCP server using the same Python interpreter
    server = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:

            # Initialize the MCP session
            await session.initialize()

            print("\nConnected to MCP Server\n")

            # List available tools
            tools = await session.list_tools()

            print("Available Tools:")
            for tool in tools.tools:
                print(f" - {tool.name}")

            # Test ping
            result = await session.call_tool("ping", {})
            print("\nPing Result:")
            print(result.content)

            # Test cluster health
            result = await session.call_tool("cluster_health", {})
            print("\nCluster Health:")
            print(result.content)

            # Test list indices
            result = await session.call_tool("list_indices", {})
            print("\nIndices:")
            print(result.content)


if __name__ == "__main__":
    asyncio.run(main())