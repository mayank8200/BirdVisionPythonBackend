description = """
This project implements user registration, authentication, and token-based authorization using FastAPI. It securely stores user data, generates JWT tokens for authentication, and handles error scenarios gracefully. Technologies include FastAPI, Pydantic, SQLAlchemy, Passlib, OAuth2 Password Bearer, and JWT. The project structure is organized using APIRouter, and detailed documentation is provided for each endpoint. Overall, it provides a robust, scalable, and efficient solution for user authentication in web applications.
"""

from fastapi import FastAPI
import models
from database import engine
from routers import product, auth

app = FastAPI(
    title="Product Management App",
    description=description,
)
models.Base.metadata.create_all(bind = engine)

app.include_router(product.router)
app.include_router(auth.router)

