from django.urls import reverse, reverse_lazy

from .question_base_view import QuestionBaseView
from ..forms.have_you_ever_smoked_form import HaveYouEverSmokedForm
from ..models.have_you_ever_smoked_response import (
    HaveYouEverSmokedResponse
)


class HaveYouEverSmokedView(QuestionBaseView):
    template_name = "have_you_ever_smoked.jinja"
    form_class = HaveYouEverSmokedForm
    model = HaveYouEverSmokedResponse
    success_url = reverse_lazy("questions:date_of_birth")
    back_link_url = reverse_lazy("questions:start")

    def get_success_url(self):
        if self.object.has_smoked_regularly():
            return super().get_success_url()
        else:
            return reverse("questions:non_smoker_exit")
