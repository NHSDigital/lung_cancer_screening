from django.http import Http404

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory

class EnsureSmokingHistoryForTypeMixin:

    def dispatch(self, request, *args, **kwargs):
        self.ensure_smoking_history_item_exists()
        return super().dispatch(request, *args, **kwargs)

    def ensure_smoking_history_item_exists(self):
        try:
            self.tobacco_smoking_history_item()
        except TobaccoSmokingHistory.DoesNotExist:
            raise Http404("Tobacco smoking history item not found")


    def tobacco_type(self):
        return self.kwargs["tobacco_type"]


    def level(self):
        return self.kwargs.get("level", TobaccoSmokingHistory.Levels.NORMAL)


    def tobacco_smoking_history_item(self):
        return self.request.response_set.tobacco_smoking_history.by_url_type(
            self.tobacco_type(),
        ).get(
            level=self.level()
        )
