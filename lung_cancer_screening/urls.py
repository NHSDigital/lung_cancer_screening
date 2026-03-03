"""
URL configuration for lung_cancer_screening project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.auth.decorators import login_not_required
from django.http import HttpResponse
from django.urls import path, include
from django.views.decorators.http import require_GET

from lung_cancer_screening.core.decorators import basic_auth_exempt

@require_GET
@basic_auth_exempt
@login_not_required
def sha_view(request):
    return HttpResponse(settings.COMMIT_SHA)


@require_GET
@basic_auth_exempt
@login_not_required
def health_check(request):
    return HttpResponse("OK")


urlpatterns = [
    path('', include(
        ("lung_cancer_screening.questions.urls", "questions"),
        namespace="questions")),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path(
        "healthcheck",
        health_check,
    ),
    path(
        "sha",
        sha_view,
    ),
]
