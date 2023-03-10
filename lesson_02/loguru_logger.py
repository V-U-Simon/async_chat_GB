import sys
from loguru import logger
import pprint
from io import StringIO


def pretty(data):
    buffer = StringIO()
    pprint.pprint(data, buffer)
    return "\n" + buffer.getvalue()


logger.add(
    f"{__name__}1.log",
    # sys.stdout,
    format="{time} {level} {message}",
    # format=custom_formatter,
    # format="<green>{time}</green> {level} <level>{message}</level>",
    level="DEBUG",
    serialize=True,
)

logger.pretty = pretty
