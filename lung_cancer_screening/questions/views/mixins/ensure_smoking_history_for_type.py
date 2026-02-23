from inflection import camelize
from django.http import Http404

from lung_cancer_screening.questions.models.tobacco_smoking_history import TobaccoSmokingHistory

class EnsureSmokingHistoryForTypeMixin:

    def dispatch(self, request, *args, **kwargs):
        url_tobacco_type = camelize(kwargs["tobacco_type"])
        level = kwargs.get("level", TobaccoSmokingHistory.Levels.NORMAL)

        tobacco_smoking_history_item = request.response_set.tobacco_smoking_history.filter(
            type=url_tobacco_type,
            level=level
        )

        if tobacco_smoking_history_item.exists():
            request.tobacco_smoking_history_item = tobacco_smoking_history_item.first()
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
