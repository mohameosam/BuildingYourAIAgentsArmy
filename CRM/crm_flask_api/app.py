from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import logging
from datetime import datetime

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "crm_user"),
        password=os.getenv("DB_PASSWORD", "crm_pass"),
        database=os.getenv("DB_NAME", "crm_database")
    )

@app.route("/customer/phone/<phone>", methods=["GET"])
def get_customer_by_phone(phone):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer WHERE phone = %s", (phone,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(result or {}), 200
    except Exception as e:
        logging.exception("Error fetching customer by phone")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/order", methods=["POST"], strict_slashes=False)
def create_order_with_items():
    data = request.get_json() or {}
    phone = data.get('phone')
    products = data.get('products')

    if not phone or not isinstance(products, list) or not products:
        return jsonify({"success": False, "message": "Missing or invalid phone/products"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Find customer
        cursor.execute("SELECT customer_id FROM customer WHERE phone = %s", (phone,))
        cust = cursor.fetchone()
        if not cust:
            logging.debug(f"No customer found with phone {phone}")
            cursor.close()
            conn.close()
            return jsonify({}), 200
        customer_id = cust[0]

        # Prepare item details
        total_amount = 0
        item_details = []
        for item in products:
            product_id = item.get('product_id')
            qty = item.get('quantity', 0)
            if not product_id or qty <= 0:
                logging.warning(f"Skipping invalid item: {item}")
                continue

            cursor.execute("SELECT price FROM product WHERE product_id = %s", (product_id,))
            prod = cursor.fetchone()
            if not prod:
                logging.warning(f"Product not found: {product_id}")
                continue
            unit_price = prod[0]
            total_price = unit_price * qty
            total_amount += total_price
            item_details.append((product_id, qty, unit_price, total_price))

        if not item_details:
            logging.debug("No valid items to insert")
            cursor.close()
            conn.close()
            return jsonify({"success": False, "message": "No valid products provided"}), 400

        # Insert order
        now = datetime.now()
        cursor.execute(
            "INSERT INTO `order` (customer_id, order_date, total_amount, status) VALUES (%s, %s, %s, %s)",
            (customer_id, now, total_amount, 'pending')
        )
        order_id = cursor.lastrowid
        logging.debug(f"Inserted order {order_id} with total {total_amount}")

        # Insert order items
        for product_id, qty, unit_price, total_price in item_details:
            cursor.execute(
                "INSERT INTO order_item (order_id, product_id, quantity, unit_price, total_price) VALUES (%s, %s, %s, %s, %s)",
                (order_id, product_id, qty, unit_price, total_price)
            )
            logging.debug(f"Inserted item for order {order_id}: product_id={product_id}, qty={qty}")

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "order_id": order_id, "order_date":now, "total_amount": total_amount}), 201

    except Exception as e:
        logging.exception("Error creating order with items")
        return jsonify({"success": False, "message": str(e)}), 500

# Generic CRUD endpoints (excluded 'order' from generic POST)
@app.route("/<table>", methods=["GET"])
def list_records(table):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table}")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        logging.exception("Error listing records")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/<table>/<int:record_id>", methods=["GET"])
def get_record(table, record_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table} WHERE {table}_id = %s", (record_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "message": "Not found"}), 404
    except Exception as e:
        logging.exception("Error fetching record")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/<table>", methods=["POST"])
def create_record(table):
    if table.lower() == 'order':
        return jsonify({"success": False, "message": "Please use POST /order for orders."}), 404
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        fields = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({fields}) VALUES ({values})"
        cursor.execute(sql, tuple(data.values()))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Record created"}), 200
    except Exception as e:
        logging.exception("Error creating record")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/<table>/<int:record_id>", methods=["PUT"])
def update_record(table, record_id):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        updates = ', '.join([f"{k} = %s" for k in data.keys()])
        sql = f"UPDATE {table} SET {updates} WHERE {table}_id = %s"
        cursor.execute(sql, tuple(data.values()) + (record_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Record updated"}), 200
    except Exception as e:
        logging.exception("Error updating record")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/<table>/<int:record_id>", methods=["DELETE"])
def delete_record(table, record_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = f"DELETE FROM {table} WHERE {table}_id = %s"
        cursor.execute(sql, (record_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Record deleted"}), 200
    except Exception as e:
        logging.exception("Error deleting record")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)