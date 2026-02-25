from inflection import dasherize, underscore

from lung_cancer_screening.questions.presenters.base_presenter import BasePresenter

class TobaccoSmokingHistoryPresenter(BasePresenter):
    def __init__(self, tobacco_smoking_history):
        self.tobacco_smoking_history = tobacco_smoking_history

    def human_type(self):
        return self.tobacco_smoking_history.human_type()

    def url_type(self):
        return dasherize(underscore(self.tobacco_smoking_history.type)).lower()

    def duration_years(self):
        if not self.tobacco_smoking_history.duration_years():
            return self.NOT_ANSWERED_TEXT

        return f"{self.tobacco_smoking_history.duration_years()} years"

    def is_current(self):
        return self.tobacco_smoking_history.is_current()

    def to_sentence(self):
        return f"{self.tobacco_smoking_history.amount()} {self.tobacco_smoking_history.human_type().lower()} a {self.tobacco_smoking_history.frequency_singular()}"

