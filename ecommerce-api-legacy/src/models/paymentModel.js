const { run } = require('./database');

function createPayment(db, enrollmentId, amount, status) {
    return run(
        db,
        'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
        [enrollmentId, amount, status]
    );
}

module.exports = { createPayment };
