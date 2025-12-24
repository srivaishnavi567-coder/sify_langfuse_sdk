from typing import Any, Dict


class TraceSpan:
    def __init__(self, span):
        self.span = span

    def generation(
        self,
        model: str,
        input: Any,
        output: Any,
        usage: Dict[str, Any] | None = None,
    ):
        with self.span.start_as_current_observation(
            as_type="generation",
            name="model-generation",
            model=model,
            input=input,
            output=output,
            metadata={
                "usage": usage,
            },
        ):
            pass

    def event(self, name: str, metadata: Dict[str, Any]):
        with self.span.start_as_current_observation(
            as_type="span",
            name=name,
            metadata=metadata,
        ):
            pass
