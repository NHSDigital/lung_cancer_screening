from django.http import HttpResponse
from django.urls import reverse
from django.test import TestCase, tag
from django.test.client import RequestFactory
from django.views.generic import View

from ....factories.response_set_factory import ResponseSetFactory
from ....factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ....factories.smoking_current_response_factory import SmokingCurrentResponseFactory

from .....views.mixins.ensure_prerequisite_responses import EnsurePrerequisiteResponsesMixin
from .....views.mixins.ensure_smoking_history_for_type import EnsureSmokingHistoryForTypeMixin


class BaseFakeView(EnsureSmokingHistoryForTypeMixin, EnsurePrerequisiteResponsesMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200)

@tag("mixins")
class EnsurePrerequisiteResponsesMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.request.response_set = ResponseSetFactory()
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory(
            response_set=self.request.response_set
        )

    def _dispatch(self, view, request, tobacco_type):
        view.request = request
        view.kwargs = {"tobacco_type": tobacco_type}
        view.args = ()
        return view, view.dispatch(request, tobacco_type=tobacco_type)


    def test_returns_200_by_default(self):
        tobacco_type = self.tobacco_smoking_history.type.lower()
        view, response = self._dispatch(BaseFakeView(), self.request, tobacco_type)

        self.assertEqual(response.status_code, 200)

    def test_returns_200_when_prerequisite_responses_are_present(self):
        class FakeView(BaseFakeView):
            def prerequisite_responses(self):
                return ["smoking_current_response"]

        SmokingCurrentResponseFactory(
            tobacco_smoking_history=self.tobacco_smoking_history
        )

        tobacco_type = self.tobacco_smoking_history.type.lower()
        view, response = self._dispatch(FakeView(), self.request, tobacco_type)

        self.assertEqual(response.status_code, 200)

    def test_redirects_when_the_prerequisite_responses_do_not_exist(self):
        class FakeView(BaseFakeView):
            def prerequisite_responses(self):
                return ["smoking_current_response"]

        tobacco_type = self.tobacco_smoking_history.type.lower()
        view, response = self._dispatch(FakeView(), self.request, tobacco_type)

        self.assertRedirects(response, reverse(
            "questions:smoking_current",
            kwargs={"tobacco_type": tobacco_type}
        ), fetch_redirect_response=False)
