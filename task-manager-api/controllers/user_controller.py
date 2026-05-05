import re

from database import db
from models.task import Task
from models.user import User


EMAIL_PATTERN = r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$'
VALID_ROLES = {'user', 'admin', 'manager'}


def list_users():
    return [serialize_user(user) for user in User.query.all()]


def get_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None
    data = user.to_dict()
    data['tasks'] = [task.to_dict() for task in Task.query.filter_by(user_id=user_id).all()]
    return data


def create_user(data):
    error, status = validate_user_payload(data, require_password=True)
    if error:
        return None, error, status
    user = User(name=data['name'], email=data['email'], role=data.get('role', 'user'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), None, 201


def update_user(user_id, data):
    user = db.session.get(User, user_id)
    if not user:
        return None, 'Usuário não encontrado', 404
    if not data:
        return None, 'Dados inválidos', 400

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        email_error = validate_email(data['email'], user_id)
        if email_error:
            return None, email_error[0], email_error[1]
        user.email = data['email']
    if 'password' in data:
        if len(data['password']) < 4:
            return None, 'Senha muito curta', 400
        user.set_password(data['password'])
    if 'role' in data:
        if data['role'] not in VALID_ROLES:
            return None, 'Role inválido', 400
        user.role = data['role']
    if 'active' in data:
        user.active = data['active']

    db.session.commit()
    return user.to_dict(), None, 200


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return 'Usuário não encontrado', 404
    Task.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return None, 200


def user_tasks(user_id):
    if not db.session.get(User, user_id):
        return None, 'Usuário não encontrado'
    return [serialize_user_task(task) for task in Task.query.filter_by(user_id=user_id).all()], None


def login(data):
    if not data:
        return None, 'Dados inválidos', 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return None, 'Email e senha são obrigatórios', 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return None, 'Credenciais inválidas', 401
    if not user.active:
        return None, 'Usuário inativo', 403
    return {
        'message': 'Login realizado com sucesso',
        'user': user.to_dict(),
        'token_type': 'development',
        'token': f'dev-token-{user.id}'
    }, None, 200


def serialize_user(user):
    data = user.to_dict()
    data['task_count'] = len(user.tasks)
    return data


def serialize_user_task(task):
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    return data


def validate_user_payload(data, require_password=False):
    if not data:
        return 'Dados inválidos', 400
    for field, message in (('name', 'Nome é obrigatório'), ('email', 'Email é obrigatório')):
        if not data.get(field):
            return message, 400
    if require_password and not data.get('password'):
        return 'Senha é obrigatória', 400
    email_error = validate_email(data['email'])
    if email_error:
        return email_error
    if require_password and len(data['password']) < 4:
        return 'Senha deve ter no mínimo 4 caracteres', 400
    if data.get('role', 'user') not in VALID_ROLES:
        return 'Role inválido', 400
    return None, 200


def validate_email(email, current_user_id=None):
    if not re.match(EMAIL_PATTERN, email):
        return 'Email inválido', 400
    existing = User.query.filter_by(email=email).first()
    if existing and existing.id != current_user_id:
        return 'Email já cadastrado', 409
    return None
