from django.http import HttpResponse

def home(request):
    """Homepage view that displays hello world."""
    return HttpResponse("hello world")
