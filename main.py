import sys
import io
import sqlite3
import csv

from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QButtonGroup
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5 import uic, QtWidgets

MAIN_UI = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout_2">
    <item row="0" column="0">
     <layout class="QGridLayout" name="gridLayout">
      <item row="0" column="0" colspan="2">
       <widget class="QTableWidget" name="table"/>
      </item>
     </layout>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class SteamPortfolio(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(MAIN_UI), self)

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.result = []
        self.initUI()

    def initUI(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS coffee_base(
                           id INTEGER,
                           name TEXT,
                           degree_of_roasting TEXT,
                           ground_or_beans TEXT,
                           description_of_taste TEXT,
                           price TEXT,
                           volume TEXT);
                           """)
        self.con.commit()
        self.update_table()

    def update_table(self):
        try:
            self.result = self.cur.execute(f"""
            SELECT * FROM coffee_base""").fetchall()
            self.result = [list(item) for item in self.result]
        except sqlite3.OperationalError:
            print('ошибка')

        if not self.result:
            self.table.setColumnCount(7)
            self.table.setRowCount(1)
        else:
            self.table.setRowCount(len(self.result))
            self.table.setColumnCount(len(self.result[0]))

        self.table.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                              'описание вкуса', 'цена', 'объем упаковки'])

        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        for i in range(len(self.result)):
            for j in range(len(self.result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SteamPortfolio()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
