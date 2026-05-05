const courseModel = require('../models/courseModel');
const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const auditLogModel = require('../models/auditLogModel');
const { hashPassword } = require('./passwordService');
const { processPayment } = require('./paymentService');

async function checkout(db, payload) {
    const normalized = normalizePayload(payload);
    const validationError = validate(normalized);
    if (validationError) {
        return { statusCode: 400, body: { error: validationError } };
    }

    const course = await courseModel.findActiveCourse(db, normalized.courseId);
    if (!course) {
        return { statusCode: 404, body: { error: 'Curso não encontrado' } };
    }

    let user = await userModel.findByEmail(db, normalized.email);
    if (!user) {
        const created = await userModel.createUser(db, {
            name: normalized.name,
            email: normalized.email,
            passwordHash: hashPassword(normalized.password || '123456')
        });
        user = { id: created.id, name: normalized.name, email: normalized.email };
    }

    const paymentDecision = processPayment(normalized.card);
    if (paymentDecision.status === 'DENIED') {
        return { statusCode: 400, body: { error: 'Pagamento recusado' } };
    }

    const enrollment = await enrollmentModel.createEnrollment(db, user.id, normalized.courseId);
    await paymentModel.createPayment(db, enrollment.id, course.price, paymentDecision.status);
    await auditLogModel.record(db, `Checkout curso ${normalized.courseId} por ${user.id}`);

    return { statusCode: 200, body: { msg: 'Sucesso', enrollment_id: enrollment.id } };
}

function normalizePayload(payload = {}) {
    return {
        name: payload.name || payload.usr,
        email: payload.email || payload.eml,
        password: payload.password || payload.pwd,
        courseId: payload.course_id || payload.c_id,
        card: payload.card
    };
}

function validate(payload) {
    if (!payload.name || !payload.email || !payload.courseId || !payload.card) {
        return 'Bad Request';
    }
    return null;
}

module.exports = { checkout };
