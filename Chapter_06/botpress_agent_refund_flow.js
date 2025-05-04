const fetch = require('node-fetch');
const response = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        jsonrpc: '2.0',
        id: 3,
        method: 'update_order',
        params: { order_id: workflow.order_id || 'UNKNOWN', status: 'refunded' },
        api_key: 'SECRET_KEY'
    })
});
const data = await response.json();
if (data.error) {
    workflow.error = data.error;
} else {
    workflow.order_status = 'refunded';

}

