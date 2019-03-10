from flask import request, jsonify
from sqlalchemy import desc
from sqlalchemy.orm import load_only

from api_crud.factory import db
from routes import blueprint
from shared.serializers import get_error_response
from todos.models import Todo
from todos.serializers import TodoListSerializer, TodoDetailsSerializer


@blueprint.route('/todos', methods=['GET'])
# @cross_origin() Not needed , we enabled cors app wide
def list_todos():
    return get_todos_page()


@blueprint.route('/todos/pending', methods=['GET'])
def pending_todos():
    return get_todos_page(completed=False)


@blueprint.route('/todos/completed', methods=['GET'])
def completed_todos():
    return get_todos_page(completed=True)


def get_todos_page(completed=None):
    todos = Todo.query.order_by(desc(Todo.created_at)).options(
        load_only('id', 'title', 'completed', 'created_at', 'updated_at'))
    if completed:
        todos = todos.filter_by(completed=True)
    elif completed is False:
        todos = todos.filter_by(completed=False)
    todos = todos.all()
    return jsonify(TodoListSerializer(todos).data), 200


@blueprint.route('/todos/<id>', methods=['GET'])
def show_todo(id):
    todo = Todo.query.get(id)
    return jsonify(TodoDetailsSerializer(todo).data), 200


@blueprint.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    todo = Todo(title=data.get('title'), description=data.get('description', ''),
                completed=data.get('completed', False))

    db.session.add(todo)
    db.session.commit()

    return jsonify(TodoDetailsSerializer(todo).data), 201


@blueprint.route('/todos/<id>', methods=['PUT'])
def update_comment(id):
    todo = Todo.query.get(id)
    if todo is None:
        return get_error_response(messages='not found', status_code=404)
    todo.title = request.json.get('title')
    description = request.json.get('description', None)

    if description is not None:
        todo.description = description

    todo.completed = request.json.get('completed')
    db.session.commit()
    return jsonify(TodoDetailsSerializer(todo).data), 200


@blueprint.route('/todos/<id>', methods=['DELETE'])
def destroy_comment(id):
    todo = Todo.query.get(id)
    if todo is None:
        return get_error_response(messages='not found', status_code=404)
    db.session.delete(todo)
    db.session.commit()
    return '', 204


@blueprint.route('/todos', methods=['DELETE'])
def destroy_all():
    # db.session.query(Todo).delete()
    Todo.query.delete()
    db.session.commit()
    return '', 204
