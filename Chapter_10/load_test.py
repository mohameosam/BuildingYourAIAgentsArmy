import asyncio
import websockets
import json
import random
import time

async def send_task(task_type, params):
    async with websockets.connect("ws://<elb-dns>:8001") as ws:
        await ws.send(json.dumps({
            "action": task_type,
            "params": params,
            "api_key": "SECRET_KEY"
        }))
        response = await ws.recv()
        print(response)

async def load_test():
    tasks = [
        send_task("submit_order", {"order_id": f"ORD{random.randint(1000, 9999)}", "item_id": "ABC", "quantity": 2}),
        send_task("submit_ticket", {"ticket_id": f"TKT{random.randint(1000, 9999)}", "issue": "Order delayed"}),
        send_task("onboard_employee", {"employee_id": "Jane Doe"}),
        send_task("schedule_delivery", {"order_id": f"ORD{random.randint(1000, 9999)}", "destination": "Boston"})
    ] * 2500
    await asyncio.gather(*tasks)

start = time.time()
asyncio.run(load_test())
print(f"Load test: {time.time() - start:.2f}s")
