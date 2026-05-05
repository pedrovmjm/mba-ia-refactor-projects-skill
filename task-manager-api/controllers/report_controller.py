from datetime import datetime, timedelta

from database import db
from models.category import Category
from models.task import Task
from models.user import User
from utils.helpers import calculate_percentage


def summary_report():
    total_tasks = Task.query.count()
    done = Task.query.filter_by(status='done').count()
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    overdue_tasks = [
        {
            'id': task.id,
            'title': task.title,
            'due_date': str(task.due_date),
            'days_overdue': (datetime.utcnow() - task.due_date).days,
        }
        for task in Task.query.all()
        if task.is_overdue()
    ]

    return {
        'generated_at': str(datetime.utcnow()),
        'overview': {
            'total_tasks': total_tasks,
            'total_users': User.query.count(),
            'total_categories': Category.query.count(),
        },
        'tasks_by_status': {
            status: Task.query.filter_by(status=status).count()
            for status in ['pending', 'in_progress', 'done', 'cancelled']
        },
        'tasks_by_priority': {
            'critical': Task.query.filter_by(priority=1).count(),
            'high': Task.query.filter_by(priority=2).count(),
            'medium': Task.query.filter_by(priority=3).count(),
            'low': Task.query.filter_by(priority=4).count(),
            'minimal': Task.query.filter_by(priority=5).count(),
        },
        'overdue': {'count': len(overdue_tasks), 'tasks': overdue_tasks},
        'recent_activity': {
            'tasks_created_last_7_days': Task.query.filter(Task.created_at >= seven_days_ago).count(),
            'tasks_completed_last_7_days': Task.query.filter(
                Task.status == 'done', Task.updated_at >= seven_days_ago
            ).count(),
        },
        'user_productivity': user_productivity(),
        'completion_rate': calculate_percentage(done, total_tasks),
    }


def user_report(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None
    tasks = Task.query.filter_by(user_id=user_id).all()
    total = len(tasks)
    done = sum(1 for task in tasks if task.status == 'done')
    return {
        'user': {'id': user.id, 'name': user.name, 'email': user.email},
        'statistics': {
            'total_tasks': total,
            'done': done,
            'pending': sum(1 for task in tasks if task.status == 'pending'),
            'in_progress': sum(1 for task in tasks if task.status == 'in_progress'),
            'cancelled': sum(1 for task in tasks if task.status == 'cancelled'),
            'overdue': sum(1 for task in tasks if task.is_overdue()),
            'high_priority': sum(1 for task in tasks if task.priority <= 2),
            'completion_rate': calculate_percentage(done, total),
        },
    }


def list_categories():
    return [
        {**category.to_dict(), 'task_count': Task.query.filter_by(category_id=category.id).count()}
        for category in Category.query.all()
    ]


def create_category(data):
    if not data:
        return None, 'Dados inválidos', 400
    if not data.get('name'):
        return None, 'Nome é obrigatório', 400
    category = Category(
        name=data['name'],
        description=data.get('description', ''),
        color=data.get('color', '#000000'),
    )
    db.session.add(category)
    db.session.commit()
    return category.to_dict(), None, 201


def update_category(category_id, data):
    category = db.session.get(Category, category_id)
    if not category:
        return None, 'Categoria não encontrada', 404
    if 'name' in data:
        category.name = data['name']
    if 'description' in data:
        category.description = data['description']
    if 'color' in data:
        category.color = data['color']
    db.session.commit()
    return category.to_dict(), None, 200


def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return 'Categoria não encontrada', 404
    db.session.delete(category)
    db.session.commit()
    return None, 200


def user_productivity():
    stats = []
    for user in User.query.all():
        total = len(user.tasks)
        completed = sum(1 for task in user.tasks if task.status == 'done')
        stats.append({
            'user_id': user.id,
            'user_name': user.name,
            'total_tasks': total,
            'completed_tasks': completed,
            'completion_rate': calculate_percentage(completed, total),
        })
    return stats
