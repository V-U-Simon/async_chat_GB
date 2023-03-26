"""Запуск скрипта-дочернего процесса"""

from subprocess import Popen, PIPE

PROC = Popen(
    "python test_ex.py",
    shell=True,
    stdout=PIPE, stderr=PIPE
)

# получить tuple('stdout', 'stderr')
RES = PROC.communicate()
print(PROC.returncode)
if PROC.returncode == 0:
    print(RES)
print('result:', RES[0])
