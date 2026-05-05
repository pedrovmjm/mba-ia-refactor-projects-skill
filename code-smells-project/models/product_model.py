from database import get_db
from models.base import row_to_dict, rows_to_dicts


def list_products():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM produtos")
    return rows_to_dicts(cursor.fetchall())


def get_product(product_id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
    return row_to_dict(cursor.fetchone())


def create_product(data):
    cursor = get_db().cursor()
    cursor.execute(
        """
        INSERT INTO produtos (nome, descricao, preco, estoque, categoria)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["nome"],
            data.get("descricao", ""),
            data["preco"],
            data["estoque"],
            data.get("categoria", "geral"),
        ),
    )
    get_db().commit()
    return cursor.lastrowid


def update_product(product_id, data):
    cursor = get_db().cursor()
    cursor.execute(
        """
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ?
        WHERE id = ?
        """,
        (
            data["nome"],
            data.get("descricao", ""),
            data["preco"],
            data["estoque"],
            data.get("categoria", "geral"),
            product_id,
        ),
    )
    get_db().commit()


def delete_product(product_id):
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    get_db().commit()


def search_products(term="", category=None, price_min=None, price_max=None):
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []
    if term:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        params.extend([f"%{term}%", f"%{term}%"])
    if category:
        query += " AND categoria = ?"
        params.append(category)
    if price_min is not None:
        query += " AND preco >= ?"
        params.append(price_min)
    if price_max is not None:
        query += " AND preco <= ?"
        params.append(price_max)

    cursor = get_db().cursor()
    cursor.execute(query, params)
    return rows_to_dicts(cursor.fetchall())
