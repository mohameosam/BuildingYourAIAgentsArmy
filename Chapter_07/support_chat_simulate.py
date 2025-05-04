import websockets
import json
async def send_support_message():
    async with websockets.connect("ws://localhost:8001") as ws:
        await ws.send(json.dumps({
            "action": "send_message",
            "params": {"recipient_id": "CUST1234", "content": "How can we assist you?"},
            "api_key": "SECRET_KEY"
        }))
        response = await ws.recv()
        print(response)
import asyncio
asyncio.run(send_support_message())

