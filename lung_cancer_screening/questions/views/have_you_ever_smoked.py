from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins.ensure_accepted_terms_of_use import EnsureAcceptedTermsEligible
from .mixins.ensure_response_set import EnsureResponseSet

from .question_base_view import QuestionBaseView

from ..forms.have_you_ever_smoked_form import HaveYouEverSmokedForm
from ..models.have_you_ever_smoked_response import (
    HaveYouEverSmokedResponse
)


class HaveYouEverSmokedView(LoginRequiredMixin, EnsureResponseSet, EnsureAcceptedTermsEligible, QuestionBaseView):
    template_name = "have_you_ever_smoked.jinja"
    form_class = HaveYouEverSmokedForm
    model = HaveYouEverSmokedResponse
    success_url = reverse_lazy("questions:date_of_birth")
    back_link_url = reverse_lazy("questions:agree_terms_of_use")

    def get_success_url(self):
        if self.object.is_eligible():
            return super().get_success_url()
        else:
            return reverse("questions:non_smoker_exit")
