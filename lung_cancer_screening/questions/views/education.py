from django.shortcuts import render, redirect
from django.urls import reverse

from .authenticated_view import AuthenticatedView

class EducationView(AuthenticatedView):
    def get(self, request):
        return render_template(request)

    def post(self, request):
        return redirect(reverse("questions:respiratory_conditions"))

def render_template(request, status=200):
    return render(
        request,
        "question_form.jinja",
        {
            "back_link_url": reverse("questions:ethnicity")
        },
        status=status
    )
