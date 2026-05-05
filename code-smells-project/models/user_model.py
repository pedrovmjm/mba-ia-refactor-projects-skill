from database import get_db
from models.base import row_to_dict, rows_to_dicts


def public_user(row):
    if not row:
        return None
    user = dict(row)
    user.pop("senha", None)
    return user


def list_users():
    cursor = get_db().cursor()
    cursor.execute("SELECT id, nome, email, tipo, criado_em FROM usuarios")
    return rows_to_dicts(cursor.fetchall())


def get_user(user_id):
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT id, nome, email, tipo, criado_em FROM usuarios WHERE id = ?",
        (user_id,),
    )
    return row_to_dict(cursor.fetchone())


def get_user_by_credentials(email, password):
    cursor = get_db().cursor()
    cursor.execute(
        "SELECT id, nome, email, tipo FROM usuarios WHERE email = ? AND senha = ?",
        (email, password),
    )
    return row_to_dict(cursor.fetchone())


def create_user(data):
    cursor = get_db().cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (
            data["nome"],
            data["email"],
            data["senha"],
            data.get("tipo", "cliente"),
        ),
    )
    get_db().commit()
    return cursor.lastrowid
