from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .mixins.ensure_response_set import EnsureResponseSet


class QuestionBaseView(LoginRequiredMixin, EnsureResponseSet, View):
    pass

    def _should_redirect_to_responses(self, request):
        return bool(request.POST.get("change"))

    def redirect_to_response_or_next_question(self, request, next_question_url):
        if self._should_redirect_to_responses(request):
            return redirect(reverse("questions:responses"))
        else:
            return redirect(reverse(next_question_url))
