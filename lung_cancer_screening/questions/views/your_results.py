from django.shortcuts import render
from django.views.decorators.http import require_GET

@require_GET
def your_results(request):
    return render(
        request,
        "your_results.jinja"
    )
