import os
from starlette.middleware.cors import CORSMiddleware


def add_cors_middleware(app):
    ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN", "http://localhost:5173")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[ALLOW_ORIGIN],
        allow_credentials=True,
        allow_methods=["GET", "HEAD", "OPTIONS", "PUT", "PATCH", "POST", "DELETE"],
        allow_headers=[
            "Origin",
            "Content-Length",
            "Content-Type",
            "Access-Control-Allow-Headers",
            "Authorization",
            "Set-Cookie",
        ],
    )
