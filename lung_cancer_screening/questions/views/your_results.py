from django.shortcuts import render
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def your_results(request):
    return render(
        request,
        "your_results.jinja"
    )
