from django.http import Http404
from inflection import camelize

class EnsureSmokingHistoryForTypeMixin:

    def dispatch(self, request, *args, **kwargs):
        url_tobacco_type = camelize(kwargs["tobacco_type"])

        if request.response_set.tobacco_smoking_history.filter(type=url_tobacco_type).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
