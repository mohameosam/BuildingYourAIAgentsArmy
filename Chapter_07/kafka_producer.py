import json
import logging

logging.basicConfig(filename="kafka.log", level=logging.INFO)

def delivery_report(err, msg):
    if err:
        logging.error(f"Message delivery failed: {err}")
    else:
        logging.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_to_kafka(message, topic="orders"):
    producer = Producer({"bootstrap.servers": "localhost:9092"})
    producer.produce(topic, json.dumps(message).encode("utf-8"), callback=delivery_report)
    producer.flush()

if __name__ == "__main__":
    send_to_kafka({"order_id": "ORD002", "action": "notify", "recipient": "customer@example.com"})
