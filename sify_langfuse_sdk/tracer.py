from contextlib import contextmanager
from time import time
from langfuse import observe
from .context import langfuse_context
from .span import TraceSpan


class LangfuseTracer:
    def __init__(self, service_name, user_id=None, session_id=None):
        self.service_name = service_name
        self.user_id = user_id
        self.session_id = session_id

    @contextmanager
    def trace(self, name, metadata=None):
        metadata = metadata or {}
        start = time()

        with observe(name=name) as span:
            span.update(
                metadata={
                    "service": self.service_name,
                    **metadata,
                }
            )

            with langfuse_context(
                user_id=self.user_id,
                session_id=self.session_id,
            ):
                try:
                    yield TraceSpan(span)
                finally:
                    span.update(
                        metadata={
                            "duration_ms": round((time() - start) * 1000, 2)
                        }
                    )


