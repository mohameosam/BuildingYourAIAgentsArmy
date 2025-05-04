from mcp import Server
import sqlite3
from datetime import datetime
import logging

logging.basicConfig(filename="mcp.log", level=logging.INFO)

class MAServer(Server):
    def __init__(self):
        super().__init__(name="mas-server", transport="http")
        self.db = sqlite3.connect("mas.db")
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

    async def handle_request(self, request):
        logging.info(f"Request: {request}")
        method = request.get("method")
        params = request.get("params", {})
        cursor = self.db.cursor()

        if request.get("api_key") != "SECRET_KEY":
            return {"error": "Unauthorized"}

        if method == "submit_order":
            order_id = params.get("order_id")
            product = params.get("product")
            quantity = params.get("quantity")
            customer_id = params.get("customer_id", "UNKNOWN")
            if not all([order_id, product, quantity]) or not isinstance(order_id, str) or not order_id.startswith("ORD"):
                return {"error": "Invalid or missing fields"}
            if not isinstance(quantity, int) or quantity <= 0:
                return {"error": "Invalid quantity"}
            status = "pending"
            timestamp = datetime.now().isoformat()
            try:
                cursor.execute(
                    "INSERT INTO orders (order_id, product, quantity, customer_id, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (order_id, product, quantity, customer_id, status, timestamp)
                )
                self.db.commit()
                return {"result": {"order_id": order_id, "status": status}}
            except sqlite3.IntegrityError:
                return {"error": f"Order ID {order_id} already exists"}

        if method == "get_order_status":
            order_id = params.get("order_id")
            if not isinstance(order_id, str):
                return {"error": "Invalid order_id"}
            cursor.execute("SELECT status, product, quantity FROM orders WHERE order_id = ?", (order_id,))
            row = cursor.fetchone()
            if row:
                return {"result": {"status": row[0], "product": row[1], "quantity": row[2]}}
            return {"error": "Order not found"}

        if method == "update_order":
            order_id = params.get("order_id")
            status = params.get("status")
            if not all([order_id, status]) or status not in ["confirmed", "out_of_stock", "partial", "refunded"]:
                return {"error": "Invalid or missing fields"}
            cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))
            if cursor.rowcount == 0:
                return {"error": "Order not found"}
            self.db.commit()
            return {"result": "Status updated"}

        return {"error": f"Unknown method: {method}"}

if __name__ == "__main__":
    server = MAServer()
    server.run()


# Run the script from bash:
#
# python mas_server.py