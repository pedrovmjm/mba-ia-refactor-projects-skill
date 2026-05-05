const express = require('express');
const { createCheckoutController } = require('../controllers/checkoutController');
const { createReportController } = require('../controllers/reportController');
const { createUserController } = require('../controllers/userController');

function createRoutes(db) {
    const router = express.Router();
    const checkoutController = createCheckoutController(db);
    const reportController = createReportController(db);
    const userController = createUserController(db);

    router.post('/checkout', checkoutController.checkout);
    router.get('/admin/financial-report', reportController.financialReport);
    router.delete('/users/:id', userController.deleteUser);

    return router;
}

module.exports = { createRoutes };
