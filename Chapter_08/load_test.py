import asyncio
import websockets
import json
import random
import time

async def send_bid(bid_id):
    async with websockets.connect("ws://<ec2-public-ip>:8001") as ws:
        await ws.send(json.dumps({
            "action": "update_order",
            "params": {
                "order_id": bid_id,
                "status": "pending",
                "item_id": random.choice(["ABC", "DEF", "GHI"]),
                "amount": random.randint(300, 2000)
            },
            "api_key": "SECRET_KEY"
        }))
        response = await ws.recv()
        print(response)

async def load_test(n_bids=10000):
    tasks = [send_bid(f"BID{i:04d}") for i in range(n_bids)]
    await asyncio.gather(*tasks)

start = time.time()
asyncio.run(load_test())
print(f"Load test: {time.time() - start:.2f}s")


   
# Run the script from bash:
#
# python load_test.py