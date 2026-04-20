import logging

from django.apps import apps
from django.db import models

from lung_cancer_screening.questions.models.base import BaseModel
from lung_cancer_screening.questions.services.metrics import Metrics

logger = logging.getLogger(__name__)


class ModelMetricsCollector:
    """
    Collects current-state metrics for all models inheriting from BaseModel.

    Emits:
      - model_records_<model_name>
      - model_submitted_records_<model_name>   (only for models with a status field)
    """

    def __init__(self):
        logger.info(
            "ModelMetricsCollector: Starting collection of model metrics."   )
        self.metrics = Metrics()

    def collect(self):
        logger.info(
            "ModelMetricsCollector: collect."   )
        for model in apps.get_models():
            if not issubclass(model, BaseModel) or model._meta.abstract:
                continue

            self._collect_for_model(model)

    def _collect_for_model(self, model: type[models.Model]):
        model_name = model._meta.label_lower.replace(".", "_")

        total_count = model.objects.count()

        logger.info(
            "ModelMetricsCollector: _collect_for_model."
            " model=%s, total_count=%d",
            model._meta.label_lower,
            total_count
        )

        self.metrics.set_gauge_value(
            metric_name=f"model_records_{model_name}",
            units="records",
            description=f"Current number of records for {model._meta.label_lower}",
            value=total_count,
        )

        status_field = self._get_status_field(model)
        if status_field:
            submitted_count = model.objects.filter(status="submitted").count()
            self.metrics.set_gauge_value(
                metric_name=f"model_submitted_records_{model_name}",
                units="records",
                description=f"Current number of submitted records for {model._meta.label_lower}",
                value=submitted_count,
            )

    @staticmethod
    def _get_status_field(model: type[models.Model]):
        return next(
            (field for field in model._meta.fields if field.name == "status"),
            None,
        )
