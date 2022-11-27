from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from db_funcs import (table_view, insert_coffee, get_roast_value, get_consistency_value, get_item_value, update_coffee)
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
            status = 'add_status'
            dialog = AddEditCoffeeForm(status, self)
            dialog.exec_()
            table_view(self, self.tableView)
        elif self.sender().text() == 'Редактировать запись':
            status = 'edit_status'
            row = self.tableView.currentIndex().row()
            if row != -1:
                coffee_id = self.tableView.model().index(row, 6).data()
                dialog = AddEditCoffeeForm(status, self, get_item_value(coffee_id))
                dialog.exec_()
                table_view(self, self.tableView)


class AddEditCoffeeForm(QDialog):
    def __init__(self, status, parent=None, *characteristics):
        super(AddEditCoffeeForm, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.status = status

        if self.status == 'add_status':
            self.roasting_cb.addItems(get_roast_value())
            self.consist_cb.addItems(get_consistency_value())
            self.ok_pB.clicked.connect(self.add_coffee)

        elif self.status == 'edit_status':
            self.characteristics = characteristics[0]  # Coffee characteristics list [sort_name, roast, consistency,
            # taste_description, price, coffee_amount, id]
            self.sort_name_lE.setText(str(self.characteristics[0]))
            self.taste_lE.setText(str(self.characteristics[3]))
            self.price_lE.setText(str(self.characteristics[4]))
            self.amount_lE.setText(str(self.characteristics[5]))

            self.roasting_cb.addItems(get_roast_value())
            self.roasting_cb.setCurrentText(self.characteristics[1])

            self.consist_cb.addItems(get_consistency_value())
            self.consist_cb.setCurrentText(self.characteristics[2])

            self.ok_pB.clicked.connect(self.edit_coffee)
        self.cancel_pB.clicked.connect(self.cancel_btn)

    def add_coffee(self):
        try:
            sort_name, roast, consistency, taste_description, price, coffee_amount = \
                self.sort_name_lE.text(), self.roasting_cb.currentText(), self.consist_cb.currentText(), \
                self.taste_lE.text(), int(self.price_lE.text()), int(self.amount_lE.text())

            if insert_coffee(sort_name, roast, consistency, taste_description, price, coffee_amount):
                self.close()
            else:
                self.statusBar.setText('Поля заполнены не полностью')

        except ValueError:
            self.statusBar.setText('Поля заполнены неверно')

    def edit_coffee(self):
        try:
            sort_name, roast, consistency, taste_description, price, coffee_amount = \
                self.sort_name_lE.text(), self.roasting_cb.currentText(), self.consist_cb.currentText(), \
                self.taste_lE.text(), int(self.price_lE.text()), int(self.amount_lE.text())

            if update_coffee(sort_name, roast, consistency, taste_description, price, coffee_amount,
                             self.characteristics[6]):
                self.close()
            else:
                self.statusBar.setText('Поля заполнены не полностью')

        except ValueError:
            self.statusBar.setText('Поля заполнены неверно')

    def cancel_btn(self):
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
