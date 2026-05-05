const { run } = require('./database');

function createEnrollment(db, userId, courseId) {
    return run(db, 'INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)', [userId, courseId]);
}

module.exports = { createEnrollment };
