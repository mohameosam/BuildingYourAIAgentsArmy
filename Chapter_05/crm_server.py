from mcp import Server
import sqlite3
from datetime import datetime

class CRMServer(Server):
    def __init__(self):
        super().__init__(name="crm-server", transport="http")
        self.db = sqlite3.connect("crm.db")
        cursor = self.db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS marketing_queries (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT, timestamp TEXT, customer_id TEXT)")
        self.db.commit()

    async def handle_request(self, request):
        method = request["method"]
        params = request["params"]
        cursor = self.db.cursor()

        if method == "log_marketing_query":
            query = params["query"]
            customer_id = params.get("customer_id", "UNKNOWN")
            timestamp = datetime.now().isoformat()
            cursor.execute("INSERT INTO marketing_queries (query, timestamp, customer_id) VALUES (?, ?, ?)", 
                          (query, timestamp, customer_id))
            self.db.commit()
            return {"result": "Query logged."}

        if method == "get_marketing_history":
            customer_id = params["customer_id"]
            cursor.execute("SELECT query, timestamp FROM marketing_queries WHERE customer_id = ?", 
                          (customer_id,))
            rows = cursor.fetchall()
            return {"result": [{"query": row[0], "timestamp": row[1]} for row in rows]}

        # Existing methods (log_query, get_history)
        # ... (from Chapter 4)

        return {"error": f"Unknown method: {method}"}

if __name__ == "__main__":
    server = CRMServer()
    server.run()


    
# Run the script from bash:
#
# python crm_server.py