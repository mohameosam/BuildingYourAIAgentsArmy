const fetch = require('node-fetch');
fetch('http://localhost:5678/webhook/customer-query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        query: workflow.userInput,
        intent: workflow.intent,
        customer_id: workflow.userId || 'CUST001',
        timestamp: new Date().toISOString()
    })
});

