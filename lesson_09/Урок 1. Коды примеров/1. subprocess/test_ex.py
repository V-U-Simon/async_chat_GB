"""Получение кода завершения подпроцесса"""

from subprocess import Popen

PROGRAM = "regedit.exe"
PROCESS = Popen(PROGRAM)
