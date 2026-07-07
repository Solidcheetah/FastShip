from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse


class FastShipError(Exception):
    """Base exception for all exceptions in fastship api"""

    status = status.HTTP_400_BAD_REQUEST


class EntityNotFound(FastShipError):
    """Entity not found in database"""

    status = status.HTTP_404_NOT_FOUND


class ClientNotAuthorized(FastShipError):
    """Client is not authorized to perform the action"""

    status = status.HTTP_403_FORBIDDEN


class BadCredentials(FastShipError):
    """User email or password is incorrect"""

    status = status.HTTP_401_UNAUTHORIZED


class InvalidToken(FastShipError):
    """Access token is invalid or expired"""

    status = status.HTTP_401_UNAUTHORIZED


class DeliveryPartnerNotAvailable(FastShipError):
    """Delivery partner/s do not service the destination"""

    status = status.HTTP_422_UNPROCESSABLE_CONTENT


class DeliveryPartnerCapacityExceeded(FastShipError):
    """Delivery partner has reached their max handling capacity"""

    status = status.HTTP_422_UNPROCESSABLE_CONTENT


class EmailNotVerified(FastShipError):
    """User's email has not been verified"""

    status = status.HTTP_403_FORBIDDEN


class NothingToUpdate(FastShipError):
    """No data was provided to perform an update"""

    status = status.HTTP_400_BAD_REQUEST


def _get_handler(code: int, detail: str):
    def handler(request: Request, exception: Exception) -> Response:
        raise HTTPException(
            status_code=code,
            detail=detail,
        )

    return handler


def add_exception_handlers(app: FastAPI):
    for subclass in FastShipError.__subclasses__():
        app.add_exception_handler(
            subclass, _get_handler(subclass.status, subclass.__doc__)
        )

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    def internal_server_error_handler(request, exception):
        return JSONResponse(
            content={"detail": "Something went wrong..."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers={
                "X-ERROR": f"{exception}",
            },
        )
