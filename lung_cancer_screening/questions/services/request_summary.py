import logging
from ..models.response_set import ResponseSet

logger = logging.getLogger(__name__)

class RequestSummary:

    def __init__(self):
        logger.info("RequestSummary: init")

    def get_submitted_count(self):

        return ResponseSet.objects.submitted().count()

    def get_count(self):

        return ResponseSet.objects.count()

    def get_summary(self):
        return {
            "total": self.get_count(),
            "submitted": self.get_submitted_count(),
        }
