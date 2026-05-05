const { get, all } = require('./database');

function findActiveCourse(db, courseId) {
    return get(db, 'SELECT * FROM courses WHERE id = ? AND active = 1', [courseId]);
}

function listCourses(db) {
    return all(db, 'SELECT * FROM courses ORDER BY id');
}

module.exports = { findActiveCourse, listCourses };
