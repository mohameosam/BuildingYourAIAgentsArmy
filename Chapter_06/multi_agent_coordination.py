# File: multi_agent_coordination.py
# Chapter 6: Multi-Agent Systems (MAS)
# This script shows how agents coordinate using RabbitMQ.

# Import libraries
import pika

# Function to connect to RabbitMQ
def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='agent_tasks')
    return channel, connection

# Agent function
def agent_process(agent_name, task):
    print(f"{agent_name} processing: {task}")
    return f"{task} completed by {agent_name}"

# Coordinate agents
def coordinate_agents(task):
    channel, connection = connect_rabbitmq()
    channel.basic_publish(exchange='', routing_key='agent_tasks', body=task)
    print(f"Task sent: {task}")
    connection.close()

# Example usage
if __name__ == "__main__":
    task = "Process order #123"
    coordinate_agents(task)