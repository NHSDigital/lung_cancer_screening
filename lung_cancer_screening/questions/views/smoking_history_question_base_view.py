from inflection import camelize
from .question_base_view import QuestionBaseView

class SmokingHistoryQuestionBaseView(QuestionBaseView):
    def get_object(self):
        return self.model.objects.get_or_build(
            tobacco_smoking_history=self.get_smoking_history_item()
        )[0]


    def get_smoking_history_item(self):
        return self.request.response_set.tobacco_smoking_history.filter(
            type=camelize(self.kwargs["tobacco_type"])
        ).first()
