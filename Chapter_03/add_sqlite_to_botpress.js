const sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('./bot_cache.db');
db.get("SELECT response FROM responses WHERE intent = ?", [workflow.intent], (err, row) => {
    if (err) {
        workflow.reply = "Error checking cache.";
        return;
    }
    if (row) {
        workflow.reply = row.response;
    } else {
        workflow.reply = "Refunds are free within 30 days. Want details?";
        db.run("INSERT INTO responses (intent, response) VALUES (?, ?)", 
               [workflow.intent, workflow.reply]);
    }
});
db.close();
