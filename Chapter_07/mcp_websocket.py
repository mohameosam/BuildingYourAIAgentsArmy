from websocket_server import WebsocketServer
import sqlite3
import json
import logging
from datetime import datetime

logging.basicConfig(filename="mcp_websocket.log", level=logging.INFO)

class MCPWebSocketServer:
    def __init__(self, host="localhost", port=8001):
        self.server = WebsocketServer(host=host, port=port)
        self.db = sqlite3.connect("mas.db")
        self.clients = {}  # {client_id: {"client": client, "subscriptions": [order_id]}}
        self.setup_db()
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.message_received)

    def setup_db(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT UNIQUE,
                product TEXT,
                quantity INTEGER,
                customer_id TEXT,
                status TEXT,
                timestamp TEXT
            )
        """)
        self.db.commit()

    def new_client(self, client, server):
        client_id = client["id"]
        self.clients[client_id] = {"client": client, "subscriptions": []}
        logging.info(f"New client connected: {client_id}")

    def client_left(self, client, server):
        client_id = client["id"]
        if client_id in self.clients:
            del self.clients[client_id]
            logging.info(f"Client disconnected: {client_id}")

    def message_received(self, client, server, message):
        client_id = client["id"]
        try:
            data = json.loads(message)
            action = data.get("action")
            params = data.get("params", {})
            api_key = data.get("api_key")

            if api_key != "SECRET_KEY":
                server.send_message(client, json.dumps({"error": "Unauthorized"}))
                return

            if action == "subscribe_order":
                order_id = params.get("order_id")
                if order_id and order_id not in self.clients[client_id]["subscriptions"]:
                    self.clients[client_id]["subscriptions"].append(order_id)
                    status = self.get_order_status(order_id)
                    server.send_message(client, json.dumps({"result": {"order_id": order_id, "status": status}}))
                    logging.info(f"Client {client_id} subscribed to {order_id}")

            elif action == "send_message":
                recipient_id = params.get("recipient_id")
                content = params.get("content")
                if recipient_id and content:
                    for cid, info in self.clients.items():
                        if cid == recipient_id:
                            server.send_message(info["client"], json.dumps({
                                "action": "receive_message",
                                "params": {"sender_id": client_id, "content": content}
                            }))
                            logging.info(f"Message from {client_id} to {recipient_id}: {content}")

            elif action == "update_order":
                order_id = params.get("order_id")
                status = params.get("status")
                if order_id and status in ["confirmed", "out_of_stock", "partial", "refunded"]:
                    self.update_order_status(order_id, status)
                    self.notify_subscribers(order_id, status)
                    server.send_message(client, json.dumps({"result": "Status updated"}))
                    logging.info(f"Order {order_id} updated to {status}")

            else:
                server.send_message(client, json.dumps({"error": f"Unknown action: {action}"}))

        except json.JSONDecodeError:
            server.send_message(client, json.dumps({"error": "Invalid JSON"}))

    def get_order_status(self, order_id):
        cursor = self.db.cursor()
        cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        return row[0] if row else "unknown"

    def update_order_status(self, order_id, status):
        cursor = self.db.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))
        self.db.commit()

    def notify_subscribers(self, order_id, status):
        for client_id, info in self.clients.items():
            if order_id in info["subscriptions"]:
                self.server.send_message(info["client"], json.dumps({
                    "action": "order_update",
                    "params": {"order_id": order_id, "status": status}
                }))

    def run(self):
        logging.info("Starting WebSocket server on port 8001")
        self.server.run_forever()

if __name__ == "__main__":
    server = MCPWebSocketServer()
    server.run()




# Run the script from bash:
#
# python mcp_websocket.py