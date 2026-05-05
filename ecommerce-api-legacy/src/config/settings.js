const config = {
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'dev-payment-key',
    smtpUser: process.env.SMTP_USER || 'no-reply@example.test',
    port: Number(process.env.PORT || 3000)
};

module.exports = { config };
