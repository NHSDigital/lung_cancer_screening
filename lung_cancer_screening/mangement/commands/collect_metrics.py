import logging

from django.core.management.base import BaseCommand, CommandError

from lung_cancer_screening.services.model_metrics_collector import ModelMetricsCollector

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Collects current model metrics and exports them via OpenTelemetry."

    def handle(self, *args, **options):
        try:
            ModelMetricsCollector().collect()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise CommandError(e)
