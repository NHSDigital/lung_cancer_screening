from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.height_response_factory import HeightResponseFactory
from ...factories.weight_response_factory import WeightResponseFactory
from ...factories.sex_at_birth_response_factory import SexAtBirthResponseFactory
from ...factories.gender_response_factory import GenderResponseFactory
from ...factories.ethnicity_response_factory import EthnicityResponseFactory
from ...factories.education_response_factory import EducationResponseFactory
from ...factories.asbestos_exposure_response_factory import AsbestosExposureResponseFactory
from ...factories.respiratory_conditions_response_factory import RespiratoryConditionsResponseFactory
from ...factories.cancer_diagnosis_response_factory import CancerDiagnosisResponseFactory
from ...factories.family_history_lung_cancer_response_factory import FamilyHistoryLungCancerResponseFactory
from ...factories.relatives_age_when_diagnosed_response_factory import RelativesAgeWhenDiagnosedResponseFactory
from ...factories.periods_when_you_stopped_smoking_response_factory import PeriodsWhenYouStoppedSmokingResponseFactory
from ...factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory

from ....presenters.tobacco_smoking_history_type_presenter import TobaccoSmokingHistoryTypePresenter

from ....models.have_you_ever_smoked_response import HaveYouEverSmokedValues
from ....models.sex_at_birth_response import SexAtBirthValues
from ....models.gender_response import GenderValues
from ....models.ethnicity_response import EthnicityValues
from ....models.education_response import EducationValues
from ....models.family_history_lung_cancer_response import FamilyHistoryLungCancerValues
from ....models.relatives_age_when_diagnosed_response import RelativesAgeWhenDiagnosedValues
from ....models.tobacco_smoking_history import TobaccoSmokingHistoryTypes

from ....models.respiratory_conditions_response import RespiratoryConditionValues

from ....presenters.response_set_presenter import ResponseSetPresenter


class TestResponseSetPresenter(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create()

    @tag("HaveYouEverSmoked")
    def test_have_you_ever_smoked_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.have_you_ever_smoked,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("HaveYouEverSmoked")
    def test_have_you_ever_smoked_with_yes_value(self):
        HaveYouEverSmokedResponseFactory(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        )
        presenter = ResponseSetPresenter(self.response_set)

        self.assertEqual(
            presenter.have_you_ever_smoked,
            HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.label
        )

    @tag("PeriodsWhenYouStoppedSmoking")
    def test_periods_when_you_stopped_smoking_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.periods_when_you_stopped_smoking,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("PeriodsWhenYouStoppedSmoking")
    def test_periods_when_you_stopped_smoking_with_value(self):
        DateOfBirthResponseFactory(response_set=self.response_set)
        age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory(response_set=self.response_set)

        periods_when_you_stopped_smoking_response = PeriodsWhenYouStoppedSmokingResponseFactory(
            response_set=self.response_set,
            value=True,
            duration_years=age_when_started_smoking_response.years_smoked_including_stopped() - 1
        )
        presenter = ResponseSetPresenter(self.response_set)

        self.assertEqual(
            presenter.periods_when_you_stopped_smoking,
            f"Yes ({periods_when_you_stopped_smoking_response.duration_years} years)",
        )

    @tag("DateOfBirth")
    def test_what_is_your_date_of_birth_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.date_of_birth,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("DateOfBirth")
    def test_what_is_your_date_of_birth_with_value(self):
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            value="1990-01-01"
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.date_of_birth, "1 January 1990")


    @tag("Height")
    def test_what_is_your_height_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.height,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("Height")
    def test_what_is_your_height_with_metric_value(self):
        HeightResponseFactory(
            response_set=self.response_set,
            metric=1800
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.height, "180 cm")


    @tag("Height")
    def test_what_is_your_height_with_imperial_value(self):
        HeightResponseFactory(
            response_set=self.response_set,
            imperial=71
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.height, "5 feet 11 inches")


    @tag("Weight")
    def test_what_is_your_weight_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.weight,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )

    @tag("Weight")
    def test_what_is_your_weight_with_value(self):
        WeightResponseFactory(
            response_set=self.response_set,
            metric=700
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.weight, "70 kg")


    @tag("Weight")
    def test_what_is_your_weight_with_imperial_value(self):
        WeightResponseFactory(
            response_set=self.response_set,
            imperial=156
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.weight, "11 stone 2 pounds")


    @tag("SexAtBirth")
    def test_sex_at_birth_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.sex_at_birth,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("SexAtBirth")
    def test_sex_at_birth_with_value(self):
        SexAtBirthResponseFactory(
            response_set=self.response_set,
            value=SexAtBirthValues.MALE
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.sex_at_birth, SexAtBirthValues.MALE.label)


    @tag("Gender")
    def test_gender_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.gender,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("Gender")
    def test_gender_with_value(self):
        GenderResponseFactory(
            response_set=self.response_set,
            value=GenderValues.MALE
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.gender, GenderValues.MALE.label)


    @tag("Ethnicity")
    def test_ethnicity_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.ethnicity,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("Ethnicity")
    def test_ethnicity_with_value(self):
        EthnicityResponseFactory(
            response_set=self.response_set,
            value=EthnicityValues.WHITE
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.ethnicity, EthnicityValues.WHITE.label)


    @tag("Education")
    def test_education_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.education,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("Education")
    def test_education_with_value(self):
        EducationResponseFactory(
            response_set=self.response_set,
            value=[
                EducationValues.GCSES,
                EducationValues.A_LEVELS,
            ],
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.education,
            EducationValues.GCSES.label
            + " and "
            + EducationValues.A_LEVELS.label,
        )


    @tag("AsbestosExposure")
    def test_asbestos_exposure_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.asbestos_exposure,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("AsbestosExposure")
    def test_asbestos_exposure_with_value(self):
        AsbestosExposureResponseFactory(
            response_set=self.response_set,
            value=True
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.asbestos_exposure, "Yes")


    @tag("RespiratoryConditions")
    def test_respiratory_conditions_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.respiratory_conditions,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("RespiratoryConditions")
    def test_respiratory_conditions_with_value(self):
        RespiratoryConditionsResponseFactory(
            response_set=self.response_set,
            value=[RespiratoryConditionValues.COPD, RespiratoryConditionValues.BRONCHITIS]
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.respiratory_conditions, RespiratoryConditionValues.COPD.label + " and " + RespiratoryConditionValues.BRONCHITIS.label)


    @tag("CancerDiagnosis")
    def test_cancer_diagnosis_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.cancer_diagnosis,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("CancerDiagnosis")
    def test_cancer_diagnosis_with_value(self):
        CancerDiagnosisResponseFactory(
            response_set=self.response_set,
            value=True
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.cancer_diagnosis, "Yes")


    @tag("FamilyHistoryLungCancer")
    def test_family_history_lung_cancer_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.family_history_lung_cancer,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("FamilyHistoryLungCancer")
    def test_family_history_lung_cancer_with_value(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.YES
        )

        presenter = ResponseSetPresenter(self.response_set)

        self.assertEqual(presenter.family_history_lung_cancer, FamilyHistoryLungCancerValues.YES.label)


    @tag("RelativesAgeWhenDiagnosed")
    def test_relative_age_when_diagnosed_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.relatives_age_when_diagnosed,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("RelativesAgeWhenDiagnosed")
    def test_relative_age_when_diagnosed_with_value(self):
        RelativesAgeWhenDiagnosedResponseFactory(
            response_set=self.response_set,
            value=RelativesAgeWhenDiagnosedValues.YES
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.relatives_age_when_diagnosed, RelativesAgeWhenDiagnosedValues.YES.label)


    @tag("FamilyHistoryLungCancer")
    @tag("RelativesAgeWhenDiagnosed")
    def test_family_history_responses_when_no_family_history_response_set(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertNotIn(
            "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?",
            [
                item.get("key").get("text")
                for item in presenter.family_history_responses_items()
            ],
        )


    @tag("FamilyHistoryLungCancer")
    @tag("RelativesAgeWhenDiagnosed")
    def test_family_history_responses_when_no_family_history(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.NO
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertNotIn(
            "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?",
            [
                item.get("key").get("text")
                for item in presenter.family_history_responses_items()
            ],
        )


    @tag("FamilyHistoryLungCancer")
    @tag("RelativesAgeWhenDiagnosed")
    def test_family_history_responses_when_family_history(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.YES
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertIn(
            "Were any of your relatives younger than 60 years old when they were diagnosed with lung cancer?",
            [
                item.get("key").get("text")
                for item in presenter.family_history_responses_items()
            ],
        )


    @tag("AgeWhenStartedSmoking")
    def test_age_when_started_smoking_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.age_when_started_smoking,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("AgeWhenStartedSmoking")
    def test_age_when_started_smoking_with_value(self):
        AgeWhenStartedSmokingResponseFactory(
            response_set=self.response_set,
            value=10
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.age_when_started_smoking, "10")


    @tag("TypesTobaccoSmoking")
    def test_types_tobacco_smoking_with_no_response(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(
            presenter.types_tobacco_smoking,
            ResponseSetPresenter.NOT_ANSWERED_TEXT
        )


    @tag("TypesTobaccoSmoking")
    def test_types_tobacco_smoking(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.SHISHA
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARS
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.types_tobacco_smoking, "Cigarettes, Cigars, and Shisha")


    @tag("TobaccoSmokingHistory")
    def test_tobacco_smoking_history_by_type_returns_presenter_grouped_by_type(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
            normal=True,
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigars=True,
            normal=True,
        )
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigars=True,
            increased=True,
        )

        result = ResponseSetPresenter(self.response_set).tobacco_smoking_history_by_type()

        self.assertEqual(type(result[0]), TobaccoSmokingHistoryTypePresenter)
        self.assertEqual(type(result[1]), TobaccoSmokingHistoryTypePresenter)
