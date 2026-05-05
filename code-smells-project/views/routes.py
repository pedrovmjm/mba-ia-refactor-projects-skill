from flask import jsonify, request

from controllers import order_controller, product_controller, user_controller
from database import get_db


def register_routes(app):
    @app.get("/")
    def index():
        return jsonify(
            {
                "mensagem": "Bem-vindo à API da Loja",
                "versao": "1.0.0",
                "endpoints": {
                    "produtos": "/produtos",
                    "usuarios": "/usuarios",
                    "pedidos": "/pedidos",
                    "login": "/login",
                    "relatorios": "/relatorios/vendas",
                    "health": "/health",
                },
            }
        )

    @app.get("/produtos")
    def listar_produtos():
        return jsonify({"dados": product_controller.list_products(), "sucesso": True}), 200

    @app.get("/produtos/busca")
    def buscar_produtos():
        results = product_controller.search_products(request.args)
        return jsonify({"dados": results, "total": len(results), "sucesso": True}), 200

    @app.get("/produtos/<int:product_id>")
    def buscar_produto(product_id):
        product = product_controller.get_product(product_id)
        if not product:
            return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404
        return jsonify({"dados": product, "sucesso": True}), 200

    @app.post("/produtos")
    def criar_produto():
        data, error = product_controller.create_product(request.get_json())
        if error:
            return jsonify({"erro": error}), 400
        return jsonify({"dados": data, "sucesso": True, "mensagem": "Produto criado"}), 201

    @app.put("/produtos/<int:product_id>")
    def atualizar_produto(product_id):
        error, status = product_controller.update_product(product_id, request.get_json())
        if error:
            return jsonify({"erro": error}), status
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

    @app.delete("/produtos/<int:product_id>")
    def deletar_produto(product_id):
        error, status = product_controller.delete_product(product_id)
        if error:
            return jsonify({"erro": error}), status
        return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200

    @app.get("/usuarios")
    def listar_usuarios():
        return jsonify({"dados": user_controller.list_users(), "sucesso": True}), 200

    @app.get("/usuarios/<int:user_id>")
    def buscar_usuario(user_id):
        user = user_controller.get_user(user_id)
        if not user:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        return jsonify({"dados": user, "sucesso": True}), 200

    @app.post("/usuarios")
    def criar_usuario():
        data, error = user_controller.create_user(request.get_json())
        if error:
            return jsonify({"erro": error}), 400
        return jsonify({"dados": data, "sucesso": True}), 201

    @app.post("/login")
    def login():
        user, error = user_controller.login(request.get_json())
        if error:
            return jsonify({"erro": error}), 400
        if not user:
            return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
        return jsonify({"dados": user, "sucesso": True, "mensagem": "Login OK"}), 200

    @app.post("/pedidos")
    def criar_pedido():
        data, error = order_controller.create_order(request.get_json())
        if error:
            return jsonify({"erro": error, "sucesso": False}), 400
        return jsonify({"dados": data, "sucesso": True, "mensagem": "Pedido criado com sucesso"}), 201

    @app.get("/pedidos")
    def listar_todos_pedidos():
        return jsonify({"dados": order_controller.list_orders(), "sucesso": True}), 200

    @app.get("/pedidos/usuario/<int:user_id>")
    def listar_pedidos_usuario(user_id):
        return jsonify({"dados": order_controller.list_orders(user_id), "sucesso": True}), 200

    @app.put("/pedidos/<int:order_id>/status")
    def atualizar_status_pedido(order_id):
        error = order_controller.update_status(order_id, request.get_json().get("status", ""))
        if error:
            return jsonify({"erro": error}), 400
        return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200

    @app.get("/relatorios/vendas")
    def relatorio_vendas():
        return jsonify({"dados": order_controller.sales_report(), "sucesso": True}), 200

    @app.get("/health")
    def health_check():
        cursor = get_db().cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        products = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        orders = cursor.fetchone()[0]
        return jsonify(
            {
                "status": "ok",
                "database": "connected",
                "counts": {"produtos": products, "usuarios": users, "pedidos": orders},
                "versao": "1.0.0",
            }
        ), 200

    @app.post("/admin/reset-db")
    def reset_database():
        cursor = get_db().cursor()
        for table in ("itens_pedido", "pedidos", "produtos", "usuarios"):
            cursor.execute(f"DELETE FROM {table}")
        get_db().commit()
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200

    @app.post("/admin/query")
    def executar_query():
        return jsonify({"erro": "Endpoint desabilitado por segurança"}), 403
