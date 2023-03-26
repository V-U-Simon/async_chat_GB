"""Функции модуля os"""

import os

# информация о платформе
# ‘posix’, ‘nt’, ‘os2’, ‘ce’, ‘java’, ‘riscos’
# ответ: nt для Windows
print(os.name)

# дает вам полезную информацию, такую как количество процессоров
# , тип ОЗУ, имя компьютера, и так далее
print(os.environ)

# узнать, сколько процессорных ядер в системе
print(os.environ["NUMBER_OF_PROCESSORS"])

# какой путь вы в данный момент используете
print(os.getcwd())

# изменяем текущий путь
os.chdir("new_dir")
print(os.getcwd())

# создаем папку в новом текущем каталоге new_dir
# это папка my_dir
PATH = "my_dir"
os.mkdir(PATH)

# удаление папки
os.rmdir("my_dir")

# удаление файла
os.remove("test.txt")
