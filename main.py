from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        conn = sqlite3.connect('coffee.sqlite')
        self.cursor = conn.cursor()
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.sqlite')
        self.db.open()
        self.table_view(self.tableView)
        self.tableView.setColumnHidden(6, True)
        
    def table_view(self, view):
        model = QSqlTableModel(self, self.db)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
