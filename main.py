from PyQt5.QtWidgets import \
    (QWidget, QPushButton, QApplication, QLabel, QComboBox, QLineEdit, QGridLayout, QMessageBox, QSizePolicy)
import os
import sqlite3
import sys


class AddingMode(QWidget):
    def __init__(self):
        super().__init__()

        self.create_db_and_tables()
        self.last_number_id_res = self.get_sendid_from_db(table_name='NameAgreement')
        self.agree_global = 'none_dirs'  # to know with which agreement we work
        self.gp_global = 'none dirs'

        # Start block
        self.folders_org = ('Adjudications', 'Application', 'Approval of the transaction', 'Extract USRLE',
                            'List of participants or shareholders register', 'Main contract',
                            'Official correspondence', 'Questionnaire')
        self.folders_entr = ('Adjudications', 'Application', 'Consent of the spouse', 'Main contract',
                             'Official correspondence', 'Questionnaire', 'Russian passport')
        self.checking_files_done = None

        # GuPl block
        self.folders_gp_org = ('Adjudications', 'Approval of the transaction', 'Consent to the encumbrance',
                               'Extract USRLE', 'Official correspondence', 'Questionnaire',
                               'Surety agreement OR pledge')
        self.folders_gp_entr = ('Adjudications', 'Consent to the encumbrance', 'Official correspondence',
                                'Questionnaire', 'Russian passport', 'Surety agreement OR pledge')

        # GrpObj block
        self.folder_grp_obj = ('Certificate of ownership', 'Contract of sale', 'Extract USRRE')

        # Start block
        self.Adjudications = ('Plaintiff', 'Respondent', 'Third parties', 'Case number', 'Instance')
        self.Application = ('Profile Date',)
        self.ApprovalTran = ('meeting Date', 'participants of the meeting', 'Chairman of meeting', 'Secretary')
        self.ConsentSpou = ('Date',)
        self.ExtractUSRLE = ('date of issue', 'director', 'members of society')
        self.ListParShare = ('list Date', 'Member №1', 'member share №1', 'Member №2', 'member share №2')
        self.MainContract = ('The lender / guarantor', 'Borrower / Principal', 'beneficiary', 'contract number',
                             'Date of contract', 'The amount of the transaction', 'Contract fee Period',
                             'Signatory of the Creditor', 'Signatory of the Borrower')
        self.OfficialCorr = ('Sender', 'Destination', 'Outgoing №', 'Date Outgoing №', 'Incoming №', 'Date Incoming №')
        self.Questionnaire = ('Profile Date',)
        self.RussianPassp = ('Number',)
        self.sum_org_attr = (self.Adjudications + self.Application + self.ApprovalTran + self.ExtractUSRLE +
                             self.ListParShare + self.MainContract + self.OfficialCorr + self.Questionnaire)
        self.sum_entr_attr = (self.Adjudications + self.Application + self.ConsentSpou + self.MainContract +
                              self.OfficialCorr + self.Questionnaire + self.RussianPassp)
        self.len_attrib = []
        self.data_from_attrib = []

        # GuPl block
        self.ConsEncumb = ('Date of approval', 'Address of the object', 'Cadastral (or conditional) number',
                           'type of encumbrances', 'term of agreement')
        self.SuretAgrPledg = ('agreement date', 'The lender / guarantor', 'Guarantor / Pledgor', 'term maintenance',
                              'Reg.number account on mortgage')

        self.sum_gp_org_attr = (self.Adjudications + self.ApprovalTran + self.ConsentSpou + self.ExtractUSRLE
                                + self.OfficialCorr + self.Questionnaire + self.SuretAgrPledg)
        self.sum_gp_entr_attr = (self.Adjudications + self.ConsentSpou + self.OfficialCorr + self.Questionnaire
                                 + self.RussianPassp + self.SuretAgrPledg)
        self.arr_attr_start_or_pg = '0'

        self.pt1_start_adding()

    def arrange_labels(self, place, list_with_names, step_down):
        start = 0
        step = 1
        while start != len(list_with_names):
            label_name = QLabel(list_with_names[start])
            place.addWidget(label_name, step, 0)
            start += 1
            step += step_down

    def arrange_comboboxes(self, place, list_with_types, list_with_types_2):
        self.combo = QComboBox()
        self.combo.addItems(list_with_types)
        place.addWidget(self.combo, 2, 1)

        if list_with_types_2 != 0:
            self.combo2 = QComboBox()
            self.combo2.addItems(list_with_types_2)
            place.addWidget(self.combo2, 3, 1)

    def arrange_entries_for_comboboxes(self, place, column, step_down, total):
        self.data_from_entr = []
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

    def arrange_color_labels(self, place, total):
        start = 0
        step = 1
        while start != total:
            label_name = QLabel()
            label_name.setStyleSheet('background-color: #f2ecec')
            place.addWidget(label_name, step, 1)
            start += 1
            step += 2

    def arrange_attributes(self, place, step_down, list_with_words):
        def receive_list_with_len_attributes():  # (TO-DO) make flexible func
            self.len_attrib = []
            if self.type_is == 'Organization':
                self.len_attrib.append(len(self.Adjudications))  # Aou
                self.len_attrib.append(len(self.Application))  # Aou
                self.len_attrib.append(len(self.ApprovalTran))  # o
                self.len_attrib.append(len(self.ExtractUSRLE))  # o
                self.len_attrib.append(len(self.ListParShare))  # o
                self.len_attrib.append(len(self.MainContract))  # Aou
                self.len_attrib.append(len(self.OfficialCorr))  # Aou
                self.len_attrib.append(len(self.Questionnaire))  # Aou
            else:
                self.len_attrib.append(len(self.Adjudications))  # Aou
                self.len_attrib.append(len(self.Application))  # Aou
                self.len_attrib.append(len(self.ConsentSpou))  # U
                self.len_attrib.append(len(self.MainContract))  # Aou
                self.len_attrib.append(len(self.OfficialCorr))  # Aou
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.RussianPassp))  # U
            return self.len_attrib

        def receive_list_with_len_attributes_pg():
            self.len_attrib = []
            if self.type_is == 'Organization':
                self.len_attrib.append(len(self.Adjudications))  # Aou
                self.len_attrib.append(len(self.ApprovalTran))  # o
                self.len_attrib.append(len(self.ConsentSpou))  # o
                self.len_attrib.append(len(self.ExtractUSRLE))  # o
                self.len_attrib.append(len(self.OfficialCorr))  # Aou
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.SuretAgrPledg))  # Aou
            else:
                self.len_attrib.append(len(self.Adjudications))  # Aou
                self.len_attrib.append(len(self.ConsentSpou))  # Aou
                self.len_attrib.append(len(self.OfficialCorr))  # U
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.RussianPassp))  # Aou
                self.len_attrib.append(len(self.SuretAgrPledg))  # Aou
            return self.len_attrib

        self.attribute_len_list = receive_list_with_len_attributes()

        if self.arr_attr_start_or_pg == 1:
            self.attribute_len_list = receive_list_with_len_attributes_pg()


        print(self.arr_attr_start_or_pg)
        print(self.attribute_len_list)

        word = 0
        step = 2
        for i in self.attribute_len_list:  # i = quantity of needed labels
            start = 0
            offset = 0
            while start != i:
                entry = QLineEdit(list_with_words[word])
                place.addWidget(entry, step, offset)
                self.data_from_attrib.append(entry)
                start += 1
                offset += 1
                word += 1
            step += step_down

    def clear_gui(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

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
            cursor.execute(
                'CREATE TABLE PledGuar (id integer PRIMARY KEY, Name text NULL, Type text NULL, Type2 text NULL, '
                'Date text NULL, idSend integer NULL)')
            cursor.execute(
                'CREATE TABLE DocumGuPl (id integer PRIMARY KEY, Adjudications text NULL, ApprovalTran text NULL, '
                'ConsentSpou text NULL, ExtractUSRLE text NULL, OfficialCorr text NULL, Questionnaire text NULL, '
                'RussianPassp text NULL, SuretAgrPledg text NULL, idSend integer NULL)')
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

    def collect_data_with_comboboxes(self):
        collected_combbox = str(self.combo.currentText())
        self.collected_data = []

        for i in self.data_from_entr:
            to_append = (i.text())
            self.collected_data.append(to_append)
        self.collected_data.insert(1, collected_combbox)

        # take data with 2 cmbbxs
        try:
            collected_combbox_2 = str(self.combo2.currentText())
            if collected_combbox_2 == '':
                pass
            else:
                self.collected_data.insert(2, collected_combbox_2)
                self.collected_data.pop(3)
        except AttributeError:
            pass

        return self.collected_data

    def collect_data(self):
        self.collected_data_attributes = []
        for i in self.data_from_attrib:
            to_append = (i.text())
            self.collected_data_attributes.append(to_append)
        return self.collected_data_attributes

    def check_files_in_folder(self):  # (TO-DO) try to make it simple
        file_exists = []
        dirs_without_docs = []
        work_dir = os.getcwd()
        z = 0
        all_dirs_list = os.listdir()
        len_dirs = len(all_dirs_list)
        while z != len_dirs:
            curr_dir = all_dirs_list[z]
            os.chdir(curr_dir)
            file_in_folder = os.listdir()
            if file_in_folder == []:
                file_exists.append('#7d0541')  # no
                dirs_without_docs.append(curr_dir)
            else:
                file_exists.append('#00ff7d')  # yes
            os.chdir(work_dir)
            z += 1

        # make colour of labels (y/n file in folder) by info in []
        def count():  # static count
            try:
                count.a += 1
            except AttributeError:
                count.a = 0
            return count.a

        def make_color():
            curr_color = file_exists[count()]
            final_color = 'background-color: ' + curr_color
            return final_color

        start = 0
        step = 1
        while start != self.len_folder:
            label_name = QLabel()
            label_name.setStyleSheet(make_color())
            self.layout.addWidget(label_name, step, 1)
            start += 1
            step += 2

        # check for start add_attribute func
        null_documents = ['Adjudications', 'Official correspondence', 'Consent to the encumbrance']
        for q in null_documents:
            for i in dirs_without_docs:
                if i == q:
                    c = dirs_without_docs.index(q)
                    dirs_without_docs.pop(c)
        if dirs_without_docs == []:
            self.checking_files_done = True
        else:
            QMessageBox.information(self, 'Information', 'Please add files')
            self.checking_files_done = False

        return self.checking_files_done

    # TEST
    def pt1_start_adding(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('AddingMode (Part 1 of 4)')

        self.label_start = QLabel('Add name of organization and # of agreement')
        self.layout.addWidget(self.label_start, 0, 1)

        admode_pt1_labels = ['Name', 'Type', 'Date', 'Agreement', 'Agr. date']
        admode_pt1_cmbbox = ['Organization', 'Entrepreneur']
        self.arrange_labels(place=self.layout, list_with_names=admode_pt1_labels, step_down=1)
        self.arrange_entries_for_comboboxes(place=self.layout, column=1, step_down=1, total=3)  # (TO-DO) insert date
        self.arrange_comboboxes(place=self.layout, list_with_types=admode_pt1_cmbbox, list_with_types_2=0)

        def check_data():
            data_to_insert = self.collect_data_with_comboboxes()
            if data_to_insert[0] == '':
                QMessageBox.warning(self, 'Warning', 'Please add name')
            elif data_to_insert[3] == '':
                QMessageBox.warning(self, 'Warning', 'Please add agreement')
            else:
                commit_info_to_db()  # (TO-DO) check for folders exists
        def commit_info_to_db():  # run function by button with param.
            data_to_insert = self.collect_data_with_comboboxes()
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))  # change to main folder for connect DB
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO NameAgreement (Name, Type, Date, Agreement, AgrDate, idSend) '
                           'VALUES (?, ?, ?, ?, ?, ?)',
                           (data_to_insert[0], data_to_insert[1], data_to_insert[2],
                            data_to_insert[3], data_to_insert[4], self.last_number_id_res))
            conn.commit()
            conn.close()
            self.pt2_put_files()
        self.butt = QPushButton(text='Save and next step')
        self.butt.clicked.connect(check_data)
        # self.butt.clicked.connect(self.pt5_optional_adding_groups_obj)  # TEST
        self.layout.addWidget(self.butt, 6, 1)

        self.show()

    def pt2_put_files(self):
        data_to_insert = self.collect_data_with_comboboxes()

        def make_clients_folders():
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

            a = os.path.exists('CLIENTS')
            if a is False:
                os.mkdir('CLIENTS')
            os.chdir('CLIENTS')

            b = os.path.exists(data_to_insert[0])
            if b is False:
                q = data_to_insert[0] + '//' + data_to_insert[3]
                self.agree_global = 'CLIENTS//' + q
                os.makedirs(q)
                os.chdir(q)

                if data_to_insert[1] == 'Organization':
                    folders = self.folders_org
                else:
                    folders = self.folders_entr
                z = 0
                d = len(folders)
                while z != d:
                    folder = folders[z]
                    os.mkdir(folder)
                    z += 1
        make_clients_folders()

        self.clear_gui()

        self.label_start = QLabel('Put files in folders')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('AddingMode (Part 2 of 4)')

        self.len_folder = 0
        self.type_is = 'None'
        if data_to_insert[1] == 'Organization':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_org, step_down=2)
            self.len_folder = len(self.folders_org)
            self.type_is = 'Organization'
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_entr, step_down=2)
            self.len_folder = len(self.folders_entr)
            self.type_is = 'Entrepreneur'

        self.arrange_color_labels(place=self.layout, total=self.len_folder)

        def add_attribute_or_no():
            result = self.check_files_in_folder()
            if result is True:
                self.pt2_adding_attributes_for_files()
        self.butt = QPushButton(text='Check files in folder')
        self.butt.clicked.connect(add_attribute_or_no)
        self.layout.addWidget(self.butt, 17, 1)

    def pt2_adding_attributes_for_files(self):
        self.clear_gui()

        self.label_start = QLabel('Add attributes for documents')
        self.layout.addWidget(self.label_start, 0, 0)
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('AddingMode (Part 2 of 4)')

        if self.type_is == 'Organization':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_org, step_down=2)
            words = self.sum_org_attr
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_entr, step_down=2)
            words = self.sum_entr_attr

        self.arrange_attributes(place=self.layout, step_down=2, list_with_words=words)

        def commit_info_pt2_to_db():
            list_with_attributes = self.collect_data()

            # prepare to insert data (separate by column)
            separate_list_with_attributes = []
            start = 0
            stop = 0
            for item in self.attribute_len_list:
                stop += item
                separate_list_with_attributes.append(list_with_attributes[start:stop])
                start += item

            # insert info in DB
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            if self.type_is == 'Organization':  # (TO-DO) do it shorter
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                g = str(separate_list_with_attributes[6])
                h = str(separate_list_with_attributes[7])
                cursor.execute(
                    'INSERT INTO DocumAgreem (Adjudications, Application, ApprovalTran, ExtractUSRLE, ListParShare, '
                    'MainContract, OfficialCorr, Questionnaire, idSend) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (a, b, c, d, e, f, g, h, self.last_number_id_res))
            else:
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                g = str(separate_list_with_attributes[6])
                cursor.execute(
                    'INSERT INTO DocumAgreem (Adjudications, Application, ConsentSpou, MainContract, OfficialCorr, '
                    'Questionnaire, RussianPassp, idSend) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (a, b, c, d, e, f, g, self.last_number_id_res))
            conn.commit()
            conn.close()
            self.pt3_adding_guar_pled()
        self.butt = QPushButton(text='Save information')
        self.butt.clicked.connect(commit_info_pt2_to_db)
        self.layout.addWidget(self.butt, 17, 0)

    def pt3_adding_guar_pled(self):
        self.clear_gui()

        self.label_start = QLabel('Add pledgor or guarantor')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('AddingMode (Part 3 of 4)')

        admode_pt3_labels = ['Name', 'Type', 'Type 2', 'Date']
        admode_pt3_cmbbox = ['Guarantor', 'Pledgor']
        admode_pt3_cmbbox_2 = ['Organization', 'Entrepreneur']
        self.arrange_labels(place=self.layout, list_with_names=admode_pt3_labels, step_down=1)
        self.arrange_entries_for_comboboxes(place=self.layout, column=1, step_down=1, total=2)
        self.arrange_comboboxes(place=self.layout, list_with_types=admode_pt3_cmbbox,
                                list_with_types_2=admode_pt3_cmbbox_2)

        def check_data():
            data_to_insert = self.collect_data_with_comboboxes()
            if data_to_insert[0] == '':
                QMessageBox.warning(self, 'Warning', 'Please add name')
            else:
                commit_info_to_db()  # (TO-DO) check for folders exists
        def commit_info_to_db():
            data_to_insert = self.collect_data_with_comboboxes()
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))  # change to main folder for connect DB
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO PledGuar (Name, Type, Type2, Date, idSend) '
                           'VALUES (?, ?, ?, ?, ?)',
                           (data_to_insert[0], data_to_insert[1], data_to_insert[2], data_to_insert[3],
                            self.last_number_id_res))
            conn.commit()
            conn.close()
            self.pt4_put_files_gu_pl()
        self.butt = QPushButton(text='Save and next step')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 5, 1)

        self.show()

    def pt4_put_files_gu_pl(self):
        data_to_insert = self.collect_data_with_comboboxes()
        self.type_g_or_p = data_to_insert[1]

        def make_gu_pl_folders():
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            os.chdir(str(self.agree_global))

            b = os.path.exists(data_to_insert[0])
            if b is False:
                q = '_' + data_to_insert[0]
                self.gp_global = 'CLIENTS//' + q
                os.makedirs(q)
                os.chdir(q)

                if self.type_is == 'Organization':  # and Pledgor (delete)
                    folders = self.folders_gp_org
                else:
                    folders = self.folders_gp_entr
                z = 0
                d = len(folders)
                while z != d:
                    folder = folders[z]
                    os.mkdir(folder)
                    z += 1
        make_gu_pl_folders()

        self.clear_gui()

        self.label_start = QLabel('Put files in folders')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('AddingMode (Part 2 of 4)')

        self.len_folder = 0
        if self.type_is == 'Organization':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_org, step_down=2)
            self.len_folder = len(self.folders_gp_org)
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_entr, step_down=2)
            self.len_folder = len(self.folders_gp_entr)

        self.arrange_color_labels(place=self.layout, total=self.len_folder)

        def add_attribute_or_no():
            result = self.check_files_in_folder()
            if result is True:
                self.pt4_adding_attributes_for_files_gp()
        self.butt = QPushButton(text='Check files in folder')
        self.butt.clicked.connect(add_attribute_or_no)
        self.layout.addWidget(self.butt, 17, 1)

    def pt4_adding_attributes_for_files_gp(self):
        print('3')
        self.clear_gui()

        self.label_start = QLabel('Add attributes for documents')
        self.layout.addWidget(self.label_start, 0, 0)
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle('AddingMode (Part 3 of 4)')

        if self.type_is == 'Organization':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_org, step_down=2)
            words = self.sum_gp_org_attr
            self.arr_attr_start_or_pg = 1
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_entr, step_down=2)
            words = self.sum_gp_entr_attr
            self.arr_attr_start_or_pg = 1

        self.arrange_attributes(place=self.layout, step_down=2, list_with_words=words)
        def commit_info_pt4_to_db():
            print('1')
            list_with_attributes = self.collect_data()
            print('2')
            # prepare to insert data (separate by column)
            separate_list_with_attributes = []
            start = 0
            stop = 0
            for item in self.attribute_len_list:
                stop += item
                separate_list_with_attributes.append(list_with_attributes[start:stop])
                start += item
            print('3')
            # insert info in DB
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            print('4')
            if self.type_is == 'Organization':  # (TO-DO) do it shorter
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                g = str(separate_list_with_attributes[6])
                cursor.execute(
                    'INSERT INTO DocumGuPl (Adjudications, ApprovalTran, ConsentSpou, ExtractUSRLE, OfficialCorr, '
                    'Questionnaire, SuretAgrPledg, idSend) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (a, b, c, d, e, f, g, self.last_number_id_res))
            else:
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                cursor.execute(
                    'INSERT INTO DocumGuPl (Adjudications, ConsentSpou, OfficialCorr, Questionnaire, RussianPassp, '
                    'SuretAgrPledg, idSend) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (a, b, c, d, e, f, self.last_number_id_res))
            print('5')
            conn.commit()
            conn.close()

            if self.type_g_or_p == 'Pledgor':
                self.pt5_optional_adding_groups_obj()
            else:
                print('go home screen')
        self.butt = QPushButton(text='Save information')
        self.butt.clicked.connect(commit_info_pt4_to_db)
        self.layout.addWidget(self.butt, 17, 0)

    def pt5_optional_adding_groups_obj(self):
        self.clear_gui()

        self.label_start = QLabel('Add groups of objects')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('AddingMode (Part 4 of 4)')

        self.arrange_labels(place=self.layout, list_with_names=['Name'], step_down=1)
        combo = QLineEdit()
        self.layout.addWidget(combo, 1, 1)

        self.data_to_insert = 'none'
        def check_data():
            self.data_to_insert = combo.text()
            if self.data_to_insert == '':
                QMessageBox.warning(self, 'Warning', 'Please add name')
            else:
                self.pt5_optional_check_and_commit()
        self.butt = QPushButton(text='Save and next step')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 3, 1)

        self.show()

    def pt5_optional_check_and_commit(self):
        self.clear_gui()

        self.label_start = QLabel('Put files in folders')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('AddingMode (Part 4 of 4)')

        def make_grp_obj_folders():
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            os.chdir(str(self.gp_global))

            b = os.path.exists(self.data_to_insert)
            if b is False:
                q = '__' + self.data_to_insert
                os.makedirs(q)
                os.chdir(q)

                folders = self.folder_grp_obj

                z = 0
                d = len(folders)
                while z != d:
                    folder = folders[z]
                    os.mkdir(folder)
                    z += 1
        make_grp_obj_folders()


        print(self.data_to_insert)
        def commit_info_to_db():
            data_to_insert = self.collect_data_with_comboboxes()
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))  # change to main folder for connect DB
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO PledGuar (Name, Type, Type2, Date, idSend) '
                           'VALUES (?, ?, ?, ?, ?)',
                           (data_to_insert[0], data_to_insert[1], data_to_insert[2], data_to_insert[3],
                            self.last_number_id_res))
            conn.commit()
            conn.close()
            self.pt4_put_files_gu_pl()
        # def loop_adding():
        # ONLY PLEDGOR GO TO NEXT STEP
        #     QMessageBox.question(self, 'Question', 'Add another ')


class UpdatingMode(QWidget):
    # try mmap; or seek/read;
    # count = 0
    # count += 1
    # count = str(count)
    # cred_line_fle.write(str(count))
    # cred_line_fle.write(str(':'))
    pass


class ViewMode(QWidget):
    pass

if __name__ == "__main__":
    AdMode_pt1 = QApplication(sys.argv)
    run = AddingMode()
    sys.exit(AdMode_pt1.exec_())
