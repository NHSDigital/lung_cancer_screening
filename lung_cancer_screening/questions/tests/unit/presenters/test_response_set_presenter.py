from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory
from ...factories.date_of_birth_response_factory import DateOfBirthResponseFactory
from ...factories.height_response_factory import HeightResponseFactory
from ...factories.weight_response_factory import WeightResponseFactory
from ...factories.sex_at_birth_response_factory import SexAtBirthResponseFactory
from ...factories.gender_response_factory import GenderResponseFactory
from ...factories.ethnicity_response_factory import EthnicityResponseFactory
from ...factories.asbestos_exposure_response_factory import AsbestosExposureResponseFactory
from ...factories.respiratory_conditions_response_factory import RespiratoryConditionsResponseFactory

from ....models.have_you_ever_smoked_response import HaveYouEverSmokedValues
from ....models.sex_at_birth_response import SexAtBirthValues
from ....models.gender_response import GenderValues
from ....models.ethnicity_response import EthnicityValues
from ....models.respiratory_conditions_response import RespiratoryConditionValues

from ....presenters.response_set_presenter import ResponseSetPresenter

class TestResponseSetPresenter(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()


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
