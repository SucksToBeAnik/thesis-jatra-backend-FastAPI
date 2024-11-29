from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from typing import Any


class CustomException(Exception):
    def __init__(
        self,
        exc: Exception | str,
        message: str | None = None,
        status_code: int = 500,
    ):
        print("Custom Exception---------------", exc)
        self.status_code = status_code
        self.message = message or str(exc)

        self.detail = {
            "type": "Unexpected Error",
            "message": self.message,
        }

        if isinstance(exc, SQLAlchemyError):
            self.status_code = 409
            self.detail = {
                "type": "Database Error",
                "message": str(exc),
            }

        elif isinstance(exc, ValidationError):
            # Handle Pydantic validation errors
            self.status_code = 422
            # Convert validation errors to a dictionary format
            self.detail = {
                "type": "Validation Error",
                "message": [
                    {"detail": err["msg"], "type": err["type"]} for err in exc.errors()
                ],
            }

        elif isinstance(exc, ValueError):
            # Handle ValueError specifically
            self.status_code = 400
            # Convert ValueError to string instead of passing the object
            self.detail = {
                "type": "Value Error",
                "message": str(exc),
            }

        elif isinstance(exc, HTTPException):
            self.status_code = exc.status_code
            self.detail = {
                "type": "HTTP Error",
                "message": str(exc),
            }
