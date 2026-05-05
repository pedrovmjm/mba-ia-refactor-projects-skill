const userModel = require('../models/userModel');

function createUserController(db) {
    return {
        deleteUser: async (req, res) => {
            try {
                await userModel.deleteUser(db, req.params.id);
                res.json({ message: 'Usuário deletado' });
            } catch (error) {
                res.status(500).json({ error: 'Erro ao deletar usuário' });
            }
        }
    };
}

module.exports = { createUserController };
