import logging

# 로거
logger = logging.getLogger(__name__)


class TimeCheckError(Exception):
    pass