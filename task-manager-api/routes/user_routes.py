from flask import Blueprint, jsonify, request

from controllers import user_controller


user_bp = Blueprint('users', __name__)


@user_bp.get('/users')
def get_users():
    return jsonify(user_controller.list_users()), 200


@user_bp.get('/users/<int:user_id>')
def get_user(user_id):
    user = user_controller.get_user(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(user), 200


@user_bp.post('/users')
def create_user():
    data, error, status = user_controller.create_user(request.get_json())
    if error:
        return jsonify({'error': error}), status
    return jsonify(data), status


@user_bp.put('/users/<int:user_id>')
def update_user(user_id):
    data, error, status = user_controller.update_user(user_id, request.get_json())
    if error:
        return jsonify({'error': error}), status
    return jsonify(data), status


@user_bp.delete('/users/<int:user_id>')
def delete_user(user_id):
    error, status = user_controller.delete_user(user_id)
    if error:
        return jsonify({'error': error}), status
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200


@user_bp.get('/users/<int:user_id>/tasks')
def get_user_tasks(user_id):
    tasks, error = user_controller.user_tasks(user_id)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(tasks), 200


@user_bp.post('/login')
def login():
    data, error, status = user_controller.login(request.get_json())
    if error:
        return jsonify({'error': error}), status
    return jsonify(data), status
