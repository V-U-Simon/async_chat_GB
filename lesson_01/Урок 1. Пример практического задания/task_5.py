"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet
"""

import subprocess
import chardet

# ARGS = ['ping', 'yandex.ru']
# YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
# for line in YA_PING.stdout:
#     result = chardet.detect(line)
#     print(result)
#     line = line.decode(result['encoding']).encode('utf-8')
#     print(line.decode('utf-8'))


ARGS = ['ping', '-c', '3', 'yandex.ru']


res = subprocess.run(ARGS, capture_output=True, text=True)
print(res.stdout)
res = subprocess.run(ARGS, stdout=subprocess.PIPE, text=True)
print(res.stdout)

