const fetch = require('node-fetch');
const order_id = `ORD${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
if (!workflow.product || workflow.quantity <= 0) {
    workflow.error = "Invalid product or quantity";
    return;
}
const response = await fetch('http://localhost:8000', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        jsonrpc: '2.0',
        id: 1,
        method: 'submit_order',
        params: {
            order_id: order_id,
            product: workflow.product,
            quantity: workflow.quantity || 1,
            customer_id: workflow.userId || 'CUST001'
        },
        api_key: 'SECRET_KEY'
    })
});
const data = await response.json();
if (data.error) {
    workflow.error = data.error;
} else {
    workflow.order_id = order_id;
    workflow.order_status = data.result.status;
}

