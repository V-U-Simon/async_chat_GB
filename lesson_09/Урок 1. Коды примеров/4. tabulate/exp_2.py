"""Форматирование таблиц в tabulate"""

from tabulate import tabulate

# Табличное представление списка словарей
DICTS_LIST = [{'programming language': 'Python',
               'type': 'interpreted',
               'year': '1991'},
              {'programming language': 'JAVA',
               'type': 'compiled',
               'year': '1995'},
              {'programming language': 'С',
               'type': 'compiled',
               'year': '1972'}]

# grid-формат
print(tabulate(DICTS_LIST, headers='keys', tablefmt="grid"))

print()

# markdown-формат
print(tabulate(DICTS_LIST, headers='keys', tablefmt="pipe"))

print()

# html-формат
print(tabulate(DICTS_LIST, headers='keys', tablefmt="html"))

print()

# Выравнивание столбцов
# Выравнивание по центру
print(tabulate(DICTS_LIST, headers='keys', tablefmt="pipe", stralign="center"))
