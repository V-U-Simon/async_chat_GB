"""Связь с дочерним процессом"""

from subprocess import Popen, PIPE
import chardet

ARGS = ["ping", "www.google.ru"]
PROCESS = Popen(ARGS, stdout=PIPE)

# communicate - связь с созданным процессом
# None – это результат stderr, а это значит, что ошибок не найдено
DATA = PROCESS.communicate()
print(DATA)  # -> вернет кортеж (stdout, stderr)
RESULT = chardet.detect(DATA[0])
OUT = DATA[0].decode(RESULT['encoding'])
print(OUT)
