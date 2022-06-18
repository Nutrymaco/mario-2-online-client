import asyncio
import time

import websockets

from examples.websocket_client import  producer


async def main():
    ws = await websockets.connect("ws://localhost:8080/coordinates/nutrymaco")
    await producer(ws)

if __name__ == '__main__':
    asyncio.run(main())