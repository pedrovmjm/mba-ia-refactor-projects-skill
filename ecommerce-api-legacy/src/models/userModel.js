const { get, run } = require('./database');

function findByEmail(db, email) {
    return get(db, 'SELECT id, name, email FROM users WHERE email = ?', [email]);
}

function createUser(db, user) {
    return run(
        db,
        'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
        [user.name, user.email, user.passwordHash]
    );
}

function deleteUser(db, userId) {
    return run(db, 'DELETE FROM users WHERE id = ?', [userId]);
}

module.exports = { findByEmail, createUser, deleteUser };
