from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View


@method_decorator(login_required, name='post')
class StartView(View):
    def get(self, request):
        return render(
            request,
            "start.jinja"
        )

    def post(self, request):
        try:
            request.user.responseset_set.create()

            return redirect(reverse("questions:have_you_ever_smoked"))
        except ValidationError as e:
            return render(
                request,
                "start.jinja",
                {"error_messages": [{ "text": message } for message in e.messages ]},
                status=422
            )
