from django.shortcuts import redirect
from django.urls import reverse


class EnsurePrerequisiteResponsesMixin:
    RESPONSE_URL_MAPPING = {
        "age_when_started_smoking_response": "questions:age_when_started_smoking",
    }

    prerequisite_responses = []

    def dispatch(self, request, *args, **kwargs):
        for prerequisite_response in self.prerequisite_responses:
            if not hasattr(self.request.response_set, prerequisite_response):
                return redirect(self.get_redirect_url(prerequisite_response))

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, prerequisite_response):
        return reverse(
            self.RESPONSE_URL_MAPPING[prerequisite_response],
            query=self.change_query_params()
        )

    def change_query_params(self):
        if not bool(self.request.GET.get("change")):
            return {}

        return {"change": "True"}
