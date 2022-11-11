import asyncio
import websockets

import json

import linux_common_tools as tools
from linux_autoconnect import get_networks


# create server who receives data
async def send_data():
    uri = "ws://localhost:8080"

    cmd = "nmcli device wifi"
    networks = get_networks(tools.read_data_from_shell(cmd)[0])

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(networks))


if __name__ == "__main__":
    asyncio.run(send_data())
