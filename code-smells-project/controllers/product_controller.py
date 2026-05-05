from models import product_model


VALID_CATEGORIES = {"informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"}


def list_products():
    return product_model.list_products()


def get_product(product_id):
    return product_model.get_product(product_id)


def create_product(payload):
    error = validate_product_payload(payload)
    if error:
        return None, error
    product_id = product_model.create_product(payload)
    return {"id": product_id}, None


def update_product(product_id, payload):
    if not product_model.get_product(product_id):
        return "Produto não encontrado", 404
    error = validate_product_payload(payload)
    if error:
        return error, 400
    product_model.update_product(product_id, payload)
    return None, 200


def delete_product(product_id):
    if not product_model.get_product(product_id):
        return "Produto não encontrado", 404
    product_model.delete_product(product_id)
    return None, 200


def search_products(args):
    price_min = _optional_float(args.get("preco_min"))
    price_max = _optional_float(args.get("preco_max"))
    return product_model.search_products(
        args.get("q", ""),
        args.get("categoria"),
        price_min,
        price_max,
    )


def validate_product_payload(payload):
    if not payload:
        return "Dados inválidos"
    for field, label in (("nome", "Nome"), ("preco", "Preço"), ("estoque", "Estoque")):
        if field not in payload:
            return f"{label} é obrigatório"
    if payload["preco"] < 0:
        return "Preço não pode ser negativo"
    if payload["estoque"] < 0:
        return "Estoque não pode ser negativo"
    if len(payload["nome"]) < 2:
        return "Nome muito curto"
    if len(payload["nome"]) > 200:
        return "Nome muito longo"
    if payload.get("categoria", "geral") not in VALID_CATEGORIES:
        return "Categoria inválida. Válidas: " + str(sorted(VALID_CATEGORIES))
    return None


def _optional_float(value):
    return float(value) if value not in (None, "") else None
