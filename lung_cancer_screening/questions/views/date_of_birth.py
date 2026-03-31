from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from lung_cancer_screening.questions.views.mixins.ensure_accepted_terms_of_use import EnsureAcceptedTermsEligible

from .mixins.ensure_response_set import EnsureResponseSet
from .question_base_view import QuestionBaseView
from ..forms.date_of_birth_form import DateOfBirthForm
from ..models.date_of_birth_response import DateOfBirthResponse

class EnsureSmokedEligible:
    def dispatch(self, request, *args, **kwargs):
        if (
            not hasattr(request.response_set, "have_you_ever_smoked_response")
            or not request.response_set.have_you_ever_smoked_response.is_eligible()
        ):
            return redirect(reverse("questions:have_you_ever_smoked"))
        else:
            return super().dispatch(request, *args, **kwargs)


class DateOfBirthView(LoginRequiredMixin, EnsureResponseSet, EnsureAcceptedTermsEligible, EnsureSmokedEligible, QuestionBaseView):
    template_name = "question_form.jinja"
    form_class = DateOfBirthForm
    model = DateOfBirthResponse
    success_url = reverse_lazy("questions:check_need_appointment")
    back_link_url = reverse_lazy("questions:have_you_ever_smoked")
    page_title: str = "What is your date of birth? – Check if you need a lung scan – NHS"

    def get_success_url(self):
        if self.object.is_eligible():
            return super().get_success_url()
        else:
            return reverse("questions:age_range_exit")

