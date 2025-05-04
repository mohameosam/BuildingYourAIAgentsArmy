import redis
import json
import sqlite3
import logging

logging.basicConfig(filename="cag.log", level=logging.INFO)
redis_client = redis.Redis(host="localhost", port=6379, db=0)

def cache_product(product_id, data, ttl=3600):
    redis_client.setex(product_id, ttl, json.dumps(data))
    db = sqlite3.connect("mas_cache.db")
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO cache (product_id, data, timestamp) VALUES (?, ?, ?)",
        (product_id, json.dumps(data), datetime.now().isoformat())
    )
    db.commit()
    db.close()
    logging.info(f"Cached {product_id} in Redis and SQLite")

def get_cached_product(product_id):
    cached = redis_client.get(product_id)
    if cached:
        logging.info(f"Cache hit: {product_id}")
        return json.loads(cached)
    db = sqlite3.connect("mas_cache.db")
    cursor = db.cursor()
    cursor.execute("SELECT data FROM cache WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()
    if row:
        data = json.loads(row[0])
        redis_client.setex(product_id, 3600, json.dumps(data))
        logging.info(f"Cache miss, restored: {product_id}")
        return data
    logging.info(f"Cache miss: {product_id}")
    return None
