from django.test import TestCase


from lung_cancer_screening.questions.tests.factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from lung_cancer_screening.questions.models.smoking_frequency_response import SmokingFrequencyValues

from lung_cancer_screening.questions.presenters.tobacco_smoking_history_presenter import (
    TobaccoSmokingHistoryPresenter,
)


class TestTobaccoSmokingHistoryPresenter(TestCase):
    def setUp(self):
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.build(
            rolled_cigarettes=True,
            complete=True,
        )

    def test_delgates_human_type_to_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.human_type(),
            "Rolled cigarettes, or roll-ups"
        )

    def test_url_type_returns_the_url_type_of_the_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.url_type(),
            "rolled-cigarettes"
        )

    def test_duration_years_returns_not_answered_text_if_duration_years_is_not_set(self):
        self.tobacco_smoking_history.smoked_total_years_response = None
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.duration_years(),
            TobaccoSmokingHistoryPresenter.NOT_ANSWERED_TEXT
        )

    def test_duration_years_returns_the_number_of_years_as_a_string(self):
        self.tobacco_smoking_history.smoked_total_years_response.value = 10
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.duration_years(),
            "10 years"
        )

    def is_current_delegates_to_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.is_current(),
            self.tobacco_smoking_history.is_current()
        )


    def test_to_sentence_returns_the_amount_of_type_per_frequency(self):
        self.tobacco_smoking_history.smoked_amount_response.value = 7
        self.tobacco_smoking_history.smoking_frequency_response.value = SmokingFrequencyValues.WEEKLY

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.to_sentence(),
            "7 rolled cigarettes, or roll-ups a week"
        )
