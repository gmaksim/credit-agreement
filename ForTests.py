# #! temp .py file to check some part of code
from tkinter import *  # (TO-DO) import what's needed

from PyQt5.QtWidgets import *  # (TO-DO) import what's needed
from PyQt5.QtGui import *  # (TO-DO) import what's needed

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
        list_entries_for_rb = []
        list_entries_for_rb.append(start_entry_cmbbox)
        while start != total:
            entry_cmbbox = QLineEdit(place)
            entry_cmbbox.move(100, step)
            entry_cmbbox.show()
            list_entries_for_rb.append(entry_cmbbox)
            labels_gc3.append(entry_cmbbox)
            start += 1
            step += step_down
        return list_entries_for_rb

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
        print(arr.type_is)

        self.test = arr.entries_for_rb(place=self, step_down=30, total=3)

        btn1 = QPushButton("Button 1", self)
        btn1.move(200, 200)


        # creditLine_btn = Button(text='Save and next step', height=1, width=20, command=self.collect)
        # creditLine_btn.place(relx=.12, rely=.40, height=30, width=130)

        # self.insert_current_date(self)
        # self.make_db()
        self.show()

    def collect(self):

        list_attr_list =[]
        for attr in self.test:
            to_append = (attr.get())
            list_attr_list.append(to_append)
        print(list_attr_list)


if __name__ == "__main__":
    AdMode_pt1 = QApplication(sys.argv)
    something = AddingMode()
    sys.exit(AdMode_pt1.exec_())


