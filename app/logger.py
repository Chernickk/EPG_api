import sys

from loguru import logger

from settings import RUN_LEVEL

logger.add(sys.stderr, level="INFO" if RUN_LEVEL == 'prod' else "DEBUG")
