import asyncio
import os
import websockets

clients = set()


async def handler(websocket):

    clients.add(websocket)

    print("PLAYER CONNECTED")
    print("Players:", len(clients))

    try:

        async for message in websocket:

            print("MESSAGE:", message)

            disconnected = set()

            for client in clients.copy():

                try:

                    await client.send(message)

                except Exception as e:

                    print("SEND ERROR:", e)

                    disconnected.add(client)

            for client in disconnected:

                clients.discard(client)


    except websockets.exceptions.ConnectionClosed as e:

        print("Connection closed:", e)


    except Exception as e:

        print("CLIENT ERROR:", e)


    finally:

        clients.discard(websocket)

        print("PLAYER DISCONNECTED")
        print("Players:", len(clients))


async def main():

    port = int(
        os.environ.get(
            "PORT",
            8765
        )
    )

    print("================================")
    print("CHAT SERVER STARTED")
    print("PORT:", port)
    print("================================")


    async with websockets.serve(
        handler,
        "0.0.0.0",
        port
    ):

        await asyncio.Future()


asyncio.run(main())
