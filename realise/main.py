import sys
import io
import sqlite3
import csv

from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QButtonGroup
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5 import uic, QtWidgets
from main_ui import *
from edit_window import *
from add_window import *


class CoffeBase(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.con = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.con.cursor()

        self.button_group_del = QButtonGroup(self)
        self.button_group_edit = QButtonGroup(self)

        self.result = []
        self.initUI()

        self.addbutton.clicked.connect(self.open_add_wind)
        self.button_group_del.buttonClicked.connect(self.remove_row)
        self.button_group_edit.buttonClicked.connect(self.edit_row)

    def initUI(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS coffee_base(
                           id INTEGER,
                           name TEXT,
                           degree_of_roasting TEXT,
                           ground_or_beans TEXT,
                           description_of_taste TEXT,
                           price TEXT,
                           volume TEXT,
                           edit TEXT,
                           delite TEXT);
                           """)
        self.con.commit()
        self.update_table()

    def update_table(self):
        try:
            self.result = self.cur.execute(f"""
            SELECT * FROM coffee_base""").fetchall()
            self.result = [list(item) for item in self.result]
        except sqlite3.OperationalError:
            pass

        if not self.result:
            self.table.setColumnCount(7)
            self.table.setRowCount(1)
        else:
            for i in range(len(self.result)):
                self.result[i][0] = self.result.index(self.result[i]) + 1
            self.table.setRowCount(len(self.result))
            self.table.setColumnCount(len(self.result[0]))

        self.table.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                              'описание вкуса', 'цена', 'объем упаковки',
                                              'Редактировать', 'Удалить'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        if not self.result:
            for i in range(1):
                for j in range(9):
                    self.table.setItem(i, j, QTableWidgetItem(''))
        else:
            for i in range(len(self.result)):
                for j in range(len(self.result[0])):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))

                but_del = QtWidgets.QPushButton(self)
                self.table.setCellWidget(i, 8, but_del)
                but_del.setText('Удалить')
                self.button_group_del.addButton(but_del)

                but_edit = QtWidgets.QPushButton(self)
                self.table.setCellWidget(i, 7, but_edit)
                but_edit.setText('Редактировать')
                self.button_group_edit.addButton(but_edit)

    def remove_row(self, pressed_btn):
        index = self.button_group_del.buttons().index(pressed_btn)

        self.cur.execute(f"""DELETE FROM coffee_base
        WHERE name = ? AND
        degree_of_roasting = ? AND
        ground_or_beans = ? AND
        description_of_taste = ? AND
        price = ? AND
        volume = ?
        """, (self.table.item(index, 1).text(),
              self.table.item(index, 2).text(),
              self.table.item(index, 3).text(),
              self.table.item(index, 4).text(),
              self.table.item(index, 5).text(),
              self.table.item(index, 6).text()))

        self.con.commit()
        self.update_table()

    def edit_row(self, pressed_btn):
        index_row = self.button_group_edit.buttons().index(pressed_btn)
        self.edit_window = EditCoffeeInfo(index_row)
        self.edit_window.show()

    def open_add_wind(self):
        self.add_wind = AddCoffeeWindow()
        self.add_wind.show()


class EditCoffeeInfo(QWidget, Ui_Form1):
    def __init__(self, index):
        super().__init__()
        self.setupUi(self)
        self.save_pushButton.clicked.connect(self.edit)
        self.index = index

    def edit(self):
        ex.cur.execute(f"""UPDATE coffee_base
                    SET name = ?, 
                    degree_of_roasting = ?,
                    ground_or_beans = ?,
                    description_of_taste = ?,
                    price = ?,
                    volume = ?
                    
                    WHERE name = ? AND
                    degree_of_roasting = ? AND
                    ground_or_beans = ? AND
                    description_of_taste = ? AND
                    price = ? AND
                    volume = ?
                    """, (self.name_lineEdit.text(), self.degree_of_roasting_lineEdit.text(),
                          self.ground_or_beans_lineEdit.text(), self.description_of_taste_lineEdit.text(),
                          self.price_lineEdit.text(), self.volume_lineEdit.text(),
                          ex.table.item(self.index, 1).text(),
                          ex.table.item(self.index, 2).text(),
                          ex.table.item(self.index, 3).text(),
                          ex.table.item(self.index, 4).text(),
                          ex.table.item(self.index, 5).text(),
                          ex.table.item(self.index, 6).text()))

        ex.con.commit()
        ex.update_table()
        self.close()


class AddCoffeeWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_add_coffee.clicked.connect(self.add_coffee)

    def add_coffee(self):
        self.result = ex.cur.execute(f"""
        SELECT * FROM coffee_base""").fetchall()
        coffee_id = len(self.result) + 1

        itog_info = (coffee_id, self.name_lineEdit.text(), self.degree_of_roasting_lineEdit.text(),
                     self.ground_or_beans_lineEdit.text(), self.description_of_taste_lineEdit.text(),
                     self.price_lineEdit.text(), self.volume_lineEdit.text(), 'edit', 'del')

        ex.cur.execute(f"""
        INSERT INTO coffee_base
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", itog_info)

        ex.con.commit()
        self.close()
        ex.update_table()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeBase()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
