const reportModel = require('../models/reportModel');

function createReportController(db) {
    return {
        financialReport: async (req, res) => {
            try {
                res.json(await reportModel.financialReport(db));
            } catch (error) {
                res.status(500).json({ error: 'Erro DB' });
            }
        }
    };
}

module.exports = { createReportController };
