from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.have_you_ever_smoked_response_factory import HaveYouEverSmokedResponseFactory

from ....models.have_you_ever_smoked_response import HaveYouEverSmokedResponse, HaveYouEverSmokedValues


class TestHaveYouEverSmokedResponse(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory()

    def test_has_a_valid_factory(self):
        model = HaveYouEverSmokedResponseFactory.build(response_set=self.response_set)
        model.full_clean()


    def test_has_response_set_as_foreign_key(self):
        response_set = ResponseSetFactory()
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=response_set,
            value=HaveYouEverSmokedValues.YES_I_CURRENTLY_SMOKE
        )

        self.assertEqual(response.response_set, response_set)

    def test_has_value_as_enum(self):
        response_set = ResponseSetFactory()
        response = HaveYouEverSmokedResponse.objects.create(
            response_set=response_set,
            value=HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY
        )

        self.assertEqual(
            response.get_value_display(),
            HaveYouEverSmokedValues.YES_I_USED_TO_SMOKE_REGULARLY.label
        )
