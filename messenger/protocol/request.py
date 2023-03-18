from messenger.config import ENCODING
from pydantic import BaseModel
from time import time

AccountName = str
ChatName = str  #todo: add validation for start with #
Password = str  #todo: add validation for password and also it should be encripted in sha


class UserWithoutPassword(BaseModel):
    account_name: AccountName
    status: str | None = 'Yep, I am here!'


class UserWithPassword(UserWithoutPassword):
    password: Password


class Request(BaseModel):
    time: float = time()
    action: str


class Auth(Request):
    action: str = 'authenticate'
    user: UserWithPassword


class AuthQuit(Request):
    action: str = 'quit'
    user: UserWithoutPassword


class AuthPresence(Request):
    action: str = 'presence'
    type: str | None = 'status'
    user: UserWithoutPassword | None = None


class AuthPrоbe(Request):
    action: str = 'prоbe'


class Message(Request):
    action: str = 'msg'
    to: AccountName | ChatName
    from_: AccountName
    encoding: str = ENCODING
    message: str


class ChatJoin(Message):
    action: str = 'join'
    room: ChatName


class ChatLeave(Message):
    action: str = 'leave'
    room: ChatName
