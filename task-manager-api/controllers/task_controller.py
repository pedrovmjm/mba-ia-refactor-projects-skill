from datetime import datetime

from database import db
from models.category import Category
from models.task import Task
from models.user import User
from sqlalchemy.orm import joinedload


VALID_STATUSES = {'pending', 'in_progress', 'done', 'cancelled'}
MIN_PRIORITY = 1
MAX_PRIORITY = 5


def list_tasks():
    tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
    return [serialize_task(task, include_names=True) for task in tasks]


def get_task(task_id):
    task = db.session.get(Task, task_id)
    return serialize_task(task) if task else None


def create_task(data):
    error = validate_create(data)
    if error:
        return None, error, 400

    user_error = validate_relationships(data)
    if user_error:
        return None, user_error, 404

    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 3),
        user_id=data.get('user_id'),
        category_id=data.get('category_id'),
    )
    parse_error = apply_due_date(task, data.get('due_date'), 'Formato de data inválido. Use YYYY-MM-DD')
    if parse_error:
        return None, parse_error, 400
    apply_tags(task, data.get('tags'))

    db.session.add(task)
    db.session.commit()
    return task.to_dict(), None, 201


def update_task(task_id, data):
    task = db.session.get(Task, task_id)
    if not task:
        return None, 'Task não encontrada', 404
    if not data:
        return None, 'Dados inválidos', 400

    if 'title' in data:
        error = validate_title(data['title'])
        if error:
            return None, error, 400
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return None, 'Status inválido', 400
        task.status = data['status']
    if 'priority' in data:
        if not valid_priority(data['priority']):
            return None, 'Prioridade deve ser entre 1 e 5', 400
        task.priority = data['priority']
    if 'user_id' in data:
        if data['user_id'] and not db.session.get(User, data['user_id']):
            return None, 'Usuário não encontrado', 404
        task.user_id = data['user_id']
    if 'category_id' in data:
        if data['category_id'] and not db.session.get(Category, data['category_id']):
            return None, 'Categoria não encontrada', 404
        task.category_id = data['category_id']
    if 'due_date' in data:
        parse_error = apply_due_date(task, data['due_date'], 'Formato de data inválido')
        if parse_error:
            return None, parse_error, 400
    if 'tags' in data:
        apply_tags(task, data['tags'])

    task.updated_at = datetime.utcnow()
    db.session.commit()
    return task.to_dict(), None, 200


def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return 'Task não encontrada', 404
    db.session.delete(task)
    db.session.commit()
    return None, 200


def search_tasks(args):
    query = Task.query
    term = args.get('q', '')
    if term:
        query = query.filter(db.or_(Task.title.like(f'%{term}%'), Task.description.like(f'%{term}%')))
    if args.get('status'):
        query = query.filter(Task.status == args.get('status'))
    if args.get('priority'):
        query = query.filter(Task.priority == int(args.get('priority')))
    if args.get('user_id'):
        query = query.filter(Task.user_id == int(args.get('user_id')))
    return [task.to_dict() for task in query.all()]


def task_stats():
    total = Task.query.count()
    done = Task.query.filter_by(status='done').count()
    all_tasks = Task.query.all()
    return {
        'total': total,
        'pending': Task.query.filter_by(status='pending').count(),
        'in_progress': Task.query.filter_by(status='in_progress').count(),
        'done': done,
        'cancelled': Task.query.filter_by(status='cancelled').count(),
        'overdue': sum(1 for task in all_tasks if task.is_overdue()),
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0,
    }


def serialize_task(task, include_names=False):
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    if include_names:
        data['user_name'] = task.user.name if task.user else None
        data['category_name'] = task.category.name if task.category else None
    return data


def validate_create(data):
    if not data:
        return 'Dados inválidos'
    if not data.get('title'):
        return 'Título é obrigatório'
    title_error = validate_title(data['title'])
    if title_error:
        return title_error
    if data.get('status', 'pending') not in VALID_STATUSES:
        return 'Status inválido'
    if not valid_priority(data.get('priority', 3)):
        return 'Prioridade deve ser entre 1 e 5'
    return None


def validate_title(title):
    if len(title) < 3:
        return 'Título muito curto'
    if len(title) > 200:
        return 'Título muito longo'
    return None


def valid_priority(priority):
    return MIN_PRIORITY <= priority <= MAX_PRIORITY


def validate_relationships(data):
    if data.get('user_id') and not db.session.get(User, data['user_id']):
        return 'Usuário não encontrado'
    if data.get('category_id') and not db.session.get(Category, data['category_id']):
        return 'Categoria não encontrada'
    return None


def apply_due_date(task, due_date, error_message):
    if due_date:
        try:
            task.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return error_message
    elif due_date == '':
        task.due_date = None
    return None


def apply_tags(task, tags):
    if tags is None:
        return
    task.tags = ','.join(tags) if isinstance(tags, list) else tags
