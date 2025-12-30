
# from langfuse import get_client

# class TraceSpan:
#     def __init__(self, root_span):
#         self.root = root_span
#         self.langfuse = get_client()

#     def generation(
#         self,
#         model: str,
#         input,
#         model_call,              # 👈 function
#         usage_details_fn=None,   # optional callable
#         cost_details=None,
#     ):
#         """
#         Measures model latency correctly by executing the model
#         INSIDE the generation observation.
#         """

#         with self.root.start_as_current_observation(
#             as_type="generation",
#             name="model-generation",
#             model=model,
#             input=input,
#         ):
#             # 🔥 Model execution is now timed
#             output = model_call()

#             usage_details = usage_details_fn(output) if usage_details_fn else None

#             self.langfuse.update_current_generation(
#                 output={
#                     "role": "assistant",
#                     "content": output,
#                 },
#                 usage_details=usage_details,
#                 cost_details=cost_details,
#             )

#             return output

from .client import get_langfuse_client


class TraceSpan:
    def __init__(self, root_span):
        self.root = root_span
        self.langfuse = get_langfuse_client()

    def generation(
        self,
        model: str,
        input,
        model_call,
        usage_details_fn=None,
        cost_details=None,
    ):
        if not self.root or not self.langfuse:
            # 🚫 Langfuse disabled → just run model
            return model_call()

        with self.root.start_as_current_observation(
            as_type="generation",
            name="model-generation",
            model=model,
            input=input,
        ):
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
