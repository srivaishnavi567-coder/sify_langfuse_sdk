from contextlib import contextmanager
from time import time

from langfuse import get_client, propagate_attributes
from .span import TraceSpan


class LangfuseTracer:
    def __init__(self, service_name, user_id=None, session_id=None):
        self.service_name = service_name
        self.user_id = user_id
        self.session_id = session_id
        self.lf = get_client()

    @contextmanager
    def trace(self, name, metadata=None):
        metadata = metadata or {}
        start = time()

        with self.lf.start_as_current_observation(
            as_type="span",
            name=name,
        ) as root:
           
            root.update(
                metadata={
                    "service": self.service_name,
                    **metadata,
                }
            )

            
            with propagate_attributes(
                user_id=self.user_id,
                session_id=self.session_id,
            ):
                try:
                    yield TraceSpan(root)
                finally:
                    root.update(
                        metadata={
                            "duration_ms": round((time() - start) * 1000, 2)
                        }
                    )
