import requests

def log_to_crm(query, customer_id="CUST001"):
    response = requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "log_marketing_query",
        "params": {"query": query, "customer_id": customer_id}
    })
    return response.json()

def get_crm_history(customer_id="CUST001"):
    response = requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "get_marketing_history",
        "params": {"customer_id": customer_id}
    })
    return response.json()["result"]

# Update query logic
query = "What are the top tech trends for 2025?"
cached = get_cached_response(query)
if cached:
    response = cached
else:
    response = qa_chain.run(query)
    cache_response(query, response)
    log_to_crm(query)
history = get_crm_history()
print("Response:", response)
print("History:", history)
