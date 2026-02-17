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
from django.views.generic import RedirectView, TemplateView

from .views.age_range_exit import AgeRangeExitView
from .views.age_when_started_smoking import AgeWhenStartedSmokingView
from .views.asbestos_exposure import AsbestosExposureView
from .views.book_an_appointment import BookAnAppointmentExitView
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
from .views.periods_when_you_stopped_smoking import PeriodsWhenYouStoppedSmokingView
from .views.relatives_age_when_diagnosed import RelativesAgeWhenDiagnosedView
from .views.respiratory_conditions import RespiratoryConditionsView
from .views.responses import ResponsesView
from .views.sex_at_birth import SexAtBirthView
from .views.types_tobacco_smoking import TypesTobaccoSmokingView
from .views.smoking_current import SmokingCurrentView
from .views.smoked_total_years import SmokedTotalYearsView
from .views.smoking_frequency import SmokingFrequencyView
from .views.smoked_amount import SmokedAmountView
from .views.smoking_change import SmokingChangeView
from .views.start import StartView
from .views.weight import WeightView
from .views.confirmation import ConfirmationView

urlpatterns = [
    path('', RedirectView.as_view(url='/start'), name='root'),
    path('age-range-exit', AgeRangeExitView.as_view(), name='age_range_exit'),
    path('age-when-started-smoking', AgeWhenStartedSmokingView.as_view(), name='age_when_started_smoking'),
    path("agree-to-share-information", TemplateView.as_view(template_name="agree_to_share_information.jinja"), name="agree_to_share_information"),
    path('asbestos-exposure', AsbestosExposureView.as_view(), name='asbestos_exposure'),
    path('call-us-to-book-an-appointment', BookAnAppointmentExitView.as_view(), name='book_an_appointment'),
    path('cancer-diagnosis', CancerDiagnosisView.as_view(), name='cancer_diagnosis'),
    path('check-if-you-need-an-appointment', CheckNeedAppointmentView.as_view(), name='check_need_appointment'),
    path('<tobacco_type>-smoking-current', SmokingCurrentView.as_view(), name='smoking_current'),
    path('date-of-birth', DateOfBirthView.as_view(), name='date_of_birth'),
    path('education', EducationView.as_view(), name='education'),
    path('ethnicity', EthnicityView.as_view(), name='ethnicity'),
    path('family-history-lung-cancer', FamilyHistoryLungCancerView.as_view(), name='family_history_lung_cancer'),
    path('gender', GenderView.as_view(), name='gender'),
    path('have-you-ever-smoked', HaveYouEverSmokedView.as_view(), name='have_you_ever_smoked'),
    path('height', HeightView.as_view(), name='height'),
    path('non-smoker-exit', NonSmokerExitView.as_view(), name='non_smoker_exit'),
    path('relatives-age-when-diagnosed', RelativesAgeWhenDiagnosedView.as_view(), name='relatives_age_when_diagnosed'),
    path('respiratory-conditions', RespiratoryConditionsView.as_view(), name='respiratory_conditions'),
    path('periods-when-you-stopped-smoking', PeriodsWhenYouStoppedSmokingView.as_view(), name='periods_when_you_stopped_smoking'),
    path('types-tobacco-smoking', TypesTobaccoSmokingView.as_view(), name='types_tobacco_smoking'),
    path('<tobacco_type>-smoked-total-years', SmokedTotalYearsView.as_view(), name='smoked_total_years'),
    path('<tobacco_type>-smoking-frequency', SmokingFrequencyView.as_view(), name='smoking_frequency'),
    path('<tobacco_type>-smoked-amount', SmokedAmountView.as_view(), name='smoked_amount'),
    path('<tobacco_type>-smoking-change', SmokingChangeView.as_view(), name='smoking_change'),
    path('check-your-answers', ResponsesView.as_view(), name='responses'),
    path('sex-at-birth', SexAtBirthView.as_view(), name='sex_at_birth'),
    path('start', StartView.as_view(), name='start'),
    path('weight', WeightView.as_view(), name='weight'),
    path('confirmation', ConfirmationView.as_view(), name='confirmation'),
]
