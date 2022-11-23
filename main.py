from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import sys
import sqlite3


class MainWindow(QApplication):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        conn = sqlite3.connect('coffee.sqlite')
        self.cursor = conn.cursor()
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('coffee.sqlite')
        self.db.open()
        self.table_view(self.tableView)
        
    def table_view(self, view):
        model = QSqlTableModel(self, self.db)
        model.setQuery(QSqlQuery(""""""))
        
        model.select()
        view.setModel(model)
        view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
