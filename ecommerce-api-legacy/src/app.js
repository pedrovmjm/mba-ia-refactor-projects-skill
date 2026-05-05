const express = require('express');
const { config } = require('./config/settings');
const { createDatabase } = require('./models/database');
const { createRoutes } = require('./routes');

function createApp() {
    const app = express();
    const db = createDatabase();

    app.use(express.json());
    app.use('/api', createRoutes(db));

    app.get('/health', (req, res) => {
        res.json({ status: 'ok', database: 'connected', version: '1.0.0' });
    });

    return { app, db };
}

if (require.main === module) {
    const { app } = createApp();
    app.listen(config.port, () => {
        console.log(`LMS API rodando na porta ${config.port}`);
    });
}

module.exports = { createApp };
