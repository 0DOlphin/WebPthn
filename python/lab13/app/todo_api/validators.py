from app.todo.models import Category

class TodoValidator:
    
    def __titleRequired(dto):
        if not dto.get('title'):
            return False, {
                'message': "Title must be provided",
                'status_code': 422
            }
        
        return True, None
    
    def __categoryExists(dto):
        category_id = dto.get('category_id')

        if  category_id and Category.query.filter_by(id=category_id).first() is None :
            return False, {
                'message': "Category does not exist",
                'status_code': 422
            }
        
        return True, None
    
    def __validate(dto, validators):
        for validator in validators:
            isValid, response = validator(dto)
            if not isValid:
                return isValid, response 

        return True, None

    def validateForCreate(dto):
        validators = [TodoValidator.__titleRequired, TodoValidator.__categoryExists]
        return TodoValidator.__validate(dto, validators)

    def validateForUpdate(dto):
        validators = [TodoValidator.__categoryExists]
        return TodoValidator.__validate(dto, validators)
