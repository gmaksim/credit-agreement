from tkinter import *  # (TO-DO) import what's needed

from PyQt5.QtWidgets import *  # (TO-DO) import what's needed
from PyQt5.QtGui import *  # (TO-DO) import what's needed
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

import os
import sqlite3
import sys


class AddingMode(QWidget):
    def __init__(self, ):
        super().__init__()
        self.data_from_entr = []
        self.start_adding()

    def arrange_labels(self, place, list_with_names, step_down):
        start = 0
        step = 1
        while start != len(list_with_names):
            label_name = QLabel(list_with_names[start])
            place.addWidget(label_name, step, 0)
            start += 1
            step += step_down

    def arrange_comboboxes(self, place, list_with_types):
        self.combo = QComboBox()
        self.combo.addItems(list_with_types)
        place.addWidget(self.combo, 2, 1)

    def arrange_entries_for_comboboxes(self, place, column, step_down, total):
        entry_start = QLineEdit()
        place.addWidget(entry_start, 1, 1)
        self.data_from_entr.append(entry_start)

        start = 0
        step = 3
        while start != total:
            entry = QLineEdit()
            place.addWidget(entry, step, column)
            self.data_from_entr.append(entry)
            start += 1
            step += step_down

    def arrange_entries(self):
        print('later')

    @staticmethod
    def create_db_and_tables():
        b = os.path.exists('DATA')
        if b is False:
            os.mkdir('DATA')
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute(  # (TO-DO) change to executescript
                'CREATE TABLE NameAgreement (id integer PRIMARY KEY, Name text NULL, Type text NULL, Date text NULL, '
                'Agreement text NULL, AgrDate text NULL, idSend integer NULL)')
            cursor.execute(
                'CREATE TABLE DocumAgreem (id integer PRIMARY KEY, Adjudications text NULL, Application text NULL, '
                'ApprovalTran text NULL, ConsentSpou text NULL, ExtractUSRLE text NULL, ListParShare text NULL, '
                'MainContract text NULL, OfficialCorr text NULL, Questionnaire text NULL, RussianPassp text NULL, '
                'idSend integer NULL)')
            conn.close()

    def get_sendid_from_db(self, table_name):
        table_name = 'SELECT idSend FROM ' + table_name  # (TO-DO) son drop table, remake!
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()
        cursor.execute(table_name)
        number_id_res = cursor.fetchone()

        if number_id_res is None:
            id_send = 1
        else:
            cursor.execute(table_name)
            numbers_id_res = cursor.fetchall()
            max_numbers = str(max(numbers_id_res))  # take max number of idSend, convert to str type to possible cut
            id_send = int(max_numbers[1:-2]) + 1  # cut '(,)' around number, convert to int and plus one

        conn.close()
        return id_send

    def start_adding(self):
        layout = QGridLayout()
        self.setLayout(layout)
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('AddingMode (Part 1 of 4)')

        self.label_start = QLabel('Add name of organization and # of agreement')
        layout.addWidget(self.label_start, 0, 1)

        self.admode_pt1_labels = ['Name', 'Type', 'Date', 'Agreement', 'Agr. date']
        self.admode_pt1_cmbbox = ['Organization', 'Entrepreneur']
        self.arrange_labels(place=layout, list_with_names=self.admode_pt1_labels, step_down=1)
        self.arrange_entries_for_comboboxes(place=layout, column=1, step_down=1, total=3)
        self.arrange_comboboxes(place=layout, list_with_types=self.admode_pt1_cmbbox)

        def run():  # run function by button with param.
            self.save_info_to_db_with_comboboxes(table='NameAgreement')
        self.butt = QPushButton(text='Save and next step')
        self.butt.clicked.connect(run)
        self.table = 'NameAgreement'
        layout.addWidget(self.butt, 6, 1)

        self.create_db_and_tables()
        self.show()

    def collect_data_with_comboboxes(self):
        collected_combbox = str(self.combo.currentText())

        self.collected_data = []
        for i in self.data_from_entr:
            to_append = (i.text())
            self.collected_data.append(to_append)

        self.collected_data.insert(1, collected_combbox)
        return self.collected_data

    def save_info_to_db_with_comboboxes(self, table):
        last_number_id_res = self.get_sendid_from_db(table_name=table)
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        data_to_insert = self.collect_data_with_comboboxes()
        print(data_to_insert[3])
        print(data_to_insert)
        print(last_number_id_res)



        # table_name = 'SELECT idSend FROM ' + self.table  # (TO-DO) son drop table, remake!
        # conn = sqlite3.connect('DATA//firstBase.sqlite')
        # cursor = conn.cursor()
        # cursor.execute(table_name)
        #
        #
        # cursor.execute()
        # cursor.execute('INSERT INTO ANAME (Name, Date, Type, idSend) VALUES (?, ?, ?, ?)',
        #                (credit_line_name_imp, credit_line_date_imp, self.credit_line_name_type, last_number_id_res))
        # cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
        #                (credit_line_agreement_imp, credit_line_agrdate_imp, last_number_id_res))

        conn.commit()
        conn.close()



if __name__ == "__main__":
    AdMode_pt1 = QApplication(sys.argv)
    run = AddingMode()
    sys.exit(AdMode_pt1.exec_())


