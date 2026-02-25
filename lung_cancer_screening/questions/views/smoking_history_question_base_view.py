from inflection import camelize

from ..models.tobacco_smoking_history import TobaccoSmokingHistory
from .question_base_view import QuestionBaseView


class SmokingHistoryQuestionBaseView(QuestionBaseView):
    def get_object(self):
        return self.model.objects.get_or_build(
            tobacco_smoking_history=self.get_smoking_history_item()
        )[0]

    def get_smoking_history_item(self):
        if not self.kwargs.get("level"):
            return self.get_normal_smoking_history_item()
        else:
            return self.request.response_set.tobacco_smoking_history.filter(
                type=camelize(self.kwargs["tobacco_type"]),
                level=self.kwargs.get("level")
            ).first()

    def get_normal_smoking_history_item(self):
        return self.request.response_set.tobacco_smoking_history.filter(
            type=camelize(self.kwargs["tobacco_type"]),
            level=TobaccoSmokingHistory.Levels.NORMAL
        ).first()
