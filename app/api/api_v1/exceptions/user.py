from typing import Any

from fastapi import HTTPException, status

from app.api.api_v1.exceptions import details


class GetUserIdError(HTTPException):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["status_code"] = status.HTTP_404_NOT_FOUND
        kwargs["detail"] = details.GET_USER_ID_ERROR

        super().__init__(*args, **kwargs)


class CreateUniqueUsernameError(HTTPException):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["status_code"] = status.HTTP_409_CONFLICT
        kwargs["detail"] = details.CREATE_UNIQUE_USERNAME_ERROR

        super().__init__(*args, **kwargs)


class CreateUniqueEmailError(HTTPException):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["status_code"] = status.HTTP_409_CONFLICT
        kwargs["detail"] = details.CREATE_UNIQUE_EMAIL_ERROR

        super().__init__(*args, **kwargs)


class GetUsernameError(HTTPException):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["status_code"] = status.HTTP_404_NOT_FOUND
        kwargs["detail"] = details.GET_USERNAME_ERROR

        super().__init__(*args, **kwargs)
