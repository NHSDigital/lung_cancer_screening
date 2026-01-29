import humps
from .question_base_view import QuestionBaseView

class SmokingHistoryQuestionBaseView(QuestionBaseView):
    def get_object(self):
        return self.model.objects.get_or_build(
            tobacco_smoking_history=self._get_history_item_for_type()
        )[0]

    def _get_history_item_for_type(self):
        return self.request.response_set.tobacco_smoking_history.filter(
            type=humps.pascalize(self.kwargs["tobacco_type"])
        ).first()
