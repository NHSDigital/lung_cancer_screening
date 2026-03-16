from django.shortcuts import redirect
from django.urls import reverse


class EnsureEligibleMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.response_set.is_eligible():
            return redirect(reverse("questions:agree_terms_of_use"))

        return super().dispatch(request, *args, **kwargs)
