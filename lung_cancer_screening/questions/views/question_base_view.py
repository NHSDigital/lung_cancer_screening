from django.urls import reverse
from django.views.generic.edit import UpdateView



class QuestionBaseView(UpdateView):
    page_title = "Check if you need a lung scan – NHS"

    def is_changing_responses(self):
        return self.request.GET.get("change") == "True" or self.request.POST.get("change") == "True"

    def get_change_query_params(self):
        if not self.is_changing_responses():
            return {}

        return {"change": "True"}

    def get_back_link_url(self):
        return self.back_link_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_back_link_url()
        context["page_title"] = self.page_title
        return context

    def get_success_url(self):
        if self.is_changing_responses():
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
