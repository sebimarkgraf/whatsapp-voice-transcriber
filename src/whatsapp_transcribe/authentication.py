"""
Authentication module

This module contains functions for API key authentication in FastAPI.
As we are building an API only service without any user login,
we just use a fixed API key
that could be rotated frequently.
"""

import os

from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader


def setup_api_key_auth():
    """
    Setup API key authentication

    Loads the API key from the environment variable API_KEY and
    returns a dependency for API key authentication.
    Allows access to the API only if the API key is correct

    Returns
    -------
        Dependency for API key authentication

    Raises
    ------
        ValueError: If API_KEY environment variable is not set

    """
    # Load API key from environment variable
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    api_key_name = "Authorization"
    api_key_header = APIKeyHeader(name=api_key_name, auto_error=False)

    async def get_api_key(
        api_key_header: str = Depends(api_key_header),
    ):
        if api_key_header == f"Bearer {api_key}":
            return api_key_header
        else:
            raise HTTPException(
                status_code=403,
                detail="Could not validate credentials",
            )

    return get_api_key
