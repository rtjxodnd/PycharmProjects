import logging

# 로거
logger = logging.getLogger(__name__)


class TimeCheckError(Exception):
    logger.error("ERROR!!!!: main_process")
    logger.error("09시 이전 처리 불가")
    pass