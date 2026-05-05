from flask import Flask
from flask_cors import CORS

from config.settings import Settings
from database import get_db
from middlewares.error_handler import register_error_handlers
from views.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Settings.SECRET_KEY
    app.config["DEBUG"] = Settings.DEBUG

    CORS(app)
    register_routes(app)
    register_error_handlers(app)

    with app.app_context():
        get_db()

    return app


app = create_app()


if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://0.0.0.0:{Settings.PORT}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=Settings.PORT, debug=Settings.DEBUG)
