from django.test import TestCase, tag

from lung_cancer_screening.questions.tests.factories.response_set_factory import ResponseSetFactory
from lung_cancer_screening.questions.tests.factories.age_when_started_smoking_response_factory import AgeWhenStartedSmokingResponseFactory
from lung_cancer_screening.questions.tests.factories.tobacco_smoking_history_factory import TobaccoSmokingHistoryFactory
from lung_cancer_screening.questions.models.smoking_frequency_response import SmokingFrequencyValues

from lung_cancer_screening.questions.presenters.tobacco_smoking_history_presenter import (
    TobaccoSmokingHistoryPresenter,
)
from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory

@tag("wip")
class TestTobaccoSmokingHistoryPresenter(TestCase):
    def setUp(self):
        self.response_set = ResponseSetFactory.create()
        self.age_when_started_smoking_response = AgeWhenStartedSmokingResponseFactory.create(
            response_set=self.response_set
        )
        self.tobacco_smoking_history = TobaccoSmokingHistoryFactory.create(
            rolling_tobacco=True,
            complete=True,
            response_set=self.response_set
        )

    def test_delgates_human_type_to_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.human_type(),
            "Rolling tobacco"
        )

    def test_url_type_returns_the_url_type_of_the_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.url_type(),
            "rolling-tobacco"
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
            "7 grams of rolling tobacco a week"
        )

    def test_unit_returns_the_unit_of_the_tobacco_smoking_history(self):
        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.unit(),
            "grams of rolling tobacco"
        )


    def test_smoke_or_smoked_returns_present_tense_if_current_normal_level(self):
        self.tobacco_smoking_history.smoking_current_response.value = True
        self.tobacco_smoking_history.smoking_current_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.smoke_or_smoked(),
            "smoke"
        )

    def test_smoke_or_smoked_returns_past_tense_if_not_current_normal_level(self):
        self.tobacco_smoking_history.smoking_current_response.value = False
        self.tobacco_smoking_history.smoking_current_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(presenter.smoke_or_smoked(), "smoked")


    def test_smoke_or_smoked_returns_past_tense_if_changed_type(self):
        self.tobacco_smoking_history.level = TobaccoSmokingHistory.Levels.INCREASED
        self.tobacco_smoking_history.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(presenter.smoke_or_smoked(), "smoked")


    def test_frequency_returns_the_human_frequency_of_the_tobacco_smoking_history(self):
        self.tobacco_smoking_history.smoking_frequency_response.value = SmokingFrequencyValues.WEEKLY
        self.tobacco_smoking_history.smoking_frequency_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.frequency(),
            "week"
        )


    def test_more_or_fewer_text_returns_more_if_increased_level(self):
        self.tobacco_smoking_history.level = TobaccoSmokingHistory.Levels.INCREASED
        self.tobacco_smoking_history.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.more_or_fewer(),
            "more"
        )

    def test_more_or_fewer_text_returns_fewer_if_decreased_level(self):
        self.tobacco_smoking_history.level = TobaccoSmokingHistory.Levels.DECREASED
        self.tobacco_smoking_history.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.more_or_fewer(),
            "fewer"
        )

    def test_do_or_did_returns_do_if_current_normal_level(self):
        self.tobacco_smoking_history.smoking_current_response.value = True
        self.tobacco_smoking_history.smoking_current_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.do_or_did(),
            "do"
        )

    def test_do_or_did_returns_did_if_not_current_normal_level(self):
        self.tobacco_smoking_history.smoking_current_response.value = False
        self.tobacco_smoking_history.smoking_current_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.do_or_did(),
            "did"
        )

    def test_do_or_did_returns_did_if_changed_level(self):
        self.tobacco_smoking_history.level = TobaccoSmokingHistory.Levels.INCREASED
        self.tobacco_smoking_history.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.do_or_did(),
            "did"
        )


    def currently_or_previously_returns_currently_if_current_normal_level(self):
        self.tobacco_smoking_history.smoking_current_response.value = True
        self.tobacco_smoking_history.smoking_current_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.currently_or_previously(),
            "currently"
        )

    def currently_or_previously_returns_previously_if_not_current_normal_level(self):
        self.tobacco_smoking_history.smoking_current_response.value = False
        self.tobacco_smoking_history.smoking_current_response.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.currently_or_previously(),
            "previously"
        )

    def currently_or_previously_returns_previously_if_changed_level(self):
        self.tobacco_smoking_history.level = TobaccoSmokingHistory.Levels.INCREASED
        self.tobacco_smoking_history.save()

        presenter = TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

        self.assertEqual(
            presenter.currently_or_previously(),
            "previously"
        )
