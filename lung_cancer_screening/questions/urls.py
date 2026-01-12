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
from django.views.generic import RedirectView

from .views.age_range_exit import AgeRangeExitView
from .views.asbestos_exposure import AsbestosExposureView
from .views.bmi_exit import BmiExitView
from .views.cancer_diagnosis import CancerDiagnosisView
from .views.check_need_appointment import CheckNeedAppointmentView
from .views.date_of_birth import DateOfBirthView
from .views.education import EducationView
from .views.ethnicity import EthnicityView
from .views.family_history_lung_cancer import FamilyHistoryLungCancerView
from .views.gender import GenderView
from .views.have_you_ever_smoked import HaveYouEverSmokedView
from .views.height import HeightView
from .views.non_smoker_exit import NonSmokerExitView
from .views.relatives_age_when_diagnosed import RelativesAgeWhenDiagnosedView
from .views.respiratory_conditions import RespiratoryConditionsView
from .views.responses import ResponsesView
from .views.sex_at_birth import SexAtBirthView
from .views.start import StartView
from .views.weight import WeightView
from .views.your_results import YourResultsView

urlpatterns = [
    path('', RedirectView.as_view(url='/start'), name='root'),
    path('start', StartView.as_view(), name='start'),
    path('have-you-ever-smoked', HaveYouEverSmokedView.as_view(), name='have_you_ever_smoked'),
    path('date-of-birth', DateOfBirthView.as_view(), name='date_of_birth'),
    path('check-if-you-need-an-appointment', CheckNeedAppointmentView.as_view(), name='check_need_appointment'),
    path('height', HeightView.as_view(), name='height'),
    path('weight', WeightView.as_view(), name='weight'),
    path('sex-at-birth', SexAtBirthView.as_view(), name='sex_at_birth'),
    path('gender', GenderView.as_view(), name='gender'),
    path('ethnicity', EthnicityView.as_view(), name='ethnicity'),
    path('education', EducationView.as_view(), name='education'),
    path('respiratory-conditions', RespiratoryConditionsView.as_view(), name='respiratory_conditions'),
    path('asbestos-exposure', AsbestosExposureView.as_view(), name='asbestos_exposure'),
    path('cancer-diagnosis', CancerDiagnosisView.as_view(), name='cancer_diagnosis'),
    path('family-history-lung-cancer', FamilyHistoryLungCancerView.as_view(), name='family_history_lung_cancer'),
    path('relatives-age-when-diagnosed', RelativesAgeWhenDiagnosedView.as_view(), name='relatives_age_when_diagnosed'),
    path('responses', ResponsesView.as_view(), name='responses'),
    path('age-range-exit', AgeRangeExitView.as_view(), name='age_range_exit'),
    path('bmi-exit', BmiExitView.as_view(), name='bmi_exit'),
    path('non-smoker-exit', NonSmokerExitView.as_view(), name='non_smoker_exit'),
    path('your-results', YourResultsView.as_view(), name='your_results'),
]
