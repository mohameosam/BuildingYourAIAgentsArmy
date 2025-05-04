def order_processor_tool(item_id, quantity):
    order_id = f"ORD{random.randint(1000, 9999)}"
    response = requests.post("http://localhost:5678/webhook/process-order", json={
        "item_id": item_id,
        "quantity": quantity,
        "order_id": order_id
    })
    return {"order_id": order_id, "status": response.json().get("status", "confirmed")}

order_processor.tools = [order_processor_tool]

