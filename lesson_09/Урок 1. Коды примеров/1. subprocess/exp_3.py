"""Получение кода завершения подпроцесса"""

from subprocess import Popen

'''
Здесь мы создали переменную под названием program и назначили ей значение notepad.exe. 
После этого мы передали её классу Popen. После запуска этого кода, вы увидите, 
что он мгновенно вернет объект subprocess.Popen, а вызванное приложение будет выполняться. 
'''

# сравните = не ждать закрытия приллжения
PROGRAM = "regedit.exe"
PROCESS = Popen(PROGRAM)

print(PROCESS)

# и это = ждать закрытия приллжения
PROGRAM = "regedit.exe"
PROCESS = Popen(PROGRAM)
CODE = PROCESS.wait()

print(PROCESS)
print(CODE)
