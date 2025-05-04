const fetch = require('node-fetch');
const response = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        jsonrpc: '2.0',
        id: 2,
        method: 'get_order_status',
        params: { order_id: workflow.order_id || 'UNKNOWN' },
        api_key: 'SECRET_KEY'
    })
});
const data = await response.json();
if (data.error) {
    workflow.error = data.error;
} else {
    workflow.order_status = data.result.status;
    workflow.product = data.result.product;
    workflow.quantity = data.result.quantity;
}

