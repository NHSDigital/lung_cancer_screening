from django.http import HttpResponse
from django.urls import reverse
from django.test import TestCase, tag
from django.test.client import RequestFactory
from django.views.generic import View

from ....factories.response_set_factory import ResponseSetFactory
from ....factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory

from .....views.mixins.ensure_prerequisite_responses import EnsurePrerequisiteResponsesMixin


class BaseFakeView(
    EnsurePrerequisiteResponsesMixin,
    View
):
    def get(self, request, *args, **kwargs):
        return HttpResponse(status=200)

@tag("mixins")
class EnsureSmokingHistoryPrerequisiteResponsesMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.response_set = ResponseSetFactory()
        self.request = self.factory.get("/")
        self.request.response_set = self.response_set


    def _dispatch(self, view, request, query={}):
        view.request = request
        view.args = ()
        return view, view.dispatch(request, **query)


    def test_returns_200_by_default(self):
        view, response = self._dispatch(BaseFakeView(), self.request)

        self.assertEqual(response.status_code, 200)


    def test_returns_200_when_prerequisite_responses_are_present(self):
        class FakeView(BaseFakeView):
            prerequisite_responses = ["age_when_started_smoking_response"]

        AgeWhenStartedSmokingResponseFactory(
            response_set=self.request.response_set
        )

        view, response = self._dispatch(FakeView(), self.request)

        self.assertEqual(response.status_code, 200)


    def test_redirects_when_the_prerequisite_responses_do_not_exist(self):
        class FakeView(BaseFakeView):
            prerequisite_responses = ["age_when_started_smoking_response"]

        view, response = self._dispatch(FakeView(), self.request)

        self.assertRedirects(response, reverse(
            "questions:age_when_started_smoking",
        ), fetch_redirect_response=False)


    def test_redirects_when_the_prerequisite_responses_do_not_exist_when_changing_responses(self):
        class FakeView(BaseFakeView):
            prerequisite_responses = ["age_when_started_smoking_response"]

        request = self.factory.get("/", {"change": "True"})
        request.response_set = self.response_set
        view, response = self._dispatch(FakeView(), request)

        self.assertRedirects(response, reverse(
            "questions:age_when_started_smoking",
            query={"change": "True"},
        ), fetch_redirect_response=False)

