def make_response(
    message: str = None,
    detail: str = None,
    data=None,
    total: int = None,
    skip: int = None,
    limit: int = None,
):
    response = {
        "message": message,
        "detail": detail,
        "data": data,
        "total": total,
        "skip": skip,
        "limit": limit,
    }

    # Filter out key-value pairs where the value is None
    response = {k: v for k, v in response.items() if v is not None}

    return response
