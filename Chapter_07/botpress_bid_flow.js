const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:8001');
const bid_id = `BID${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
ws.on('open', () => {
    ws.send(JSON.stringify({
        action: 'update_order',
        params: {
            order_id: bid_id,
            status: 'pending',
            item_id: workflow.item_id,
            amount: workflow.amount
        },
        api_key: 'SECRET_KEY'
    }));
    ws.send(JSON.stringify({
        action: 'subscribe_order',
        params: { order_id: bid_id },
        api_key: 'SECRET_KEY'
    }));
});
ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.action === 'order_update') {
        workflow.notify = `Bid ${msg.params.order_id} on ${workflow.item_id}: ${msg.params.status}`;
    }
});
workflow.bid_id = bid_id;

