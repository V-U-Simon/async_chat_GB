"""Работа с БД через PyQt"""

import sys
from PyQt5 import QtWidgets, QtSql

# QTableView, QTreeView, QListView

# Открытие базы данных SQLite
con1 = QtSql.QSqlDatabase.addDatabase('QSQLITE')
con1.setDatabaseName('C://work//data.sqlite')
con1.open()
con1.close()

# Открытие базы данных MySQL
con2 = QtSql.QSqlDatabase.addDatabase('QMYSQL')
con2.setHostName('localhost')
con2.setDatabaseName('TestDB')
con2.setUserName('Mario')
con2.setPassword('karabuka')
con2.open()
con2.close()
