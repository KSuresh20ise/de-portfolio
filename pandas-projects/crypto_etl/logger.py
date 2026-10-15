import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "etl.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


"""
Python has a built-in logging module.
It allows you to record events such as:

INFO     → normal information
WARNING  → something unexpected
ERROR    → something failed
DEBUG    → detailed debugging information
CRITICAL → serious failure

"""