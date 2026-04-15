import logging
import os
from threading import Lock

from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

logger = logging.getLogger(__name__)


class Metrics:
    _instance = None
    _lock = Lock()
    _initialised = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        logger.info(
                "Going into Metrics class."
            )
        if self.__class__._initialised:
            return

        connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        environment = os.getenv("ENVIRONMENT", "unknown")

        if not connection_string:
            logger.warning(
                "APPLICATIONINSIGHTS_CONNECTION_STRING not set; metrics will be no-op."
            )
            self.meter = metrics.get_meter("lungcs.models")
        else:
            exporter = AzureMonitorMetricExporter(
                connection_string=connection_string
            )
            provider = MeterProvider(
                metric_readers=[PeriodicExportingMetricReader(exporter)]
            )
            metrics.set_meter_provider(provider)
            self.meter = metrics.get_meter("lungcs.models")

        self.environment = environment

        # Create instruments once
        self.requests_created = self.meter.create_counter(
            name="requests.created",
            unit="1",
            description="Number of request records created",
        )
        self.requests_submitted = self.meter.create_counter(
            name="requests.submitted",
            unit="1",
            description="Number of request records submitted",
        )

        self.__class__._initialised = True

    def record_request_created(self, model_name: str):
        self.requests_created.add(
            1,
            {
                "environment": self.environment,
                "model": model_name,
            },
        )

    def record_request_submitted(self, model_name: str):
        self.requests_submitted.add(
            1,
            {
                "environment": self.environment,
                "model": model_name,
            },
        )

    def set_gauge_value(self, metric_name, units, description, value):
        logger.debug(
            (
                f"Metrics: set_gauge_value(metric_name: {metric_name} "
                f"units: {units}, description: {description}, value: {value})"
            )
        )

        # Create gauge metric
        gauge = self.meter.create_gauge(
            metric_name, unit=units, description=description
        )

        # Set metric value
        gauge.set(
            value,
            {"environment": self.environment},
        )
