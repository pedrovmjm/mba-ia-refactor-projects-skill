const { all } = require('./database');

async function financialReport(db) {
    const rows = await all(
        db,
        `
        SELECT
            c.id AS course_id,
            c.title AS course,
            u.name AS student,
            p.amount AS paid,
            p.status AS payment_status
        FROM courses c
        LEFT JOIN enrollments e ON e.course_id = c.id
        LEFT JOIN users u ON u.id = e.user_id
        LEFT JOIN payments p ON p.enrollment_id = e.id
        ORDER BY c.id, u.name
        `
    );

    const byCourse = new Map();
    rows.forEach((row) => {
        if (!byCourse.has(row.course_id)) {
            byCourse.set(row.course_id, { course: row.course, revenue: 0, students: [] });
        }
        const course = byCourse.get(row.course_id);
        if (row.student) {
            if (row.payment_status === 'PAID') {
                course.revenue += row.paid || 0;
            }
            course.students.push({ student: row.student, paid: row.paid || 0 });
        }
    });
    return Array.from(byCourse.values());
}

module.exports = { financialReport };
