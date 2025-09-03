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
from django.urls import path
from .views.start import start
from .views.date_of_birth import date_of_birth
from .views.responses import responses
from .views.age_range_exit import age_range_exit

urlpatterns = [
    path('start', start, name='start'),
    path('date-of-birth', date_of_birth, name='date_of_birth'),
    path('responses', responses, name='responses'),
    path('age-range-exit', age_range_exit, name='age_range_exit'),
]
