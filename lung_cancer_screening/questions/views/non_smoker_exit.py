from django.shortcuts import render

def non_smoker_exit(request):
    return render(
        request,
        "non_smoker_exit.jinja"
    )
