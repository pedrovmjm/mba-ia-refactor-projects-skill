const checkoutService = require('../services/checkoutService');

function createCheckoutController(db) {
    return {
        checkout: async (req, res) => {
            try {
                const result = await checkoutService.checkout(db, req.body);
                res.status(result.statusCode).json(result.body);
            } catch (error) {
                res.status(500).json({ error: 'Erro interno' });
            }
        }
    };
}

module.exports = { createCheckoutController };
