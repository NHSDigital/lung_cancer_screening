import humps

from django.test import TestCase, tag
from django.urls import reverse

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
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory

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


    def test_have_you_ever_smoked_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.have_you_ever_smoked, None)


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

    def test_periods_when_you_stopped_smoking_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.periods_when_you_stopped_smoking, None)


    def test_periods_when_you_stopped_smoking_with_value(self):
        # Create required dependencies
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


    def test_what_is_your_date_of_birth_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.date_of_birth, None)


    def test_what_is_your_date_of_birth_with_value(self):
        DateOfBirthResponseFactory(
            response_set=self.response_set,
            value="1990-01-01"
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.date_of_birth, "1 January 1990")

    def test_what_is_your_height_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.height, None)


    def test_what_is_your_height_with_metric_value(self):
        HeightResponseFactory(
            response_set=self.response_set,
            metric=1800
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.height, "180 cm")


    def test_what_is_your_height_with_imperial_value(self):
        HeightResponseFactory(
            response_set=self.response_set,
            imperial=71
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.height, "5 feet 11 inches")


    def test_what_is_your_weight_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.weight, None)


    def test_what_is_your_weight_with_value(self):
        WeightResponseFactory(
            response_set=self.response_set,
            metric=700
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.weight, "70 kg")


    def test_what_is_your_weight_with_imperial_value(self):
        WeightResponseFactory(
            response_set=self.response_set,
            imperial=156
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.weight, "11 stone 2 pounds")

    def test_sex_at_birth_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.sex_at_birth, None)

    def test_sex_at_birth_with_value(self):
        SexAtBirthResponseFactory(
            response_set=self.response_set,
            value=SexAtBirthValues.MALE
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.sex_at_birth, SexAtBirthValues.MALE.label)


    def test_gender_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.gender, None)


    def test_gender_with_value(self):
        GenderResponseFactory(
            response_set=self.response_set,
            value=GenderValues.MALE
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.gender, GenderValues.MALE.label)


    def test_ethnicity_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.ethnicity, None)


    def test_ethnicity_with_value(self):
        EthnicityResponseFactory(
            response_set=self.response_set,
            value=EthnicityValues.WHITE
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.ethnicity, EthnicityValues.WHITE.label)

    def test_education_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.education, None)

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


    def test_asbestos_exposure_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.asbestos_exposure, None)

    def test_asbestos_exposure_with_value(self):
        AsbestosExposureResponseFactory(
            response_set=self.response_set,
            value=True
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.asbestos_exposure, "Yes")


    def test_respiratory_conditions_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.respiratory_conditions, None)


    def test_respiratory_conditions_with_value(self):
        RespiratoryConditionsResponseFactory(
            response_set=self.response_set,
            value=[RespiratoryConditionValues.COPD, RespiratoryConditionValues.BRONCHITIS]
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.respiratory_conditions, RespiratoryConditionValues.COPD.label + " and " + RespiratoryConditionValues.BRONCHITIS.label)

    def test_cancer_diagnosis_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.cancer_diagnosis, None)


    def test_cancer_diagnosis_with_value(self):
        CancerDiagnosisResponseFactory(
            response_set=self.response_set,
            value=True
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.cancer_diagnosis, "Yes")

    def test_family_history_lung_cancer_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.family_history_lung_cancer, None)

    def test_family_history_lung_cancer_with_value(self):
        FamilyHistoryLungCancerResponseFactory(
            response_set=self.response_set,
            value=FamilyHistoryLungCancerValues.YES
        )

        presenter = ResponseSetPresenter(self.response_set)

        self.assertEqual(presenter.family_history_lung_cancer, FamilyHistoryLungCancerValues.YES.label)

    def test_relative_age_when_diagnosed_with_no_value(self):
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.relatives_age_when_diagnosed, None)


    def test_relative_age_when_diagnosed_with_value(self):
        RelativesAgeWhenDiagnosedResponseFactory(
            response_set=self.response_set,
            value=RelativesAgeWhenDiagnosedValues.YES
        )
        presenter = ResponseSetPresenter(self.response_set)
        self.assertEqual(presenter.relatives_age_when_diagnosed, RelativesAgeWhenDiagnosedValues.YES.label)

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


    def test_smoking_history_types_responses_items_sets_the_correct_key(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            type=TobaccoSmokingHistoryTypes.CIGARETTES
        )

        presenter = ResponseSetPresenter(self.response_set)

        response_items = presenter.smoking_history_types_responses_items()
        cigarettes_response_item = response_items[0]

        self.assertEqual(
            cigarettes_response_item.get("key").get("text"),
            "Total number of years you have smoked cigarettes"
        )


    def test_smoking_history_types_responses_items_sets_the_correct_value(self):
        cigarettes = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set, type=TobaccoSmokingHistoryTypes.CIGARETTES
        )
        smoked_total_years_response = SmokedTotalYearsResponseFactory.create(
            tobacco_smoking_history=cigarettes,
        )

        presenter = ResponseSetPresenter(self.response_set)

        response_items = presenter.smoking_history_types_responses_items()
        cigarettes_response_item = response_items[0]

        self.assertEqual(
            cigarettes_response_item.get("value").get("text"),
            smoked_total_years_response.value,
        )


    def test_smoking_history_types_responses_items_sets_the_correct_change_link(self):
        TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set, type=TobaccoSmokingHistoryTypes.CIGARETTES
        )

        presenter = ResponseSetPresenter(self.response_set)

        response_items = presenter.smoking_history_types_responses_items()
        cigarettes_response_item = response_items[0]

        self.assertEqual(
            cigarettes_response_item.get("actions").get("items")[0].get("href"),
            reverse(
                "questions:smoked_total_years",
                kwargs={
                    "tobacco_type": humps.kebabize(
                        TobaccoSmokingHistoryTypes.CIGARETTES
                    )
                },
                query={"change": "True"},
            ),
        )
