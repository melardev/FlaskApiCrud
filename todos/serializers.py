from shared.serializers import PageSerializer


def get_dto(todo, include_description=False):
    data = {
        'id': todo.id,
        'title': todo.title,
        'completed': todo.completed,
    }

    if include_description:
        data['description'] = todo.description
    data['created_at'] = todo.created_at
    data['updated_at'] = todo.updated_at

    return data


class TodoDetailsSerializer():
    def __init__(self, todo):
        self.data = get_dto(todo, include_description=True)


class TodoListSerializer():

    def __init__(self, todos):
        self.data = self.items = [get_dto(todo, include_description=False) for todo in todos]
