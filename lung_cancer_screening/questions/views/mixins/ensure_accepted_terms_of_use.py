from django.shortcuts import redirect
from django.urls import reverse


class EnsureAcceptedTermsEligible:
    def dispatch(self, request, *args, **kwargs):
        if (
            not hasattr(request.response_set, "terms_of_use_response")
            or not request.response_set.terms_of_use_response.has_accepted()
        ):
            return redirect(reverse("questions:agree_terms_of_use"))
        else:
            return super().dispatch(request, *args, **kwargs)
