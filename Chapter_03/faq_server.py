from mcp import Server
import sqlite3

class FAQServer(Server):
    def __init__(self):
        super().__init__(name="faq-server", transport="http")
        self.db = sqlite3.connect("faq.db")

    async def handle_request(self, request):
        if request["method"] == "get_answer":
            question = request["params"]["question"]
            cursor = self.db.cursor()
            cursor.execute("SELECT answer FROM faqs WHERE question = ?", (question,))
            row = cursor.fetchone()
            return {"result": row[0] if row else "No answer found."}
        return {"error": "Unknown method."}

if __name__ == "__main__":
    server = FAQServer()
    server.run()


    
# Run the script from bash:
#
# python faq_server.py