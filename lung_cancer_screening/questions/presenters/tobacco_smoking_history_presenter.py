from lung_cancer_screening.questions.presenters.base_presenter import BasePresenter

class TobaccoSmokingHistoryPresenter(BasePresenter):
    def __init__(self, tobacco_smoking_history):
        self.tobacco_smoking_history = tobacco_smoking_history


    def get_type_display(self):
        return self.tobacco_smoking_history.get_type_display()

    def human_type(self):
        return self.tobacco_smoking_history.human_type()

    def url_type(self):
        return self.tobacco_smoking_history.url_type()

    def duration_years(self):
        if not self.tobacco_smoking_history.duration_years():
            return self.NOT_ANSWERED_TEXT

        return f"{self.tobacco_smoking_history.duration_years()} years"

    def is_normal(self):
        return self.tobacco_smoking_history.is_normal()

    def is_current(self):
        return self.tobacco_smoking_history.is_current()

    def amount_prefix(self):
        return "grams of " if self.tobacco_smoking_history.is_rolling_tobacco() else ""

    def unit(self):
        return self.tobacco_smoking_history.unit()

    def frequency(self):
        return self.tobacco_smoking_history.frequency_singular()


    def is_present_tense(self):
        return (
            self.is_normal()
            and self.is_current()
        )


    def smoke_or_smoked(self):
        if self.is_present_tense():
            return "smoke"

        return "smoked"


    def do_or_did(self):
        if self.is_present_tense():
            return "do"

        return "did"


    def have_you_smoked_or_did_you_smoke(self):
        if self.is_present_tense():
            return "have you smoked"

        return "did you smoke"


    def more_or_fewer(self):
        if self.tobacco_smoking_history.is_increased():
            return "more"
        elif self.tobacco_smoking_history.is_decreased():
            return "fewer"


    def currently_or_previously(self):
        if self.is_present_tense():
            return "currently"

        return "previously"


    def to_sentence(self):
        return f"{self.tobacco_smoking_history.amount()} {self.tobacco_smoking_history.unit()} a {self.tobacco_smoking_history.frequency_singular()}"

