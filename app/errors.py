class APIError(Exception):
    status_code = 500
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
    def to_dict(self):
        return {'error': self.message}

class ValidationError(APIError):
    status_code = 400

class NotFoundError(APIError):
    status_code = 404

class DatabaseError(APIError):
    status_code = 500
