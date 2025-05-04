import pika
import json
import logging

logging.basicConfig(filename="rabbitmq.log", level=logging.INFO)

def send_to_queue(message, queue="tasks"):
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent
    )
    logging.info(f"Sent to {queue}: {message}")
    connection.close()

if __name__ == "__main__":
    send_to_queue({"order_id": "ORD001", "action": "log_bid", "amount": 1000})

