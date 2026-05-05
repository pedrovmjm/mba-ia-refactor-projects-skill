from database import get_db


def create_order(user_id, items, total):
    cursor = get_db().cursor()
    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (user_id, total),
    )
    return cursor.lastrowid


def add_order_item(order_id, item, unit_price):
    cursor = get_db().cursor()
    cursor.execute(
        """
        INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
        VALUES (?, ?, ?, ?)
        """,
        (order_id, item["produto_id"], item["quantidade"], unit_price),
    )


def decrement_stock(product_id, quantity):
    cursor = get_db().cursor()
    cursor.execute(
        "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
        (quantity, product_id),
    )


def list_orders(user_id=None):
    cursor = get_db().cursor()
    params = []
    where = ""
    if user_id is not None:
        where = "WHERE p.usuario_id = ?"
        params.append(user_id)

    cursor.execute(
        f"""
        SELECT
            p.id AS pedido_id,
            p.usuario_id,
            p.status,
            p.total,
            p.criado_em,
            i.produto_id,
            i.quantidade,
            i.preco_unitario,
            pr.nome AS produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido i ON i.pedido_id = p.id
        LEFT JOIN produtos pr ON pr.id = i.produto_id
        {where}
        ORDER BY p.id
        """,
        params,
    )
    return _group_orders(cursor.fetchall())


def _group_orders(rows):
    orders = {}
    for row in rows:
        order_id = row["pedido_id"]
        if order_id not in orders:
            orders[order_id] = {
                "id": order_id,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": [],
            }
        if row["produto_id"] is not None:
            orders[order_id]["itens"].append(
                {
                    "produto_id": row["produto_id"],
                    "produto_nome": row["produto_nome"] or "Desconhecido",
                    "quantidade": row["quantidade"],
                    "preco_unitario": row["preco_unitario"],
                }
            )
    return list(orders.values())


def update_order_status(order_id, status):
    cursor = get_db().cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (status, order_id),
    )
    get_db().commit()


def sales_report():
    cursor = get_db().cursor()
    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_pedidos,
            COALESCE(SUM(total), 0) AS faturamento,
            SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) AS pendentes,
            SUM(CASE WHEN status = 'aprovado' THEN 1 ELSE 0 END) AS aprovados,
            SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
        FROM pedidos
        """
    )
    row = cursor.fetchone()
    total = row["total_pedidos"]
    revenue = row["faturamento"]
    discount = 0
    if revenue > 10000:
        discount = revenue * 0.1
    elif revenue > 5000:
        discount = revenue * 0.05
    elif revenue > 1000:
        discount = revenue * 0.02

    return {
        "total_pedidos": total,
        "faturamento_bruto": round(revenue, 2),
        "desconto_aplicavel": round(discount, 2),
        "faturamento_liquido": round(revenue - discount, 2),
        "pedidos_pendentes": row["pendentes"] or 0,
        "pedidos_aprovados": row["aprovados"] or 0,
        "pedidos_cancelados": row["cancelados"] or 0,
        "ticket_medio": round(revenue / total, 2) if total > 0 else 0,
    }
