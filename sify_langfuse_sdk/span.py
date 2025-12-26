# class TraceSpan:
#     def __init__(self, root_observation):
#         self.root = root_observation

#     def generation(self, model, input, output, usage=None):
#         with self.root.start_as_current_observation(
#             as_type="generation",
#             name="model-generation",
#         ) as gen:
#             gen.update(
#                 model=model,
#                 input=input,
#                 output=output,
#                 metadata={
#                     "usage": usage
#                 },
#             )

#     def event(self, name, metadata):
#         with self.root.start_as_current_observation(
#             as_type="span",
#             name=name,
#         ) as obs:
#             obs.update(metadata=metadata)


# class TraceSpan:
#     def __init__(self, root_span):
#         self.root = root_span

#     def generation(
#         self,
#         model: str,
#         input,
#         output,
#         usage_details: dict | None = None,
#         cost_details: dict | None = None,
#     ):
#         """
#         Creates a Langfuse GENERATION observation.
#         Fully compliant with Langfuse docs:
#         - input
#         - output
#         - usage_details
#         - cost_details
#         """

#         with self.root.start_as_current_observation(
#             as_type="generation",
#             name="model-generation",
#             model=model,
#             input=input,
#         ) as generation:
#             generation.update(
#                 output=output,
#                 usage_details=usage_details,
#                 cost_details=cost_details,
#             )

#     def event(self, name: str, metadata: dict):
#         with self.root.start_as_current_observation(
#             as_type="span",
#             name=name,
#         ) as span:
#             span.update(metadata=metadata)
from langfuse import get_client

class TraceSpan:
    def __init__(self, root_span):
        self.root = root_span
        self.langfuse = get_client()

    def generation(
        self,
        model: str,
        input,
        model_call,              # 👈 function
        usage_details_fn=None,   # optional callable
        cost_details=None,
    ):
        """
        Measures model latency correctly by executing the model
        INSIDE the generation observation.
        """

        with self.root.start_as_current_observation(
            as_type="generation",
            name="model-generation",
            model=model,
            input=input,
        ):
            # 🔥 Model execution is now timed
            output = model_call()

            usage_details = usage_details_fn(output) if usage_details_fn else None

            self.langfuse.update_current_generation(
                output={
                    "role": "assistant",
                    "content": output,
                },
                usage_details=usage_details,
                cost_details=cost_details,
            )

            return output
