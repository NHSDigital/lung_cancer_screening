from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

from .mixins.ensure_response_set import EnsureResponseSet


class QuestionBaseView(LoginRequiredMixin, EnsureResponseSet, UpdateView):

    def should_redirect_to_responses(self, request):
        return bool(request.POST.get("change"))

    def redirect_to_response_or_next_question(self, request, next_question_url, query=None):
        if self.should_redirect_to_responses(request):
            return redirect(reverse("questions:responses", query=query))
        else:
            return redirect(reverse(next_question_url))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.back_link_url
        return context

    def get_success_url(self):
        if self.should_redirect_to_responses(self.request):
            return reverse("questions:responses")
        else:
            return super().get_success_url()

    def get_object(self):
        return self.model.objects.get_or_build(
            response_set=self.request.response_set
        )[0]

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form),
            status=422
        )
