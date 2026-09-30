import asyncio
import os
import websockets

clients = set()


async def handler(websocket):
    clients.add(websocket)
    print("Player connected!")

    try:
        async for message in websocket:
            print("Message:", message)

            for client in clients.copy():
                try:
                    await client.send(message)
                except:
                    clients.discard(client)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        clients.discard(websocket)
        print("Player disconnected!")


async def main():
    port = int(os.environ.get("PORT", 8765))

    print("CHAT SERVER STARTED")
    print("Port:", port)

    async with websockets.serve(
        handler,
        "0.0.0.0",
        port
    ):
        await asyncio.Future()


asyncio.run(main())
