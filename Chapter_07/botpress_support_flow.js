const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:8001');
ws.on('open', () => {
    workflow.client_id = `CUST${Math.random().toString().slice(2,6)}`;
    ws.send(JSON.stringify({
        action: 'send_message',
        params: {
            recipient_id: 'SUPPORT001',
            content: workflow.message || 'Customer needs help'
        },
        api_key: 'SECRET_KEY'
    }));
});
ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.action === 'receive_message') {
        workflow.response = `Support: ${msg.params.content}`;
    }
});

