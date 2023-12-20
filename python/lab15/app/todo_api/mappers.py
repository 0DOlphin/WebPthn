from app.todo.models import Todo
from datetime import datetime

class TodoMapper():
    
    def toDto(todo):
        return {
            "id": todo.id,
            "title": todo.title, 
            "due_date": todo.due_date.strftime("%Y-%m-%d") if  todo.due_date else None, 
            "complete": todo.complete,
            "category_id": todo.category_id
        }
    
    def toEntity(dto):
        return Todo(
            title = dto.get('title'), 
            due_date = datetime.strptime(dto.get('due_date'), "%Y-%m-%d").date() if dto.get('due_date') else None, 
            category_id = dto.get('category_id'),
            complete = dto.get('complete', False)
        )
    
    def updateFromDto(todo, dto):
        title = dto.get('title')
        due_date = dto.get('due_date')
        complete = dto.get('complete')
        category_id = dto.get('category_id')

        if title:
            todo.title = title

        if due_date:
            todo.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        if complete:
            todo.complete = complete

        if category_id:
            todo.category_id = category_id

        return todo
