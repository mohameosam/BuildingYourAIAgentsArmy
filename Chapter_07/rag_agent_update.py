def check_auction_item(item_id, amount, bid_id):
    cached = get_cached_product(item_id)
    if cached:
        starting_bid = float(cached.split("Starting Bid: $")[1].split(",")[0])
        details = cached
    else:
        query = f"Details for item {item_id}, including starting bid and description."
        details = qa_chain.run(query)
        cache_product(item_id, details)
        starting_bid = float(details.split("Starting Bid: $")[1].split(",")[0])

    status = "confirmed" if amount >= starting_bid else "rejected"
    requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "update_order",
        "params": {"order_id": bid_id, "status": status, "item_id": item_id, "amount": amount},
        "api_key": "SECRET_KEY"
    })
    send_to_queue({"bid_id": bid_id, "action": "log_bid", "amount": amount, "item_id": item_id}, "tasks")
    return details

