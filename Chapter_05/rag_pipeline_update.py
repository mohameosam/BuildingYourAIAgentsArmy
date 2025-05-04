def send_to_n8n(query, response, customer_id="CUST001", email="customer@example.com"):
    requests.post("http://localhost:5678/webhook/customer-query", json={
        "query": query,
        "response": response,
        "customer_id": customer_id,
        "email": email
    })

# Update query logic
if not cached:
    response = qa_chain.run(query)
    cache_response(query, response)
    log_to_crm(query)
    send_to_n8n(query, response)

