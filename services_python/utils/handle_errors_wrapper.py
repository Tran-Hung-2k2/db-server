from functools import wraps
from services_python.utils.exception import MyException
from fastapi import status


def handle_database_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MyException as e:
            # Nếu là MyException, raise nó để chuyển tiếp
            raise
        except Exception as e:
            # Xử lý các loại exception khác và raise MyException
            print(f"Error: {e}")
            raise MyException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error: {e}",
            )

    return wrapper
