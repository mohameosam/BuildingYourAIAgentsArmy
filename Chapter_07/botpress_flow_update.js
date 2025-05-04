const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:8001');
ws.on('open', () => {
    ws.send(JSON.stringify({
        action: 'subscribe_order',
        params: { order_id: workflow.order_id },
        api_key: 'SECRET_KEY'
    }));
});
ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.action === 'order_update') {
        workflow.order_status = msg.params.status;
        // Trigger Telegram message
        workflow.notify = `Order ${msg.params.order_id} updated to ${msg.params.status}`;
    }
});
ws.on('error', (err) => {
    workflow.error = `WebSocket error: ${err.message}`;
});

