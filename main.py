from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from config import db
from sqlmodel import SQLModel

from utils.exceptions import CustomException

# Import Models for engine to create tables
from models.profiles import Profile
from models.groups import ThesisGroup
from models.users import User

# Import Routes
from routes.auth import router as auth_router
from routes.profiles import router as profiles_router
from routes.groups import router as groups_router

routers = [
    auth_router,
    profiles_router,
    groups_router,
]


def initialize_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Starting up...")
        SQLModel.metadata.create_all(db.engine)
        yield
        print("Shutting down...")

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    [app.include_router(router) for router in routers]

    # Add exception handlers
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return app


app = initialize_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
