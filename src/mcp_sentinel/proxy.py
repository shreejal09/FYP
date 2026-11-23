# proxy.py
# Sits between the AI client and the MCP server.
# For now it just passes messages through both ways.

import asyncio
import sys


class Proxy:

    def __init__(self, server_command):
        self.server_command = server_command
        self.server = None

    async def start_server(self):
        # Launch the MCP server as a background process
        self.server = await asyncio.create_subprocess_exec(
            *self.server_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def client_to_server(self):
        # Read what the AI client types, send it to the server
        while True:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            if not line:
                break
            # (Later: check static and diff layers here)
            self.server.stdin.write(line.encode())
            await self.server.stdin.drain()

    async def server_to_client(self):
        # Read what the server sends back, print it for the AI client
        while True:
            line = await self.server.stdout.readline()
            if not line:
                break
            # (Later: inspect tools/list responses here)
            sys.stdout.write(line.decode())
            sys.stdout.flush()

    async def run(self):
        # Start the server, then run both directions at the same time
        await self.start_server()
        await asyncio.gather(
            self.client_to_server(),
            self.server_to_client(),
        )


if __name__ == "__main__":
    # Temporary: hardcoded test server
    command = [sys.executable, "docker/servers/benign/dummy_server.py"]
    p = Proxy(command)

    try:
        asyncio.run(p.run())
    except KeyboardInterrupt:
        print("\nProxy stopped.")