from crewai import Agent, Task, Crew
import redis
import requests
import logging

logging.basicConfig(filename="sales.log", level=logging.INFO)
redis_client = redis.Redis(host="localhost", port=6379, db=0)

order_agent = Agent(
    role="Order Agent",
    goal="Process customer orders and verify stock",
    backstory="Expert in e-commerce order management",
    tools=[],
    verbose=True
)

payment_agent = Agent(
    role="Payment Agent",
    goal="Validate payments and confirm orders",
    backstory="Specialist in payment gateways",
    tools=[],
    verbose=True
)

order_task = Task(
    description="Process order for item {item_id} with quantity {quantity}",
    agent=order_agent,
    expected_output="JSON with order_id, item_id, quantity, status"
)

payment_task = Task(
    description="Validate payment for order {order_id}",
    agent=payment_agent,
    expected_output="JSON with order_id, payment_status"
)

sales_crew = Crew(
    agents=[order_agent, payment_agent],
    tasks=[order_task, payment_task],
    verbose=2
)

def run_sales_crew(item_id, quantity, order_id):
    stock = query_rag_gpu(f"Stock for item {item_id}", model, index, documents)
    available = int(stock.split("Quantity: ")[1].split(",")[0])
    if available >= quantity:
        result = sales_crew.kickoff(inputs={"item_id": item_id, "quantity": quantity, "order_id": order_id})
        redis_client.setex(f"order:{order_id}", 3600, json.dumps(result))
        send_to_kafka({"order_id": order_id, "action": "notify", "recipient": "customer@example.com"})
        return result
    return {"order_id": order_id, "status": "out_of_stock"}

