from fastapi import FastAPI

from .auth.routes import router as auth_router
from .session.routes import router as session_router
from .chat.routes import router as chat_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(session_router)
    app.include_router(chat_router)