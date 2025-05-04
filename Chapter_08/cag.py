import pika  # For RabbitMQ message queue

# Initialize RabbitMQ connection
def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='agent_tasks')
    return channel, connection

# Central Agent Gateway class
class CentralAgentGateway:
    def __init__(self):
        self.channel, self.connection = connect_rabbitmq()
        self.task_history = {}  # Simple in-memory task storage

    # Process incoming task
    def process_task(self, task_data):
        # Simulate task processing (e.g., inventory query)
        task = task_data.decode()
        print(f"Processing task: {task}")
        self.task_history[task] = "Processed"
        return f"Task {task} completed"

    # Broadcast task to agents
    def broadcast_task(self, task_response):
        self.channel.basic_publish(
            exchange='',
            routing_key='agent_tasks',
            body=task_response.encode()
        )
        print("Task broadcasted to agents")

    # Run the gateway
    def run(self):
        print("Central Agent Gateway started...")
        self.channel.basic_consume(
            queue='agent_tasks',
            on_message_callback=lambda ch, method, properties, body: self.process_task(body)
        )
        self.channel.start_consuming()

# Example usage
if __name__ == "__main__":
    cag = CentralAgentGateway()
    try:
        cag.run()
    except KeyboardInterrupt:
        cag.connection.close()
        print("Gateway stopped.")