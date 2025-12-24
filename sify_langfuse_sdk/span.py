class TraceSpan:
    def __init__(self, span):
        self.span = span

    def generation(self, model, input, output, usage=None):
        with self.span.start_as_current_observation(
            as_type="generation",
            name="model-generation",
        ) as gen:
            gen.update(
                model=model,
                input=input,
                output=output,
                metadata={"usage": usage},
            )

    def event(self, name, metadata):
        with self.span.start_as_current_observation(
            as_type="span",
            name=name,
        ) as obs:
            obs.update(metadata=metadata)

