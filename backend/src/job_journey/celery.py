import logging
import os
from typing import Any

from celery import Celery
from celery.signals import setup_logging  # noqa

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_journey.settings')

celery_app = Celery('job_journey')


@setup_logging.connect
def config_loggers(*args: Any, **kwargs: Any) -> None:
    from logging.config import dictConfig  # noqa

    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
