def check_auction_item(item_id, amount, bid_id):
    cached = get_cached_product(item_id)
    if cached:
        starting_bid = float(cached["starting_bid"])
        details = cached["description"]
    else:
        details = qa_chain.run(f"Details for item {item_id}")
        starting_bid = float(details.split("Starting Bid: $")[1].split(",")[0])
        cache_product(item_id, {"starting_bid": starting_bid, "description": details})
    status = "confirmed" if amount >= starting_bid else "rejected"
    requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "update_order",
        "params": {"order_id": bid_id, "status": status, "item_id": item_id, "amount": amount},
        "api_key": "SECRET_KEY"
    })
    return details

