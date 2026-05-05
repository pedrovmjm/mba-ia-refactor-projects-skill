from flask import Blueprint, jsonify, request

from controllers import report_controller


report_bp = Blueprint('reports', __name__)


@report_bp.get('/reports/summary')
def summary_report():
    return jsonify(report_controller.summary_report()), 200


@report_bp.get('/reports/user/<int:user_id>')
def user_report(user_id):
    report = report_controller.user_report(user_id)
    if not report:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    return jsonify(report), 200


@report_bp.get('/categories')
def get_categories():
    return jsonify(report_controller.list_categories()), 200


@report_bp.post('/categories')
def create_category():
    data, error, status = report_controller.create_category(request.get_json())
    if error:
        return jsonify({'error': error}), status
    return jsonify(data), status


@report_bp.put('/categories/<int:cat_id>')
def update_category(cat_id):
    data, error, status = report_controller.update_category(cat_id, request.get_json() or {})
    if error:
        return jsonify({'error': error}), status
    return jsonify(data), status


@report_bp.delete('/categories/<int:cat_id>')
def delete_category(cat_id):
    error, status = report_controller.delete_category(cat_id)
    if error:
        return jsonify({'error': error}), status
    return jsonify({'message': 'Categoria deletada'}), 200
