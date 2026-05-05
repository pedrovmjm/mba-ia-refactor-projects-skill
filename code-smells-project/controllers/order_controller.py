from database import get_db
from models import order_model, product_model
from services.notification_service import notify_order_created, notify_order_status


VALID_STATUSES = {"pendente", "aprovado", "enviado", "entregue", "cancelado"}


def create_order(payload):
    if not payload:
        return None, "Dados inválidos"
    user_id = payload.get("usuario_id")
    items = payload.get("itens", [])
    if not user_id:
        return None, "Usuario ID é obrigatório"
    if not items:
        return None, "Pedido deve ter pelo menos 1 item"

    total = 0
    products = {}
    for item in items:
        product = product_model.get_product(item["produto_id"])
        if product is None:
            return None, f"Produto {item['produto_id']} não encontrado"
        if product["estoque"] < item["quantidade"]:
            return None, "Estoque insuficiente para " + product["nome"]
        products[item["produto_id"]] = product
        total += product["preco"] * item["quantidade"]

    order_id = order_model.create_order(user_id, items, total)
    for item in items:
        product = products[item["produto_id"]]
        order_model.add_order_item(order_id, item, product["preco"])
        order_model.decrement_stock(item["produto_id"], item["quantidade"])
    get_db().commit()
    notify_order_created(order_id, user_id)
    return {"pedido_id": order_id, "total": total}, None


def list_orders(user_id=None):
    return order_model.list_orders(user_id)


def update_status(order_id, status):
    if status not in VALID_STATUSES:
        return "Status inválido"
    order_model.update_order_status(order_id, status)
    notify_order_status(order_id, status)
    return None


def sales_report():
    return order_model.sales_report()
