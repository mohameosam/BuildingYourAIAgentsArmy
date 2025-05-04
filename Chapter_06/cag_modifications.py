def check_inventory(product, quantity, order_id):
    cached = get_cached_product(product)
    if cached:
        stock = int(cached.split("in stock")[0].split()[-1]) if "in stock" in cached.lower() else 0
        price = float(cached.split("$")[1].split(",")[0])
        details = cached
    else:
        query = f"Is {quantity} {product}(s) in stock? Include stock count, price."
        details = qa_chain.run(query)
        cache_product(product, details)
        stock = int(details.split("in stock")[0].split()[-1]) if "in stock" in details.lower() else 0
        price = float(details.split("$")[1].split(",")[0])
    
    if stock < 5:
        price *= 1.1  # 10% markup
    status = "confirmed" if stock >= quantity else "partial" if stock > 0 else "out_of_stock"
    if status == "partial":
        details += f" Only {stock} available."
    
    requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "update_order",
        "params": {"order_id": order_id, "status": status, "price": price * quantity},
        "api_key": "SECRET_KEY"
    })
    return details
