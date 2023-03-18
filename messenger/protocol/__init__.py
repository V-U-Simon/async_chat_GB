from .request import AccountName, ChatName, Password
from .request import UserWithPassword, UserWithoutPassword

from .request import Request
from .request import Auth, AuthQuit, AuthPresence, AuthPrоbe
from .request import Message, ChatJoin, ChatLeave

POSSIBLE_REQUESTS = {
    'authenticate': Auth,
    'quit': AuthQuit,
    'presence': AuthPresence,
    'authprobe': AuthPrоbe,
    'msg': Message,
    'join': ChatJoin,
    'leave': ChatLeave,
}

from .response import Responce
from .response import Responce100, Responce200
from .response import Responce300, Responce400, Responce402, Responce409, Responce500

POSSIBLE_RESPONSES = {
    100: Responce100,
    200: Responce200,
    300: Responce300,
    400: Responce400,
    402: Responce402,
    409: Responce409,
    500: Responce500,
}
