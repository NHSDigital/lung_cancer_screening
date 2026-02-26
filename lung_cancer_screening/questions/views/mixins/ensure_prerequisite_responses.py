from django.shortcuts import redirect
from django.urls import reverse

class EnsurePrerequisiteResponsesMixin:
    RESPONSE_URL_MAPPING = {
        "smoking_current_response": "questions:smoking_current",
        "smoked_total_years_response": "questions:smoked_total_years",
        "smoking_frequency_response": "questions:smoking_frequency",
        "smoked_amount_response": "questions:smoked_amount",
    }

    def dispatch(self, request, *args, **kwargs):
        for prerequisite_response in self.prerequisite_responses():
            if not hasattr(self.get_smoking_history_item(), prerequisite_response):
                return redirect(self.get_redirect_url(prerequisite_response))

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, prerequisite_response):
        return reverse(
            self.RESPONSE_URL_MAPPING[prerequisite_response],
            kwargs=self.kwargs,
            query=self.get_change_query_params()
        )
