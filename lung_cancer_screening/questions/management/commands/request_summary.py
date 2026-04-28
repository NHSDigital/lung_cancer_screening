import logging

from django.core.management.base import BaseCommand, CommandError
from lung_cancer_screening.questions.services.request_summary import RequestSummary

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Counts the number of submitted requests."

    def handle(self, *args, **options):
        logger.info("Command: SubmittedCount.")
        try:
            rs = RequestSummary()
            summary = rs.get_summary()

            self.stdout.write(str(summary))

        except Exception as e:
            logger.error(e, exc_info=True)
            raise CommandError(e)
