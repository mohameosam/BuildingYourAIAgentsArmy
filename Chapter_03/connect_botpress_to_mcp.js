const fetch = require('node-fetch');
async function getFAQ() {
    const response = await fetch('http://localhost:8000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'get_answer',
            params: { question: 'What’s your shipping cost?' }
        })
    });
    const data = await response.json();
    workflow.reply = data.result || 'Sorry, I don’t know that one!';
}
getFAQ();

