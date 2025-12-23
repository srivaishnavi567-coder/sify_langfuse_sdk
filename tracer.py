from contextlib import contextmanager
from typing import Any, Dict
from time import time

from langfuse import observe
from .client import get_langfuse_client
from .context import langfuse_context
from .span import TraceSpan


class LangfuseTracer:
    def __init__(
        self,
        service_name: str,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        self.service_name = service_name
        self.user_id = user_id
        self.session_id = session_id
        self.lf = get_langfuse_client()

    @contextmanager
    def trace(self, name: str, metadata: Dict[str, Any] | None = None):
        metadata = metadata or {}
        start = time()

        with observe(
            name=name,
            as_type="span",
            metadata={
                "service": self.service_name,
                **metadata,
            },
        ) as span:
            with langfuse_context(
                user_id=self.user_id,
                session_id=self.session_id,
            ):
                try:
                    # 👇 THIS is where TraceSpan is used
                    yield TraceSpan(span)
                finally:
                    span.update(
                        metadata={
                            "duration_ms": round((time() - start) * 1000, 2)
                        }
                    )

