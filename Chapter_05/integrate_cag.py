import sqlite3
from datetime import datetime

def get_cached_response(query):
    conn = sqlite3.connect("rag_cache.db")
    cursor = conn.cursor()
    cursor.execute("SELECT response FROM responses WHERE query = ?", (query,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def cache_response(query, response):
    conn = sqlite3.connect("rag_cache.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO responses (query, response, updated_at) VALUES (?, ?, ?)",
                   (query, response, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Modified query logic
query = "What are the top tech trends for 2025?"
cached = get_cached_response(query)
if cached:
    print("Cached:", cached)
else:
    response = qa_chain.run(query)
    cache_response(query, response)
    print("Generated:", response)

