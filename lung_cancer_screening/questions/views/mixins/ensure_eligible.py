from django.shortcuts import redirect
from django.urls import reverse


class EnsureEligibleMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.response_set.is_eligible():
            return redirect(reverse("questions:have_you_ever_smoked"))

        return super().dispatch(request, *args, **kwargs)
