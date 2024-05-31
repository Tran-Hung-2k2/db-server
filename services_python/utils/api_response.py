def make_response(
    message: str = None,
    detail: str = None,
    data=None,
    other: dict = None,
):
    if other:
        return {
            "message": message,
            "detail": detail,
            "data": data,
            "total": other["total"],
            "skip": other["skip"],
            "limit": other["limit"],
        }
    else:
        return {
            "message": message,
            "detail": detail,
            "data": data,
        }
