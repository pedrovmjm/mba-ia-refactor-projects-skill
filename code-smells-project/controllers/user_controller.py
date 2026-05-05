from models import user_model


def list_users():
    return user_model.list_users()


def get_user(user_id):
    return user_model.get_user(user_id)


def create_user(payload):
    if not payload:
        return None, "Dados inválidos"
    nome = payload.get("nome", "")
    email = payload.get("email", "")
    senha = payload.get("senha", "")
    if not nome or not email or not senha:
        return None, "Nome, email e senha são obrigatórios"
    return {"id": user_model.create_user(payload)}, None


def login(payload):
    if not payload:
        return None, "Email e senha são obrigatórios"
    email = payload.get("email", "")
    senha = payload.get("senha", "")
    if not email or not senha:
        return None, "Email e senha são obrigatórios"
    return user_model.get_user_by_credentials(email, senha), None
