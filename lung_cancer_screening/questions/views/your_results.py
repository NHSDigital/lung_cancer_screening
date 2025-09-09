from django.shortcuts import render



def your_results(request):
    return render(
        request,
        "your_results.jinja"
    )
