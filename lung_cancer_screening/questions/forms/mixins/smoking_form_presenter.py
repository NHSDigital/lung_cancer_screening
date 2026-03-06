from functools import cached_property

from lung_cancer_screening.questions.presenters.tobacco_smoking_history_presenter import TobaccoSmokingHistoryPresenter

class SmokingFormPresenter:
    @cached_property
    def presenter(self):
        return TobaccoSmokingHistoryPresenter(self.tobacco_smoking_history)

    @cached_property
    def normal_presenter(self):
        return TobaccoSmokingHistoryPresenter(self.normal_tobacco_smoking_history)

