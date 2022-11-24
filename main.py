from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from db_funcs import table_view, insert_coffee, get_roast_value, get_consistency_value
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        table_view(self, self.tableView)
        self.tableView.setColumnHidden(6, True)
        self.add_btn.clicked.connect(self.btn_clicked)
        self.edit_btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        if self.sender().text() == 'Добавить запись':
            status = True
            dialog = AddEditCoffeeForm(status, self)
            dialog.exec_()
        elif self.sender().text() == 'Редактировать запись':
            status = False
            dialog = AddEditCoffeeForm(status, self)
            dialog.exec_()


class AddEditCoffeeForm(QDialog):
    def __init__(self, status, parent=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.status = status
        if self.status:
            self.roasting_cb.addItems(get_roast_value())
            self.consist_cb.addItems(get_consistency_value())
            self.ok_pB.clicked.connect(self.add_coffee)
        else:
            self.ok_pB.clicked.connect(self.edit_coffee)
        self.cancel_pB.clicked.connect(self.cancel_btn)

    def add_coffee(self):
        pass

    def edit_coffee(self):
        pass

    def cancel_btn(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
