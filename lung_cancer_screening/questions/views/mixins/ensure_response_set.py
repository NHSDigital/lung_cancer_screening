from django.shortcuts import redirect
from django.urls import reverse

from lung_cancer_screening.questions.models.response_set import ResponseSet

class EnsureResponseSet:

    def dispatch(self, request, *args, **kwargs):
        if request.user and request.user.responseset_set.submitted_in_last_year().count() > 0:
            return redirect(reverse("questions:start"))
        else:
            if request.method == "POST":
                request.response_set = self._get_or_create_response_set(request.user)
            elif request.method == "GET":
                request.response_set = self._get_or_build_response_set(request.user)

            return super().dispatch(request, *args, **kwargs)


    def _get_or_create_response_set(self, current_user):
        if current_user.responseset_set.unsubmitted().count() == 0:
            return current_user.responseset_set.create()
        else:
            return current_user.responseset_set.unsubmitted().last()

    def _get_or_build_response_set(self, current_user):
        if current_user.responseset_set.unsubmitted().count() == 0:
            return ResponseSet(user=current_user)
        else:
            return current_user.responseset_set.unsubmitted().last()
