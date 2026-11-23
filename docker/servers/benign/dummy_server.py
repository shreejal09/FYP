# dummy_server.py
# A fake MCP server for testing the proxy.

import sys
import json

while True:
    line = sys.stdin.readline()
    if not line:
        break

    reply = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "tools": [
                {
                    "name": "hello",
                    "description": "A harmless test tool.",
                    "inputSchema": {"type": "object"},
                }
            ]
        },
    }
    print(json.dumps(reply), flush=True)