model, index = initialize_rag_gpu(["Item ABC: Vintage Guitar, Starting Bid: $500, Description: 1965 Gibson Les Paul"])
def check_auction_item_gpu(item_id, amount, bid_id):
    details = query_rag_gpu(f"Details for item {item_id}", model, index, documents)[0]
    starting_bid = float(details.split("Starting Bid: $")[1].split(",")[0])
    status = "confirmed" if amount >= starting_bid else "rejected"
    requests.post("http://localhost:8000", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "update_order",
        "params": {"order_id": bid_id, "status": status, "item_id": item_id, "amount": amount},
        "api_key": "SECRET_KEY"
    })
    return details

start = time.time()
check_auction_item_gpu("ABC", 1000, "BID1234")
print(f"GPU inference: {time.time() - start:.2f}s")

