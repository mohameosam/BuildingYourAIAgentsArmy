from crewai import Agent, Task, Crew
import requests
import redis
import logging

logging.basicConfig(filename="crewai.log", level=logging.INFO)
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Agents
stock_checker = Agent(
    role="Stock Checker",
    goal="Verify inventory levels for items",
    backstory="Expert in inventory databases, uses Redis and RAG",
    tools=[],
    verbose=True
)

order_processor = Agent(
    role="Order Processor",
    goal="Process orders and update stock",
    backstory="Specialist in order fulfillment, integrates with n8n",
    tools=[],
    verbose=True
)

# Tasks
check_stock_task = Task(
    description="Check stock for item {item_id} and return available quantity",
    agent=stock_checker,
    expected_output="JSON with item_id and quantity"
)

process_order_task = Task(
    description="Process order for item {item_id} with quantity {quantity}",
    agent=order_processor,
    expected_output="JSON with order_id and status"
)

# Crew
inventory_crew = Crew(
    agents=[stock_checker, order_processor],
    tasks=[check_stock_task, process_order_task],
    verbose=2
)

def run_inventory_crew(item_id, quantity):
    result = inventory_crew.kickoff(inputs={"item_id": item_id, "quantity": quantity})
    logging.info(f"Crew result: {result}")
    return result

