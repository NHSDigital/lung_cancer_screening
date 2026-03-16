from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from .mixins.ensure_response_set import EnsureResponseSet
from .question_base_view import QuestionBaseView
from ..forms.agree_terms_of_use_form import TermsOfUseForm
from ..models.terms_of_use_response import TermsOfUseResponse


class AgreeTermsOfUseView(LoginRequiredMixin, EnsureResponseSet, QuestionBaseView):
    template_name = "agree_terms_of_use.jinja"
    form_class = TermsOfUseForm
    model = TermsOfUseResponse
    success_url = reverse_lazy("questions:have_you_ever_smoked")
    back_link_url = reverse_lazy("questions:start")

    def get_success_url(self):
        if self.object.value:
            return reverse("questions:have_you_ever_smoked")
        else:
            return super().get_success_url()
