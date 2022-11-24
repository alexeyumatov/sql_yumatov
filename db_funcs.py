import sqlite3
from PyQt5 import QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import QHeaderView

conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('coffee.sqlite')
db.open()


def table_view(self, view):
    model = QSqlTableModel(self, db)
    model.setQuery(QSqlQuery("""SELECT coffee_info.sort_name, roasting.roast_type,
                                    consistency.consistency_type, coffee_info.taste_description, coffee_info.price,
                                    coffee_info.coffee_amount, coffee_info.id
                                    FROM coffee_info
                                    LEFT JOIN roasting ON coffee_info.roast = roasting.roast_id
                                    LEFT JOIN consistency ON coffee_info.consistency = consistency.id"""))

    model.setHeaderData(0, QtCore.Qt.Horizontal, 'Название сорта')
    model.setHeaderData(1, QtCore.Qt.Horizontal, 'Степень обжарки')
    model.setHeaderData(2, QtCore.Qt.Horizontal, 'Консистенция')
    model.setHeaderData(3, QtCore.Qt.Horizontal, 'Описание вкуса')
    model.setHeaderData(4, QtCore.Qt.Horizontal, 'Цена')
    model.setHeaderData(5, QtCore.Qt.Horizontal, 'Объем упаковки, г.')

    model.select()
    view.setModel(model)
    view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


def get_roast_value():
    res = cursor.execute("""SELECT roast_type FROM roasting""")
    return [el[0] for el in res]


def get_consistency_value():
    res = cursor.execute("""SELECT consistency_type FROM consistency""")
    return [el[0] for el in res]


def insert_coffee(sort_name, roast, consistency, taste_description, price, coffee_amount):
    try:
        cursor.execute("""INSERT INTO coffee_info(sort_name, roast, consistency, taste_description, 
                        price, coffee_amount)
                        VALUES(?, (SELECT roast_id FROM roasting WHERE roast-type = ?),
                        (SELECT id FROM consistecy WHERE consistecy_type = ?), ?, ?, ?)""",
                       (sort_name, roast, consistency, taste_description, price, coffee_amount))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
