from tkinter import *  # (TO-DO) import what's needed

from PyQt5.QtWidgets import *  # (TO-DO) import what's needed
from PyQt5.QtGui import *  # (TO-DO) import what's needed
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication


from tkinter import messagebox
from datetime import date
import os
import sqlite3
import sys


class Arrange(QWidget):
    def __init__(self, ):
        super().__init__()

    def labels(self, place, list_with_names, step_down):
        start = 0
        stop = len(list_with_names)
        step = 30
        labels_gc = []
        while start != stop:
            label_name = QLabel(list_with_names[start], place)
            label_name.move(10, step)
            labels_gc.append(label_name)
            start += 1
            step += step_down
            label_name.show()

    def comboboxes(self, place, list_with_types):
        labels_gc2 = []
        combo = QComboBox(place)
        combo.addItems(list_with_types)
        combo.move(100, 60)
        combo.show()
        self.type_is = str(combo.currentText())
        labels_gc2.append(combo)

    def entries_for_rb(self, place, step_down, total):
        start_entry_cmbbox = QLineEdit(place)
        start_entry_cmbbox.move(100, 30)
        start_entry_cmbbox.show()



        start = 0
        step = 90
        labels_gc3 = []
        self.list_entries_for_rb = []
        self.list_entries_for_rb.append(self.start_entry_cmbbox)
        while start != total:
            self.entry_cmbbox = QLineEdit(place)
            self.entry_cmbbox.move(100, step)
            self.entry_cmbbox.show()
            self.list_entries_for_rb.append(self.entry_cmbbox)
            labels_gc3.append(self.entry_cmbbox)
            start += 1
            step += step_down

    def entries(self):
        print('ok')


class AddingMode(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 600, 700)
        self.setWindowTitle('Add name of organization and # of agreement. Part 1')


        admode_pt1_labels = ['Name', 'Type', 'Date', 'Agreement', 'Agr. date']
        admode_pt1_cmbbox = ['Organization', 'Entrepreneur']
        arr = Arrange()
        arr.labels(place=self, list_with_names=admode_pt1_labels, step_down=30)
        arr.comboboxes(place=self, list_with_types=admode_pt1_cmbbox)

        self.btn1 = QPushButton("Button 1", self)
        self.btn1.move(200, 200)
        self.btn1.clicked.connect(self.collect)

        # creditLine_btn = Button(text='Save and next step', height=1, width=20, command=self.collect)
        # creditLine_btn.place(relx=.12, rely=.40, height=30, width=130)
        # self.insert_current_date(self)
        # self.make_db()
        self.show()


    def collect(self):
        arr = Arrange()
        c = arr.type_is
        print(c)


if __name__ == "__main__":
    AdMode_pt1 = QApplication(sys.argv)
    test = AddingMode()
    sys.exit(AdMode_pt1.exec_())


