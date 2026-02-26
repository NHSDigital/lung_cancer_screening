from inflection import singularize

from lung_cancer_screening.questions.presenters.base_presenter import BasePresenter
from lung_cancer_screening.questions.presenters.tobacco_smoking_history_presenter import TobaccoSmokingHistoryPresenter

class TobaccoSmokingHistoryTypePresenter(BasePresenter):
    def __init__(self, tobacco_smoking_history):
        self.tobacco_smoking_history = tobacco_smoking_history

    def normal_tobacco_smoking_history(self):
        return TobaccoSmokingHistoryPresenter(
            self.tobacco_smoking_history.normal().first()
        )

    def increased_tobacco_smoking_history(self):
        increased = self.tobacco_smoking_history.increased().first()
        return TobaccoSmokingHistoryPresenter(increased) if increased else None

    def decreased_tobacco_smoking_history(self):
        decreased = self.tobacco_smoking_history.decreased().first()
        return TobaccoSmokingHistoryPresenter(decreased) if decreased else None

    def title(self):
        return singularize(self.normal_tobacco_smoking_history().human_type())

    def url_type(self):
        return self.normal_tobacco_smoking_history().url_type()

    def human_type(self):
        return self.normal_tobacco_smoking_history().human_type()

    def current_or_previous(self):
        return "Current" if self.normal_tobacco_smoking_history().is_current() else "Previous"

    def normal_summary_items(self):
        return [
            self._check_your_answer_item(
                f"Total number of years you smoked {self.human_type().lower()}",
                self.normal_tobacco_smoking_history().duration_years(),
            ),
            self._check_your_answer_item(
                f"{self.current_or_previous()} {singularize(self.human_type().lower())} smoking",
                self.normal_tobacco_smoking_history().to_sentence(),
            ),
        ]

    def increased_summary_items(self):
        return [
            self._check_your_answer_item(
                f"When you smoked more than {self.normal_tobacco_smoking_history().to_sentence()}",
                f"{self.increased_tobacco_smoking_history().to_sentence()} for {self.increased_tobacco_smoking_history().duration_years()}",
            ),
        ]

    def decreased_summary_items(self):
        return [
            self._check_your_answer_item(
                f"When you smoked fewer than {self.normal_tobacco_smoking_history().to_sentence()}",
                f"{self.decreased_tobacco_smoking_history().to_sentence()} for {self.decreased_tobacco_smoking_history().duration_years()}",
            ),
        ]

    def summary_items(self):
        result = self.normal_summary_items()

        if self.increased_tobacco_smoking_history():
            result.extend(self.increased_summary_items())

        if self.decreased_tobacco_smoking_history():
            result.extend(self.decreased_summary_items())

        return result


    def _check_your_answer_item(self, question, value):
        return {
            "key": { "text": question },
            "value": { "text": value },
        }
