def run_inventory_crew(item_id, quantity):
    stock = stock_checker_tool(item_id)
    if stock["quantity"] >= quantity:
        result = process_order_task.execute(inputs={"item_id": item_id, "quantity": quantity})
        send_to_kafka({"order_id": result["order_id"], "action": "notify", "recipient": "customer@example.com"})
        return result
    return {"item_id": item_id, "status": "out_of_stock"}

