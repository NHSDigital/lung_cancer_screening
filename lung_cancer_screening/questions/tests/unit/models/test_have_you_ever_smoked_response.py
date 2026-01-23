from django.test import TestCase, tag

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory

from ....models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues


@tag("HaveYouEverSmoked")
class TestHaveYouEverSmokedResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = HaveYouEverSmokedResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE
        )

        self.assertEqual(response.response_set, self.response_set)

    def test_has_value_as_enum(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        )

        self.assertEqual(
            response.get_value_display(),
            HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.label
        )

    def test_has_smoked_regularly_returns_truewhen_they_currently_smoke(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE
        )

        self.assertTrue(response.has_smoked_regularly())

    def test_has_smoked_regularly_returns_true_when_they_used_to_smoke_regularly(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        )

        self.assertTrue(response.has_smoked_regularly())

    def test_has_smoked_regularly_returns_false_when_they_have_smoked_a_few_times(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_BUT_ONLY_A_FEW_TIMES
        )

        self.assertFalse(response.has_smoked_regularly())

    def test_has_smoked_regularly_returns_false_when_they_have_never_smoked(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.NO_I_HAVE_NEVER_SMOKED
        )

        self.assertFalse(response.has_smoked_regularly())

    def test_is_eligible_returns_true_when_they_have_smoked_regularly(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        )

        self.assertTrue(response.is_eligible())

    def test_is_eligible_returns_true_when_they_currently_smoke(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE
        )

        self.assertTrue(response.is_eligible())

    def test_is_eligible_returns_false_when_they_have_never_smoked(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.NO_I_HAVE_NEVER_SMOKED
        )

        self.assertFalse(response.is_eligible())

    def test_is_eligible_returns_false_when_they_have_smoked_a_few_times(self):
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=self.response_set,
            value=HaveYouEverSmokedValues.YES_BUT_ONLY_A_FEW_TIMES
        )

        self.assertFalse(response.is_eligible())
