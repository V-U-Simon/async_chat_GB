from loguru import _Logger as Logger
from loguru import logger
from messenger.config import DEBUG_LEVEL, DEBUG_START, DEBUG_FINISH, DEBUG_MARKER

from io import StringIO
from pprint import pprint
import functools
import sys

format: str = "{time} <b>{level:<8}</b> | <cyan>{name:<35}</cyan>:<cyan>{line:<4}</cyan> | <cyan>{function:<20}</cyan> {message}"

logger.remove()
level = DEBUG_LEVEL
logger.add(sys.stderr, level=level, format=format, colorize=True)
logger.add('messenger/logs.log')


def pretty(data=''):
    buffer = StringIO()
    pprint(data, buffer)
    return "\n" + buffer.getvalue()


def log(*, marker: str = DEBUG_MARKER, message: str = '', entry=DEBUG_START, exit=DEBUG_FINISH):
    """ 
    decorator for logging function 
    """

    def _log(func):

        @functools.wraps(func)
        def wrapped(*args, **kwargs):

            # setup right display (record) function name and line number
            l: Logger = logger.patch(lambda r: r.update(function=func.__name__, line=func.__code__.co_firstlineno))

            # yapf: disable
            if entry: l.debug(f'🚀 start  | {marker:<5} {message} | 📦 {args=} / 📦 {kwargs=}')

            result = func(*args, **kwargs)

            if exit:  l.debug(f'🏁 finish | {marker:<5} {message} | 📦 {result=}')
            # yapf: enable

            return result

        return wrapped

    return _log


if __name__ == '__main__':

    # using example
    @log(marker="🀄", message=None)
    def test(args='default'):
        logger.critical('message')
        logger.warning('message')
        logger.info('messagemessagemessagemessagemessagemessage')
        return args

    @log(message='message2')
    def test22(args='default2'):
        logger.debug('message')
        logger.trace('message')
        return args

    test()

    var = {
        'list': ('test', 'test2', 'test3', 'test3', 'test4'),
        'key': 'value',
    }
    test(var)
    test22('SLDFJSDLFJLSDKJFL')
