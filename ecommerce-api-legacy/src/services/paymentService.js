const { config } = require('../config/settings');

function processPayment(cardNumber) {
    const status = String(cardNumber || '').startsWith('4') ? 'PAID' : 'DENIED';
    return {
        status,
        provider: config.paymentGatewayKey === 'dev-payment-key' ? 'local-simulator' : 'configured-gateway'
    };
}

module.exports = { processPayment };
