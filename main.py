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
      <item row="1" column="0" colspan="2">
       <widget class="QTableWidget" name="table"/>
      </item>
      <item row="0" column="0" colspan="2">
       <widget class="QPushButton" name="addbutton">
        <property name="text">
         <string>Добавить</string>
        </property>
       </widget>
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
ADD_WIND_UI = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <layout class="QGridLayout" name="gridLayout_2">
   <item row="0" column="0">
    <layout class="QGridLayout" name="gridLayout">
     <item row="4" column="0">
      <widget class="QLabel" name="label_3">
       <property name="text">
        <string>молотый/в зернах</string>
       </property>
      </widget>
     </item>
     <item row="6" column="0">
      <widget class="QLabel" name="label_4">
       <property name="text">
        <string>описание вкуса</string>
       </property>
      </widget>
     </item>
     <item row="8" column="0">
      <widget class="QLabel" name="label_5">
       <property name="text">
        <string>цена</string>
       </property>
      </widget>
     </item>
     <item row="10" column="0">
      <widget class="QLabel" name="label_6">
       <property name="text">
        <string>объем упаковки</string>
       </property>
      </widget>
     </item>
     <item row="3" column="0">
      <widget class="QLineEdit" name="degree_of_roasting_lineEdit"/>
     </item>
     <item row="11" column="0">
      <widget class="QLineEdit" name="volume_lineEdit"/>
     </item>
     <item row="5" column="0">
      <widget class="QLineEdit" name="ground_or_beans_lineEdit"/>
     </item>
     <item row="9" column="0">
      <widget class="QLineEdit" name="price_lineEdit"/>
     </item>
     <item row="0" column="0">
      <widget class="QLabel" name="label">
       <property name="text">
        <string>название сорта</string>
       </property>
      </widget>
     </item>
     <item row="2" column="0">
      <widget class="QLabel" name="label_2">
       <property name="text">
        <string>степень обжарки</string>
       </property>
      </widget>
     </item>
     <item row="1" column="0">
      <widget class="QLineEdit" name="name_lineEdit"/>
     </item>
     <item row="7" column="0">
      <widget class="QLineEdit" name="description_of_taste_lineEdit"/>
     </item>
     <item row="12" column="0">
      <widget class="QPushButton" name="pushButton_add_coffee">
       <property name="text">
        <string>Добавить</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
  </layout>
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

        self.addbutton.clicked.connect(self.open_add_wind)

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
            pass

        if not self.result:
            self.table.setColumnCount(7)
            self.table.setRowCount(1)
        else:
            for i in self.result:
                i = self.result.index(i) + 1
            self.table.setRowCount(len(self.result))
            self.table.setColumnCount(len(self.result[0]))

        self.table.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                              'описание вкуса', 'цена', 'объем упаковки',
                                              'Редактировать', 'Удалить'])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        for i in range(len(self.result)):
            for j in range(len(self.result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))
    def open_add_wind(self):
        self.add_wind = AddCoffeeWindow()
        self.add_wind.show()


class AddCoffeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(ADD_WIND_UI), self)

        self.pushButton_add_coffee.clicked.connect(self.add_coffee)

    def add_coffee(self):
        self.result = ex.cur.execute(f"""
        SELECT * FROM coffee_base""").fetchall()
        coffee_id = len(self.result) + 1
        ex.cur.execute(f"""
        INSERT INTO coffee_base
        VALUES ({coffee_id}, {self.name_lineEdit.text()}, {self.degree_of_roasting_lineEdit.text()},
        {self.ground_or_beans_lineEdit.text()}, {self.description_of_taste_lineEdit.text()},
        {self.price_lineEdit.text()}, {self.volume_lineEdit.text()})""",)
        self.close()
        ex.update_table()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SteamPortfolio()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
