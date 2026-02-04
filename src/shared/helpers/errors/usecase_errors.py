from src.shared.helpers.errors.base_error import BaseError

class NoItemsFound(BaseError):
    def __init__(self, message: str):
        super().__init__(f'No items found for {message}')

class DuplicatedItem(BaseError):
    def __init__(self, message: str):
        super().__init__(f'The item already exists for this {message}')
        
class ForbiddenAction(BaseError):
    def __init__(self, message: str):
        super().__init__(message=message)