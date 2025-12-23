from typing import Optional
from langfuse import get_client

_langfuse_client = None


def get_langfuse_client():
    global _langfuse_client

    if _langfuse_client:
        return _langfuse_client

    _langfuse_client = get_client()
    return _langfuse_client
