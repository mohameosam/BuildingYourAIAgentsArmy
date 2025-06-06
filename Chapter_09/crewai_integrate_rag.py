def stock_checker_tool(item_id):
    cached = redis_client.get(item_id)
    if cached:
        return json.loads(cached)
    details = query_rag_gpu(f"Stock for item {item_id}", model, index, documents)
    quantity = int(details.split("Quantity: ")[1].split(",")[0])
    redis_client.setex(item_id, 3600, json.dumps({"item_id": item_id, "quantity": quantity}))
    return {"item_id": item_id, "quantity": quantity}

stock_checker.tools = [stock_checker_tool]
