from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from time import time
from dataclasses import asdict

Alert = str | None
Error = str | None


class Responce(BaseModel):
    response: int
    time: float = time()


class Responce100(Responce):
    response: int = 100
    alert: Alert = None


class Responce200(Responce):
    response: int = 200
    alert: Alert = None


class Responce300(Responce):
    response: int = 300
    error: Error = None


class Responce400(Responce):
    response: int = 400
    error: Error = None


class Responce402(Responce):
    response: int = 402
    error: Error = "This could be wrong password or no account with that name"


class Responce409(Responce):
    response: int = 409
    error: Error = "Someone is already connected with the given user name"


class Responce500(Responce):
    response: int = 500
    error: Error = None
