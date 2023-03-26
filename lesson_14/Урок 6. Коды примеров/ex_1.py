"""Хэширование"""

# Для шифрования строк предназначен модуль hashlib
import hashlib
# Для конвертации данных в бинарный вид и в различные
# представления строк: 16-ричное, 64-ричное
import binascii


# -------------------------- Простая хэш-функция ----------------------- #

# Создание объекта хэш-суммы
# <class '_hashlib.HASH'>
HASH_OBJ = hashlib.md5()
print(type(HASH_OBJ))

# Добавление данных для расчета суммы - можно добавлять только строку байтов
HASH_OBJ.update(b'Python')
# Вывод хэш-суммы
# Получить зашифрованную последовательность байтов
# и строку позволяют два метода — digest() и hexdigest()
print(HASH_OBJ.hexdigest())

# ------------------------- Хэш для пароля ----------------------------- #

"""
Модуль hashlib также содержит функции для хэширования (расширения) паролей. 
Хорошая функция хэширования паролей должна быть настраиваемой, 
вычисляться медленно и включать криптографическую «соль».
"""

# <class 'bytes'>
PASSWD_OBJ = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
print(type(PASSWD_OBJ))

# hash_name - строка с именем алгоритма хэширования ('sha1', 'sha256' и т.д.)
# password, salt - строки байтов, salt длиной 16 и более байт
# iterations — количество итераций (из расчета примерно 100000 для SHA-256)
# Количество итераций следует выбирать на основе алгоритма хеширования и вычислительной мощности.
# По состоянию на 2013 год предлагается не менее 100 000 итераций SHA-256.


# Вычисленное значение можно хранить в БД
print(PASSWD_OBJ)

# Метод binascii.hexlify() преобразует bytes в bytes представляющие шестнадцатеричную строку ascii.
# Это означает, что каждый байт на входе будет преобразован в два символа ascii.
print(binascii.hexlify(PASSWD_OBJ))
