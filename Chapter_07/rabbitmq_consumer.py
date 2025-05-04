import pika
import json
import sqlite3
import logging

logging.basicConfig(filename="rabbitmq.log", level=logging.INFO)

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        action = message.get("action")
        if action == "log_bid":
            order_id = message.get("order_id")
            amount = message.get("amount")
            db = sqlite3.connect("mas.db")
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO bids (order_id, amount, timestamp) VALUES (?, ?, ?)",
                (order_id, amount, datetime.now().isoformat())
            )
            db.commit()
            db.close()
            logging.info(f"Logged bid: {order_id}, ${amount}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def consume_queue(queue="tasks"):
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)
    logging.info(f"Consuming queue: {queue}")
    channel.start_consuming()

if __name__ == "__main__":
    consume_queue()

