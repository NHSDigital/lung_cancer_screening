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
        if self.__class__._initialised:
            return

        logger.info("Going into Metrics class.")

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
        self._gauges = {}

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
        logger.info(
            "Metrics: record_request_created(model_name=%s)",
            model_name
        )
        self.requests_created.add(
            1,
            {
                "environment": self.environment,
                "model": model_name,
            },
        )

    def record_request_submitted(self, model_name: str):
        logger.info(
            "Metrics: record_request_submitted(model_name=%s)",
            model_name
        )
        logger.info("record_request_submitted.")
        self.requests_submitted.add(
            1,
            {
                "environment": self.environment,
                "model": model_name,
            },
        )

    def set_gauge_value(self, metric_name, units, description, value):
        logger.debug(
            "Metrics: set_gauge_value(metric_name=%s, units=%s, description=%s, value=%s)",
            metric_name,
            units,
            description,
            value,
        )

        gauge = self._gauges.get(metric_name)
        if gauge is None:
            gauge = self.meter.create_gauge(
                name=metric_name,
                unit=units,
                description=description,
            )
            self._gauges[metric_name] = gauge

        gauge.record(
            value,
            {"environment": self.environment},
        )
