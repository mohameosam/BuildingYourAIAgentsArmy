from confluent_kafka import Consumer
import json
import logging
import requests

logging.basicConfig(filename="kafka.log", level=logging.INFO)

def consume_kafka(topic="orders"):
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "mas_group",
        "auto.offset.reset": "earliest"
    })
    consumer.subscribe([topic])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logging.error(f"Consumer error: {msg.error()}")
            continue
        message = json.loads(msg.value().decode("utf-8"))
        if message.get("action") == "notify":
            logging.info(f"Sending notification: {message}")
     # Simulate email (replace with n8n Gmail node in prod)
            requests.post("http://localhost:5678/webhook/send-email", json={
                "to": message.get("recipient"),
                "subject": f"Order {message.get('order_id')} Update",
                "message": "Your order has been processed."
            })
    consumer.close()

if __name__ == "__main__":
    consume_kafka()

