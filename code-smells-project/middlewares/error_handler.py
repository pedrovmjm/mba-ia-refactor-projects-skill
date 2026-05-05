from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception(error)
        return jsonify({"erro": "Erro interno"}), 500
