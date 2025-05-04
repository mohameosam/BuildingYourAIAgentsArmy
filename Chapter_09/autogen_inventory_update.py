support_agent.system_message = "Handle queries and escalate stock checks to StockAgent."
def handle_query(query):
    if "stock" in query.lower():
        return stock_check_tool(query.split()[-1])
    return "Please clarify your request."

support_agent.register_function(handle_query)
