from django.http import Http404, HttpResponse
from django.test import TestCase, tag
from django.test.client import RequestFactory
from django.views.generic import View

from ....factories.response_set_factory import ResponseSetFactory
from ....factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from .....views.mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin


class FakeView(EnsureSmokingHistoryForTypeMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200)


@tag("mixins")
class EnsureSmokingHistoryForTypeMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.response_set = ResponseSetFactory()
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.request.response_set
        )

    def _dispatch(self, request, tobacco_type):
        view = FakeView()
        view.request = request
        view.kwargs = {"tobacco_type": tobacco_type}
        view.args = ()
        return view, view.dispatch(request, tobacco_type=tobacco_type)

    def test_returns_200_when_tobacco_smoking_history_item_exists(self):
        tobacco_type = self.tobacco_smoking_history.type.lower()
        view, response = self._dispatch(self.request, tobacco_type)

        self.assertEqual(response.status_code, 200)

    def test_tobacco_smoking_history_item_cached_property_returns_item(self):
        tobacco_type = self.tobacco_smoking_history.type.lower()
        view, response = self._dispatch(self.request, tobacco_type)

        self.assertEqual(view.tobacco_smoking_history_item(), self.tobacco_smoking_history)

    def test_raises_404_when_tobacco_smoking_history_item_does_not_exist(self):
        with self.assertRaises(Http404):
            self._dispatch(self.request, tobacco_type="pipe")
