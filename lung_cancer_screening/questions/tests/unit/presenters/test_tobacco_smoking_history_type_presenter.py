from django.test import TestCase

from ...factories.response_set_factory import ResponseSetFactory
from ...factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from ...factories.smoking_frequency_response_factory import SmokingFrequencyResponseFactory
from ...factories.smoked_amount_response_factory import SmokedAmountResponseFactory
from ...factories.smoked_total_years_response_factory import SmokedTotalYearsResponseFactory
from ....models.smoking_frequency_response import SmokingFrequencyValues

from ....presenters.tobacco_smoking_history_type_presenter import TobaccoSmokingHistoryTypePresenter

class TestTobaccoSmokingHistoryTypePresenter(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create(complete=True)
        self.normal_tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
            normal=True,
            complete=True,
        )
        self.normal_tobacco_smoking_history.smoked_total_years_response.value = 10
        self.normal_tobacco_smoking_history.smoked_total_years_response.save()
        self.normal_tobacco_smoking_history.smoked_amount_response.value = 7
        self.normal_tobacco_smoking_history.smoked_amount_response.save()
        self.normal_tobacco_smoking_history.smoking_frequency_response.value = SmokingFrequencyValues.WEEKLY
        self.normal_tobacco_smoking_history.smoking_frequency_response.save()
        self.normal_tobacco_smoking_history.smoking_current_response.value = False
        self.normal_tobacco_smoking_history.smoking_current_response.save()


    def test_title_returns_the_title_of_the_type(self):
        presenter = TobaccoSmokingHistoryTypePresenter(self.response_set.tobacco_smoking_history.cigarettes())
        self.assertEqual(presenter.title(), "Cigarette")


    def test_delegates_the_url_type_to_the_normal_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryTypePresenter(self.response_set.tobacco_smoking_history.cigarettes())
        self.assertEqual(presenter.url_type(), "cigarettes")

    def test_delegates_the_human_type_to_the_normal_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryTypePresenter(self.response_set.tobacco_smoking_history.cigarettes())
        self.assertEqual(presenter.human_type(), "Cigarettes")

    def test_summary_items_returns_the_normal_summary_items_by_default(self):
        presenter = TobaccoSmokingHistoryTypePresenter(self.response_set.tobacco_smoking_history.cigarettes())

        self.assertEqual(
            presenter.summary_items(),
            [
                {
                    "key": { "text": "Total number of years you smoked cigarettes" },
                    "value": { "text": "10 years" }
                },
                {
                    "key": { "text": "Previous cigarette smoking" },
                    "value": { "text": "7 cigarettes a week" }
                }
            ]
        )

    def test_summary_items_returns_the_increased_summary_items_if_the_tobacco_smoking_history_is_increased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
            increased=True,
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=SmokingFrequencyValues.DAILY,
        )
        SmokedAmountResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=50,
        )
        SmokedTotalYearsResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=10,
        )

        presenter = TobaccoSmokingHistoryTypePresenter(self.response_set.tobacco_smoking_history.cigarettes())

        self.assertIn(
            {
                "key": {"text": "When you smoked more than 7 cigarettes a week"},
                "value": {"text": "50 cigarettes a day for 10 years"},
            },
            presenter.summary_items(),
        )

    def test_summary_items_returns_the_decreased_summary_items_if_the_tobacco_smoking_history_is_decreased(self):
        tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            response_set=self.response_set,
            cigarettes=True,
            decreased=True,
        )
        SmokingFrequencyResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=SmokingFrequencyValues.DAILY,
        )
        SmokedAmountResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=50,
        )
        SmokedTotalYearsResponseFactory.create(
            tobacco_smoking_history=tobacco_smoking_history,
            value=10,
        )

        presenter = TobaccoSmokingHistoryTypePresenter(self.response_set.tobacco_smoking_history.cigarettes())

        self.assertIn(
            {
                "key": {"text": "When you smoked fewer than 7 cigarettes a week"},
                "value": {"text": "50 cigarettes a day for 10 years"},
            },
            presenter.summary_items(),
        )
