import factory
from datetime import timedelta
from django.utils import timezone

from .user_factory import UserFactory
from ...models.response_set import ResponseSet


def set_submitted_at_recently(response_set, create, extracted):
    response_set.submitted_at = timezone.now() - timedelta(
        days=ResponseSet.RECENTLY_SUBMITTED_PERIOD_DAYS - 1
    )


def set_submitted_at_not_recently(response_set, create, extracted):
    response_set.submitted_at = timezone.now() - timedelta(
        days=ResponseSet.RECENTLY_SUBMITTED_PERIOD_DAYS + 1
    )


class ResponseSetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ResponseSet

    user = factory.SubFactory(UserFactory)

    class Params:
        eligible = factory.Trait(
            have_you_ever_smoked_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory.HaveYouEverSmokedResponseFactory",
                factory_related_name="response_set",
                eligible=True
            ),
            date_of_birth_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.date_of_birth_response_factory.DateOfBirthResponseFactory",
                factory_related_name="response_set",
                eligible=True
            ),
            check_need_appointment_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.check_need_appointment_response_factory.CheckNeedAppointmentResponseFactory",
                factory_related_name="response_set",
                eligible=True
            ),
        )

        complete = factory.Trait(
            asbestos_exposure_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.asbestos_exposure_response_factory.AsbestosExposureResponseFactory",
                factory_related_name="response_set"
            ),
            cancer_diagnosis_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.cancer_diagnosis_response_factory.CancerDiagnosisResponseFactory",
                factory_related_name="response_set"
            ),
            check_need_appointment_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.check_need_appointment_response_factory.CheckNeedAppointmentResponseFactory",
                factory_related_name="response_set"
            ),
            date_of_birth_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.date_of_birth_response_factory.DateOfBirthResponseFactory",
                factory_related_name="response_set"
            ),
            education_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.education_response_factory.EducationResponseFactory",
                factory_related_name="response_set"
            ),
            ethnicity_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.ethnicity_response_factory.EthnicityResponseFactory",
                factory_related_name="response_set"
            ),
            family_history_lung_cancer_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.family_history_lung_cancer_response_factory.FamilyHistoryLungCancerResponseFactory",
                factory_related_name="response_set"
            ),
            gender_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.gender_response_factory.GenderResponseFactory",
                factory_related_name="response_set"
            ),
            have_you_ever_smoked_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.have_you_ever_smoked_response_factory.HaveYouEverSmokedResponseFactory",
                factory_related_name="response_set"
            ),
            height_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.height_response_factory.HeightResponseFactory",
                factory_related_name="response_set"
            ),
            periods_when_you_stopped_smoking_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.periods_when_you_stopped_smoking_response_factory.PeriodsWhenYouStoppedSmokingResponseFactory",
                factory_related_name="response_set"
            ),
            relatives_age_when_diagnosed_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.relatives_age_when_diagnosed_response_factory.RelativesAgeWhenDiagnosedResponseFactory",
                factory_related_name="response_set"
            ),
            respiratory_conditions_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.respiratory_conditions_response_factory.RespiratoryConditionsResponseFactory",
                factory_related_name="response_set"
            ),
            sex_at_birth_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.sex_at_birth_response_factory.SexAtBirthResponseFactory",
                factory_related_name="response_set"
            ),
            weight_response=factory.RelatedFactory(
                "lung_cancer_screening.questions.tests.factories.weight_response_factory.WeightResponseFactory",
                factory_related_name="response_set"
            ),
        )

        not_recently_submitted = factory.Trait(
            complete=True,
            submitted_at=factory.PostGeneration(set_submitted_at_not_recently)
        )

        recently_submitted = factory.Trait(
            complete=True,
            submitted_at=factory.PostGeneration(set_submitted_at_recently)
        )
