from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import config

_reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="",
    scheme_name="JWT",
)

async def get_token(token: Annotated[str, Depends(_reuseable_oauth)]) -> str:
    """Extracts bearer-token from request header.

    Returns:
        str: extracted token

    Raises:
        HTTPException: if token is invalid 
    """
    if token != config.AUTH_TOKEN:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return token
