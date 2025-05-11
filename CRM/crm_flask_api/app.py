from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "crm_user"),
        password=os.getenv("DB_PASSWORD", "crm_pass"),
        database=os.getenv("DB_NAME", "crm_database")
    )

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
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/<table>", methods=["POST"])
def create_record(table):
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
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)