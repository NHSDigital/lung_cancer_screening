import logging
import os

import requests
from django.core.management.base import BaseCommand, CommandError
from lung_cancer_screening.questions.services.request_summary import RequestSummary

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Counts the number of submitted requests."

    def handle(self, *args, **options):

        logger.info("Command: Request Summary.")
        try:
            rs = RequestSummary()
            summary = rs.get_summary()

            self.stdout.write(str(summary))

            slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

            if not slack_webhook_url:
                logger.warning("SLACK_WEBHOOK_URL is not set; skipping Slack notification.")
                return

            payload = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Request Summary",
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Requests:*\n{rs.get_count()}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Submitted:*\n{rs.get_submitted_count()}"
                                }
                            ]
                        }
                    ]
                }

            response = requests.post(
                slack_webhook_url,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()

            logger.info("Request summary sent to Slack.")

        except Exception as e:
            logger.error(e, exc_info=True)
            raise CommandError(e)
