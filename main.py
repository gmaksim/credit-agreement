from PyQt5.QtWidgets import \
    (QWidget, QPushButton, QApplication, QLabel, QComboBox, QLineEdit, QGridLayout,
     QMessageBox, QListWidget, QDialog, QFrame, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
import sqlite3
import sys
import re


class AddingMode(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.create_db_and_tables()
        self.last_number_id_res = self.get_sendid_from_db(table_name='NameAgreement')
        self.agree_global = 'none_dirs'  # to know with which agreement we work
        self.gp_global = 'none dirs'

        # Start block
        self.folders_org = ('Анкета', 'Выписка ЕГРЮЛ', 'Заявка', 'Одобрение сделки',
                            'Основной договор', 'Официальная переписка',
                            'Спис-к уч-в и реестр акционеров', 'Судебные решения')
        self.folders_entr = ('Анкета', 'Заявка', 'Основной договор', 'Официальная переписка',
                             'Паспорт РФ', 'Согласие супруга', 'Судебные решения')
        self.checking_files_done = None

        # GuPl block
        self.folders_gp_org = ('Анкета', 'Выписка ЕГРЮЛ', 'Дог-р пор-ва или залога',
                               'Одобрение сделки', 'Официальная переписка', 'Согласия на обременения',
                               'Судебные решения')
        self.folders_gp_entr = ('Анкета', 'Дог-р пор-ва или залога', 'Официальная переписка',
                                'Паспорт РФ', 'Согласия на обременения', 'Судебные решения')

        # Optional block
        self.folder_grp_obj = ('Выписка ЕГРН', 'Договор купли-продажи', 'Свидетельство о праве собственности')

        # Start block
        self.Adjudications = ('Истец', 'Ответчик', 'Третьи лица', 'Номер дела', 'Инстанция')
        self.Application = ('Дата анкеты',)
        self.ApprovalTran = ('Дата собрания', 'Участники собрания', 'Председатель собрания', 'Секретарь')
        self.ConsentSpou = ('Дата согласия',)
        self.ExtractUSRLE = ('Дата выписки', 'Директор', 'Участники общества')
        self.ListParShare = ('Дата списка', 'Участник №1', 'Доля уч.№1', 'Участник №2', 'Доля уч.№2')
        self.MainContract = ('Кредитор / Гарант', 'Заемщик / Принципал', 'Бенефициар', '№ договора',
                             'Дата дог-ра', 'Сумма сделки', 'Срок сделки',
                             'Подписант от Кредитора', 'Подписант от Заемщика')
        self.OfficialCorr = ('Отправитель', 'Адресат', 'Исх.№', 'Дата исх.№', 'Вх.№', 'Дата вх.№')
        self.Questionnaire = ('Дата анкеты',)
        self.RussianPassp = ('Серия и номер',)
        self.sum_org_attr = (self.Questionnaire + self. ExtractUSRLE + self. Application + self.ApprovalTran +
                             self.MainContract + self.OfficialCorr + self.ListParShare + self.Adjudications)
        self.sum_entr_attr = (self.Questionnaire + self.Application + self.MainContract + self.OfficialCorr +
                              self.RussianPassp + self.ConsentSpou + self.Adjudications)
        self.len_attrib = []


        # GuPl block
        self.ConsEncumb = ('Дата согласия', 'Адрес объекта', 'Кадастровый (или условный) номер',
                           'Тип обременения', 'Срок согласия')
        self.SuretAgrPledg = ('Дата договора', 'Кредитор / Гарант', 'Поручитель / Залогодатель', 'Срок обеспечения',
                              'Рег.номер записи об ипотеке')

        self.sum_gp_org_attr = (self.Questionnaire + self.ExtractUSRLE + self.SuretAgrPledg + self.ApprovalTran
                                + self.OfficialCorr + self.ConsentSpou + self.Adjudications)
        self.sum_gp_entr_attr = (self.Questionnaire + self.SuretAgrPledg + self.OfficialCorr + self.RussianPassp
                                 + self.ConsentSpou + self.Adjudications)

        # Optional block
        self.CertifOwner = ('Дата свидетельства', 'Адрес объекта', 'Кадастровый (или условный) номер')
        self.ContrSale = ('Продавец', 'Покупатель', 'Дата договора', 'Адрес объекта',
                           'Кадастровый (или условный) номер')
        self.ExtracUSRRE = ('Дата выписки', 'Адрес объекта', 'Кадастровый (или условный) номер')
        self.sum_grp_obj_ttr = (self.ExtracUSRRE + self.ContrSale + self.CertifOwner)

        self.mode = 'test'

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

    def arrange_attributes(self, place, step_down, list_with_words, attribute_len):
        self.data_from_attrib = []

        word = 0
        step = 2
        for i in attribute_len:  # i = quantity of needed labels
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

        return self.data_from_attrib

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
                'idSend integer NULL, NameAgreementID text NULL, AgreemNameID text NULL, NameOfAdditAgreem text NULL)')
            cursor.execute(
                'CREATE TABLE PledGuar (id integer PRIMARY KEY, Name text NULL, Type text NULL, Type2 text NULL, '
                'Date text NULL, idSend integer NULL, DocumAgreemID text NULL)')
            cursor.execute(
                'CREATE TABLE DocumGuPl (id integer PRIMARY KEY, Adjudications text NULL, ApprovalTran text NULL, '
                'ConsentSpou text NULL, ExtractUSRLE text NULL, OfficialCorr text NULL, Questionnaire text NULL, '
                'RussianPassp text NULL, SuretAgrPledg text NULL, idSend integer NULL, PledGuarID text NULL)')
            cursor.execute(
                'CREATE TABLE GroupObj (id integer PRIMARY KEY, GlobalName text NULL, Name text NULL, '
                'CertifOwner text NULL, ContrSale text NULL, ExtracUSRRE text NULL, idSend integer NULL, '
                'PledGuarID text NULL)')
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

    def collect_data(self, data_from):
        self.collected_data_attributes = []
        for i in data_from:
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
        null_documents = ['Судебные решения', 'Официальная переписка', 'Согласия на обременения']
        for q in null_documents:
            for i in dirs_without_docs:
                if i == q:
                    c = dirs_without_docs.index(q)
                    dirs_without_docs.pop(c)
        if dirs_without_docs == []:
            self.checking_files_done = True
        else:
            QMessageBox.information(self, 'Информация', 'Пожалуйста добавьте файлы')
            self.checking_files_done = False

        return self.checking_files_done

    def check_stop_symbol_win(self, data):
        new_data = []
        for i in data:
            i = re.sub(r'\/|\\|:|\*|\?|\<|\>|\|', '_', i)  # / \ : * ? < > | on _
            i = re.sub(r'\"', '', i)  # " on 'space' (delete)
            if i == '':
                i = 'НЕТ ИНФОРМАЦИИ'
            new_data.append(i)
        return new_data

    def pt1_start_adding(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 1/4.')
        self.layout.setAlignment(Qt.AlignCenter)

        self.label_start = QLabel('Добавьте название организации, дату и договор')
        self.layout.addWidget(self.label_start, 0, 1)

        admode_pt1_labels = ['Название', 'Тип', 'Дата', 'Договор', 'Дата договора']
        admode_pt1_cmbbox = ['Юр.лицо', 'Физ.лицо']
        self.arrange_labels(place=self.layout, list_with_names=admode_pt1_labels, step_down=1)
        self.arrange_entries_for_comboboxes(place=self.layout, column=1, step_down=1, total=3)  # (TO-DO) insert date
        self.arrange_comboboxes(place=self.layout, list_with_types=admode_pt1_cmbbox, list_with_types_2=0)

        def check_data():
            data_to_insert = self.collect_data_with_comboboxes()
            if data_to_insert[0] == '':
                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста добавьте имя')
            elif data_to_insert[3] == '':
                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста добавьте договор')
            else:
                commit_info_to_db()  # (TO-DO) check for folders (cred line) exists
        self.pt1_data_saver = []
        def commit_info_to_db():  # run function by button with param.
            data_to_insert = self.collect_data_with_comboboxes()
            data_to_insert = self.check_stop_symbol_win(data_to_insert)
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()

            stop = 0
            a = os.path.exists('CLIENTS')
            if a is False:
                os.mkdir('CLIENTS')
            os.chdir('CLIENTS')
            list_dir = os.listdir()
            for dir in list_dir:
                if dir == data_to_insert[0]:
                    QMessageBox.warning(self, 'Предупреждение', 'Такое название уже существует')
                    stop = 1

            if stop == 0:
                cursor.execute('INSERT INTO NameAgreement (Name, Type, Date, Agreement, AgrDate, idSend) '
                               'VALUES (?, ?, ?, ?, ?, ?)',
                               (data_to_insert[0], data_to_insert[1], data_to_insert[2],
                                data_to_insert[3], data_to_insert[4], self.last_number_id_res))
                conn.commit()
                conn.close()
                self.nametrans = data_to_insert[0]
                self.agrtrans = data_to_insert[3]
                self.pt1_data_saver.append(data_to_insert[0])
                self.pt1_data_saver.append(data_to_insert[1])
                self.pt1_data_saver.append(data_to_insert[2])
                self.transfer_input_to_pt2 = data_to_insert
                self.pt2_put_files()

        self.butt = QPushButton(text='Сохранить и перейти к следующему шагу')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 6, 1)

        self.show()

    def pt1_start_adding_again(self, mod):
        self.mode = mod
        self.clear_gui()

        self.label_start = QLabel('Добавьте следующий договор')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 1/4.')

        admode_pt1_labels = ['Договор', 'Дата договора']
        self.arrange_labels(place=self.layout, list_with_names=admode_pt1_labels, step_down=1)

        self.entry = QLineEdit()
        self.layout.addWidget(self.entry, 1, 1)
        self.entry2 = QLineEdit()
        self.layout.addWidget(self.entry2, 2, 1)

        self.small_trans = []
        def check_data():
            if self.entry.text() == '':
                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста добавьте договор')
            else:
                self.small_trans.append(self.entry.text())
                self.small_trans.append(self.entry2.text())
                self.mall_trans = self.check_stop_symbol_win(self.small_trans)
                commit_info_to_db()
        def commit_info_to_db():
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()


            cursor.execute('INSERT INTO NameAgreement (Name, Type, Date, Agreement, AgrDate, idSend) '
                           'VALUES (?, ?, ?, ?, ?, ?)',
                           (self.pt1_data_saver[0], self.pt1_data_saver[1], self.pt1_data_saver[2],
                            self.small_trans[0], self.small_trans[1], self.last_number_id_res))
            conn.commit()
            conn.close()
            self.agrtrans = self.small_trans[0]
            self.transfer_input_to_pt2.insert(3, self.small_trans[0])
            self.transfer_input_to_pt2.pop(4)
            self.transfer_input_to_pt2.insert(4, self.small_trans[1])
            self.transfer_input_to_pt2.pop(5)
            self.pt2_put_files()
        self.butt = QPushButton(text='Сохранить и перейти\n к следующему шагу')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 6, 1)

        self.show()

    def pt2_put_files(self):
        data_to_insert = self.check_stop_symbol_win(self.transfer_input_to_pt2)

        try:
            def make_clients_folders():
                os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
                os.chdir('CLIENTS')

                q = data_to_insert[0] + '//' + data_to_insert[3]
                self.agree_global = 'CLIENTS//' + q
                os.makedirs(q)
                os.chdir(q)

                if data_to_insert[1] == 'Юр.лицо':
                    folders = self.folders_org
                else:
                    folders = self.folders_entr
                z = 0
                d = len(folders)
                while z != d:
                    folder = folders[z]
                    os.mkdir(folder)
                    z += 1
        except FileExistsError:
            QMessageBox.information(self, 'ERROR', 'ERROR IN DB, CHECK LAST COMMIT AND FILES')  # (TO-DO) error

        make_clients_folders()

        self.clear_gui()

        self.label_start = QLabel('Расположите файлы в папках')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 2/4.')

        self.len_folder = 0
        self.type_is = 'None'
        if data_to_insert[1] == 'Юр.лицо':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_org, step_down=2)
            self.len_folder = len(self.folders_org)
            self.type_is = 'Юр.лицо'
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_entr, step_down=2)
            self.len_folder = len(self.folders_entr)
            self.type_is = 'Физ.лицо'

        self.arrange_color_labels(place=self.layout, total=self.len_folder)

        def add_attribute_or_no():
            result = self.check_files_in_folder()
            if result is False:  # DEBUG (right - True)
                self.pt2_adding_attributes_for_files()
        self.butt = QPushButton(text='Проверить файлы в папках')
        self.butt.clicked.connect(add_attribute_or_no)
        self.layout.addWidget(self.butt, 17, 1)

    def pt2_adding_attributes_for_files(self):
        self.clear_gui()

        self.label_start = QLabel('Добавьте атр-ты для документов')
        self.layout.addWidget(self.label_start, 0, 0)
        self.setGeometry(30, 30, 1100, 500)
        self.setWindowTitle('Режим добавления. Шаг 2/4.')

        if self.type_is == 'Юр.лицо':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_org, step_down=2)
            words = self.sum_org_attr
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_entr, step_down=2)
            words = self.sum_entr_attr

        def receive_list_with_len_attributes():  # (TO-DO) make flexible func
            self.len_attrib = []
            if self.type_is == 'Юр.лицо':
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.ExtractUSRLE))  # Aou
                self.len_attrib.append(len(self.Application))  # o
                self.len_attrib.append(len(self.ApprovalTran))  # o
                self.len_attrib.append(len(self.MainContract))  # o
                self.len_attrib.append(len(self.OfficialCorr))  # Aou
                self.len_attrib.append(len(self.ListParShare))  # Aou
                self.len_attrib.append(len(self.Adjudications))  # Aou
            else:
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.Application))  # Aou
                self.len_attrib.append(len(self.MainContract))  # U
                self.len_attrib.append(len(self.OfficialCorr))  # Aou
                self.len_attrib.append(len(self.RussianPassp))  # Aou
                self.len_attrib.append(len(self.ConsentSpou))  # Aou
                self.len_attrib.append(len(self.Adjudications))  # U
            return self.len_attrib
        attribute_len_list = receive_list_with_len_attributes()
        data_from_attrib = self.arrange_attributes(place=self.layout, step_down=2, list_with_words=words,
                                                   attribute_len=attribute_len_list)

        def commit_info_pt2_to_db():  # CHECK THIS PART (debug)
            list_with_attributes = self.collect_data(data_from=data_from_attrib)
            list_with_attributes = self.check_stop_symbol_win(list_with_attributes)

            # prepare to insert data (separate by column)
            separate_list_with_attributes = []
            start = 0
            stop = 0
            for item in attribute_len_list:
                stop += item
                separate_list_with_attributes.append(list_with_attributes[start:stop])
                start += item

            # insert info in DB
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            if self.type_is == 'Юр.лицо':  # (TO-DO) do it shorter
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                g = str(separate_list_with_attributes[6])
                h = str(separate_list_with_attributes[7])

                if self.mode == 'anotheragree':
                    cursor.execute(
                        'INSERT INTO DocumAgreem (Adjudications, Application, ApprovalTran, ExtractUSRLE, ListParShare, '
                        'MainContract, OfficialCorr, Questionnaire, idSend, NameAgreementID, AgreemNameID)'
                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (a, b, c, d, e, f, g, h, self.last_number_id_res, self.nametrans, self.agrtrans))
                if self.mode == 'addagree':  # additional
                    cursor.execute(
                        'INSERT INTO DocumAgreem (Adjudications, Application, ApprovalTran, ExtractUSRLE, ListParShare, '
                        'MainContract, OfficialCorr, Questionnaire, idSend, NameAgreementID, AgreemNameID, NameOfAdditAgreem)'
                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (a, b, c, d, e, f, g, h, self.last_number_id_res, self.nametrans, self.agrtrans, self.small_trans[0]))

            else:
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                g = str(separate_list_with_attributes[6])

                if self.mode == 'anotheragree':
                    cursor.execute(
                        'INSERT INTO DocumAgreem (Adjudications, Application, ApprovalTran, ExtractUSRLE, ListParShare, '
                        'MainContract, OfficialCorr, Questionnaire, idSend, NameAgreementID, AgreemNameID)'
                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (a, b, c, d, e, f, g, self.last_number_id_res, self.nametrans, self.agrtrans))
                if self.mode == 'addagree':  # additional
                    cursor.execute(
                        'INSERT INTO DocumAgreem (Adjudications, Application, ApprovalTran, ExtractUSRLE, ListParShare, '
                        'MainContract, OfficialCorr, Questionnaire, idSend, NameAgreementID, AgreemNameID, NameOfAdditAgreem)'
                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (a, b, c, d, e, f, g, self.last_number_id_res, self.nametrans, self.agrtrans, self.small_trans[0]))
            conn.commit()
            conn.close()
            # loop for add.egree
            reply = QMessageBox.question(self, 'Вопрос', 'Добавить дополнительный договор?',
                                         QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.pt1_start_adding_again(mod='addagree')
            else:
                self.pt3_adding_guar_pled()
        self.butt = QPushButton(text='Сохранить и перейти\n к следующему шагу')
        self.butt.clicked.connect(commit_info_pt2_to_db)
        self.layout.addWidget(self.butt, 17, 0)

        self.show()

    def pt3_adding_guar_pled(self):
        self.clear_gui()

        self.label_start = QLabel('Добавьте поручителя или залогодателя')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 3/4.')

        admode_pt3_labels = ['Название', 'Тип', 'Тип 2', 'Дата']
        admode_pt3_cmbbox = ['Поручитель', 'Залогодатель']
        admode_pt3_cmbbox_2 = ['Юр.лицо', 'Физ.лицо']
        self.arrange_labels(place=self.layout, list_with_names=admode_pt3_labels, step_down=1)
        self.arrange_entries_for_comboboxes(place=self.layout, column=1, step_down=1, total=2)
        self.arrange_comboboxes(place=self.layout, list_with_types=admode_pt3_cmbbox,
                                list_with_types_2=admode_pt3_cmbbox_2)

        def check_data():
            data_to_insert = self.collect_data_with_comboboxes()
            if data_to_insert[0] == '':
                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста добавьте имя')
            else:
                commit_info_to_db()  # (TO-DO) check for folders exists
        def commit_info_to_db():
            data_to_insert = self.check_stop_symbol_win(self.collect_data_with_comboboxes())
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO PledGuar (Name, Type, Type2, Date, idSend, DocumAgreemID) '
                           'VALUES (?, ?, ?, ?, ?, ?)',
                           (data_to_insert[0], data_to_insert[1], data_to_insert[2], data_to_insert[3],
                            self.last_number_id_res, self.agrtrans))
            conn.commit()
            conn.close()
            self.plgutrans = data_to_insert[0]
            self.type_is_2 = data_to_insert[2]
            self.pt4_put_files_gu_pl()
        self.butt = QPushButton(text='Сохранить и перейти к следующему шагу')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 5, 1)
        self.setGeometry(30, 30, 600, 500)
        self.show()

    def pt4_put_files_gu_pl(self):
        data_to_insert = self.check_stop_symbol_win(self.collect_data_with_comboboxes())
        self.type_g_or_p = data_to_insert[1]

        def make_gu_pl_folders():
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            os.chdir(str(self.agree_global))

            b = os.path.exists(data_to_insert[0])
            if b is False:
                q = '_' + data_to_insert[0]

                self.gp_global = self.agree_global + '//' + q
                os.makedirs(q)
                os.chdir(q)

                if self.type_is_2 == 'Юр.лицо':  # and Pledgor (delete)
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

        self.label_start = QLabel('Расположите файлы в папках')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 3/4.')

        self.len_folder = 0
        if self.type_is_2 == 'Юр.лицо':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_org, step_down=2)
            self.len_folder = len(self.folders_gp_org)
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_entr, step_down=2)
            self.len_folder = len(self.folders_gp_entr)

        self.arrange_color_labels(place=self.layout, total=self.len_folder)

        def add_attribute_or_no():
            result = self.check_files_in_folder()
            if result is False:  # DEBUG (right - True)
                self.pt4_adding_attributes_for_files_gp()
        self.butt = QPushButton(text='Проверить файлы в папках')
        self.butt.clicked.connect(add_attribute_or_no)
        self.layout.addWidget(self.butt, 17, 1)

        self.show()

    def pt4_adding_attributes_for_files_gp(self):
        self.clear_gui()

        self.label_start = QLabel('Добавьте аттрибуты для документов')
        self.layout.addWidget(self.label_start, 0, 0)
        self.setGeometry(30, 30, 1100, 500)
        self.setWindowTitle('Режим добавления. Шаг 3/4.')

        if self.type_is == 'Юр.лицо':
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_org, step_down=2)
            words = self.sum_gp_org_attr
        else:
            self.arrange_labels(place=self.layout, list_with_names=self.folders_gp_entr, step_down=2)
            words = self.sum_gp_entr_attr

        def receive_list_with_len_attributes_pg():
            self.len_attrib = []
            if self.type_is == 'Юр.лицо':
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.ExtractUSRLE))  # o
                self.len_attrib.append(len(self.SuretAgrPledg))  # o
                self.len_attrib.append(len(self.ApprovalTran))  # o
                self.len_attrib.append(len(self.OfficialCorr))  # Aou
                self.len_attrib.append(len(self.ConsentSpou))  # Aou
                self.len_attrib.append(len(self.Adjudications))  # Aou
            else:
                self.len_attrib.append(len(self.Questionnaire))  # Aou
                self.len_attrib.append(len(self.SuretAgrPledg))  # Aou
                self.len_attrib.append(len(self.OfficialCorr))  # U
                self.len_attrib.append(len(self.RussianPassp))  # Aou
                self.len_attrib.append(len(self.ConsentSpou))  # Aou
                self.len_attrib.append(len(self.Adjudications))  # Aou
            return self.len_attrib
        attribute_len_list = receive_list_with_len_attributes_pg()
        data_from_attrib = self.arrange_attributes(place=self.layout, step_down=2, list_with_words=words, attribute_len=attribute_len_list)

        def commit_info_pt4_to_db():
            list_with_attributes = self.collect_data(data_from=data_from_attrib)
            list_with_attributes = self.check_stop_symbol_win(list_with_attributes)

            # prepare to insert data (separate by column)
            separate_list_with_attributes = []
            start = 0
            stop = 0
            for item in attribute_len_list:
                stop += item
                separate_list_with_attributes.append(list_with_attributes[start:stop])
                start += item

            # insert info in DB
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()

            if self.type_is == 'Юр.лицо':  # (TO-DO) do it shorter
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                g = str(separate_list_with_attributes[6])
                cursor.execute(
                    'INSERT INTO DocumGuPl (Adjudications, ApprovalTran, ConsentSpou, ExtractUSRLE, OfficialCorr, '
                    'Questionnaire, SuretAgrPledg, idSend, PledGuarID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (a, b, c, d, e, f, g, self.last_number_id_res, self.plgutrans))
            else:
                a = str(separate_list_with_attributes[0])
                b = str(separate_list_with_attributes[1])
                c = str(separate_list_with_attributes[2])
                d = str(separate_list_with_attributes[3])
                e = str(separate_list_with_attributes[4])
                f = str(separate_list_with_attributes[5])
                cursor.execute(
                    'INSERT INTO DocumGuPl (Adjudications, ConsentSpou, OfficialCorr, Questionnaire, RussianPassp, '
                    'SuretAgrPledg, idSend, PledGuarID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (a, b, c, d, e, f, self.last_number_id_res, self.plgutrans))

            conn.commit()
            conn.close()

            if self.type_g_or_p == 'Залогодатель':
                self.pt5_optional_adding_global_name()
            else:
                self.loop_in_guaran_pled()
        self.butt = QPushButton(text='Сохранить и перейти\n к следующему шагу')
        self.butt.clicked.connect(commit_info_pt4_to_db)
        self.layout.addWidget(self.butt, 17, 0)

    def pt5_optional_adding_global_name(self):
        self.clear_gui()

        self.label_start = QLabel('Добавьте название группы объектов')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 4/4.')

        self.arrange_labels(place=self.layout, list_with_names=['Название'], step_down=1)
        combo = QLineEdit()
        self.layout.addWidget(combo, 1, 1)

        self.data_small_trans = []
        def check_data():
            if combo.text() == '':
                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста добавьте имя')
            else:
                self.data_small_trans.append(combo.text())
                self.data_small_trans = self.check_stop_symbol_win(self.data_small_trans)
                self.pt5_optional_adding_groups_obj()
        self.butt = QPushButton(text='Сохранить и перейти к следующему шагу')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 3, 1)

        self.show()

    def pt5_optional_adding_groups_obj(self):
        self.clear_gui()

        self.label_start = QLabel('Добавьте групповой объект')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 4/4.')

        self.arrange_labels(place=self.layout, list_with_names=['Название'], step_down=1)
        combo = QLineEdit()
        self.layout.addWidget(combo, 1, 1)

        def check_data():
            if combo.text() == '':
                QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста добавьте имя')
            else:
                self.data_small_trans.insert(1, combo.text())
                self.data_small_trans = self.check_stop_symbol_win(self.data_small_trans)
                self.pt5_optional_check_and_commit()
        self.butt = QPushButton(text='Сохранить и перейти к следующему шагу')
        self.butt.clicked.connect(check_data)
        self.layout.addWidget(self.butt, 3, 1)

        self.show()

    def pt5_optional_check_and_commit(self):
        def make_grp_obj_folders():
            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
            os.chdir(str(self.gp_global))

            b = os.path.exists('__' + self.data_small_trans[0])

            if b is False:
                w = '__' + self.data_small_trans[0]
                os.makedirs(w)
                os.chdir(w)

                w = '__' + self.data_small_trans[1]
                os.makedirs(w)
                os.chdir(w)
                folders = self.folder_grp_obj
                z = 0
                d = len(folders)
                while z != d:
                    folder = folders[z]
                    os.mkdir(folder)
                    z += 1
            else:
                os.chdir('__' + self.data_small_trans[0])
                q = '__' + self.data_small_trans[1]
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

        self.clear_gui()

        self.label_start = QLabel('Расположите файлы в папках')
        self.layout.addWidget(self.label_start, 0, 1)
        self.setGeometry(30, 30, 600, 500)
        self.setWindowTitle('Режим добавления. Шаг 4/4.')

        self.arrange_labels(place=self.layout, list_with_names=self.folder_grp_obj, step_down=2)
        self.len_folder = len(self.folder_grp_obj)
        self.arrange_color_labels(place=self.layout, total=self.len_folder)

        def add_attribute_or_no():
            result = self.check_files_in_folder()
            if result is False:  # DEBUG (right - True)
                adding_attributes_for_grp_obj()
        self.butt = QPushButton(text='Проверить файлы в папках')
        self.butt.clicked.connect(add_attribute_or_no)
        self.layout.addWidget(self.butt, 17, 1)

        def adding_attributes_for_grp_obj():
            self.clear_gui()

            self.label_start = QLabel('Добавьте аттрибуты для документов')
            self.layout.addWidget(self.label_start, 0, 0)
            self.setGeometry(30, 30, 800, 500)
            self.setWindowTitle('Режим добавления. Шаг 4/4.')

            self.arrange_labels(place=self.layout, list_with_names=self.folder_grp_obj, step_down=2)
            words = self.sum_grp_obj_ttr

            def receive_list_with_len_attributes_grp_obj():
                self.len_attrib = []
                self.len_attrib.append(len(self.CertifOwner))
                self.len_attrib.append(len(self.ContrSale))
                self.len_attrib.append(len(self.ExtracUSRRE))
                return self.len_attrib
            self.attribute_len_list = receive_list_with_len_attributes_grp_obj()
            self.data_from_attrib_grp_obj = self.arrange_attributes(place=self.layout, step_down=2,
                                                                    list_with_words=words,
                                                                    attribute_len=self.attribute_len_list)

            self.butt = QPushButton(text='Сохранить и перейти\n к следующему шагу')
            self.butt.clicked.connect(commit_info_to_db)
            self.layout.addWidget(self.butt, 17, 0)

        def commit_info_to_db():
            list_with_attributes = self.collect_data(data_from=self.data_from_attrib_grp_obj)
            list_with_attributes = self.check_stop_symbol_win(list_with_attributes)

            # prepare to insert data (separate by column)
            separate_list_with_attributes = []
            separate_list_with_attributes.append(self.data_small_trans[0])
            separate_list_with_attributes.append(self.data_small_trans[1])
            start = 0
            stop = 0
            for item in self.attribute_len_list:
                stop += item
                separate_list_with_attributes.append(list_with_attributes[start:stop])
                start += item

            os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))  # change to main folder for connect DB
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()

            a = str(separate_list_with_attributes[0])
            b = str(separate_list_with_attributes[1])
            c = str(separate_list_with_attributes[2])
            d = str(separate_list_with_attributes[3])
            e = str(separate_list_with_attributes[4])
            cursor.execute('INSERT INTO GroupObj (GlobalName, Name, CertifOwner, ContrSale, ExtracUSRRE, idSend, '
                           'PledGuarID) VALUES (?, ?, ?, ?, ?, ?, ?)', (a, b, c, d, e, self.last_number_id_res, self.plgutrans))

            conn.commit()
            conn.close()
            self.loop_in_group_obj()

    def loop_in_group_obj(self):
        reply = QMessageBox.question(self, 'Вопрос', 'Добавить другой объект?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.pt5_optional_adding_groups_obj()
        else:
            self.loop_in_guaran_pled()

    def loop_in_guaran_pled(self):
        reply = QMessageBox.question(self, 'Вопрос', 'Добавить другого залогодателя или поручителя?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.pt3_adding_guar_pled()
        else:
            self.loop_in_creed_agr()

    def loop_in_creed_agr(self):
        reply = QMessageBox.question(self, 'Вопрос', 'Добавить другой кредитный договор?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.pt1_start_adding_again(mod='anotheragree')
        else:
            self.close()


class UpdatingMode(QDialog):
    # use add+view class with add button
    # try mmap; or seek/read;
    # count = 0
    # count += 1
    # count = str(count)
    # cred_line_fle.write(str(count))
    # cred_line_fle.write(str(':'))
    pass


# reverse search input (stop win symbol)
class SearchMode(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.start()

    def start(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setGeometry(30, 30, 300, 600)
        self.setWindowTitle('Режим поиска')
        self.layout.setAlignment(Qt.AlignCenter)

        self.show()


class ViewMode(QDialog, QFrame):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setStyleSheet("QWidget {selection-color: white; font: arial 8px;}")

        self.folder_org_entr = ('Судебные решения', 'Заявка', 'Одобрение сделки', 'Согласие супруга',
                                'Выписка ЕГРЮЛ', 'Спис-к уч-в и реестр акционеров', 'Основной договор', 'Официальная переписка',
                                'Анкета', 'Паспорт РФ')
        self.folders_org = ('Анкета', 'Выписка ЕГРЮЛ', 'Заявка', 'Одобрение сделки',
                            'Основной договор', 'Официальная переписка',
                            'Спис-к уч-в и реестр акционеров', 'Судебные решения')
        self.folders_entr = ('Анкета', 'Заявка', 'Основной договор', 'Официальная переписка',
                             'Паспорт РФ', 'Согласие супруга', 'Судебные решения')

        self.folders_gp_org = ('Анкета', 'Выписка ЕГРЮЛ', 'Дог-р пор-ва или залога',
                               'Одобрение сделки', 'Официальная переписка', 'Согласия на обременения',
                               'Судебные решения')
        self.folders_gp_entr = ('Анкета', 'Дог-р пор-ва или залога', 'Официальная переписка',
                                'Паспорт РФ', 'Согласия на обременения', 'Судебные решения')

        self.folder_grp_obj = ('Выписка ЕГРН', 'Договор купли-продажи', 'Свидетельство о праве собственности')

        try:
            self.view_cred_line_and_agr()
        except sqlite3.OperationalError:
            label_name = QLabel('База данных отсутствует или недоступна\nСвяжитесь с администратором')
            self.layout.addWidget(label_name, 0, 0)

            self.butt = QPushButton(text='Назад')
            self.butt.clicked.connect(self.close)
            self.layout.addWidget(self.butt, 1, 0)

    def fill_listbox(self, table_name, up_down, right_left):
        list = QListWidget(self)
        self.layout.addWidget(list, up_down, right_left)
        for item in table_name:
            list.addItem(item[0])

    @staticmethod
    def arrange_labels(place, list_with_names, up_down, step_right_left, step_up_down):
        start = 0
        right_left = 2
        while start != len(list_with_names):
            label_name = QLabel(list_with_names[start])
            place.addWidget(label_name, up_down, right_left)
            start += 1
            right_left += step_right_left
            up_down += step_up_down

    def arrange_attributes(self, place, step_down, list_with_words, attribute_len):
        self.data_from_attrib = []

        word = 0
        step = 2
        for i in attribute_len:  # i = quantity of needed labels
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

        return self.data_from_attrib

    def arrange_labels_spaces(self, place, list_with_names, updownpos, step_right):
        start = 0
        step = 1
        while start != len(list_with_names):
            label_name = QLabel(list_with_names[start])
            place.addWidget(label_name, updownpos, step)
            start += 1
            step += step_right

    def view_cred_line_and_agr(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setGeometry(30, 30, 300, 600)
        self.setWindowTitle('Режим просмотра')
        self.layout.setAlignment(Qt.AlignCenter)

        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        labels_spaces = ['                                   ', '                                   ',
                         '                                   ', '         ',
                         '                                   ', '                                   ',
                         '                                   ', '                                   ']  # :(
        self.arrange_labels_spaces(self.layout, labels_spaces, 12, 1)

        cursor.execute('SELECT Name, Type, Date FROM NameAgreement GROUP BY idSend')
        name = cursor.fetchall()
        self.names = QTableWidget()
        self.names.setColumnCount(3)
        self.names.setRowCount(len(name))
        header1 = ['Наименование', 'Тип', 'Дата']
        self.names.setHorizontalHeaderLabels(header1)
        self.names.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.names, 1, 1, 10, 3)
        i = 0
        for item in name:
            self.names.setItem(i, 0, QTableWidgetItem(item[0]))
            self.names.setItem(i, 1, QTableWidgetItem(item[1]))
            self.names.setItem(i, 2, QTableWidgetItem(item[2]))
            i += 1

        self.agrd = QTableWidget()
        self.agrd.setColumnCount(2)
        self.agrd.setRowCount(1)
        header2 = ['Договор', 'Дата договора']
        self.agrd.setHorizontalHeaderLabels(header2)
        self.agrd.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.agrd, 1, 5, 1, 4)

        self.plgua = QTableWidget()
        self.plgua.setColumnCount(4)
        self.plgua.setRowCount(1)
        header2 = ['Назавание', 'Тип', 'Тип 2', 'Дата']
        self.plgua.setHorizontalHeaderLabels(header2)
        self.plgua.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.plgua, 4, 5, 1, 4)

        self.grpobj = QTableWidget()
        self.grpobj.setColumnCount(1)
        self.grpobj.setRowCount(1)
        header2 = ['Группа',]
        self.grpobj.setHorizontalHeaderLabels(header2)
        self.grpobj.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.grpobj, 7, 5, 1, 4)

        self.oneobj = QTableWidget()
        self.oneobj.setColumnCount(1)
        self.oneobj.setRowCount(1)
        header2 = ['Объект в группе',]
        self.oneobj.setHorizontalHeaderLabels(header2)
        self.oneobj.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.oneobj, 10, 5, 1, 4)

        self.names.clicked.connect(self.fill_cred_agr_by_cred_line)
        self.agrd.clicked.connect(self.view_g_pl)
        self.plgua.clicked.connect(self.view_grp_obj)
        self.grpobj.clicked.connect(self.view_obj)

        self.label_info = QLabel('Кредитная линия')
        self.layout.addWidget(self.label_info, 0, 1)
        self.label_info.setStyleSheet("QWidget {color: #000000; font: bold 15px;}")
        self.label_info = QLabel('Договор')
        self.layout.addWidget(self.label_info, 0, 5)
        self.label_info.setStyleSheet("QWidget {color: #000000; font: bold 15px;}")
        self.label_info = QLabel('Залогодатели / поручители')
        self.layout.addWidget(self.label_info, 3, 5)
        self.label_info.setStyleSheet("QWidget {color: #000000; font: bold 15px;}")
        self.label_info = QLabel('Группы объектов')
        self.layout.addWidget(self.label_info, 6, 5)
        self.label_info.setStyleSheet("QWidget {color: #000000; font: bold 15px;}")
        self.label_info = QLabel('Объект')
        self.layout.addWidget(self.label_info, 8, 5)
        self.label_info.setStyleSheet("QWidget {color: #000000; font: bold 15px;}")

        self.butt = QPushButton(text='Документы')
        self.butt.clicked.connect(self.attrib_agree)
        self.layout.addWidget(self.butt, 0, 8)  # договора

        self.butt = QPushButton(text='Документы')
        self.butt.clicked.connect(self.attrib_agree_gupl)
        self.layout.addWidget(self.butt, 3, 8)  # залогодателя / поручителя

        self.butt = QPushButton(text='Документы')
        self.butt.clicked.connect(self.attrib_agree_obj)
        self.layout.addWidget(self.butt, 8, 8)  # объекта в группе

        self.show()
        conn.close()

    def fill_cred_agr_by_cred_line(self):
        self.plgua.clear()
        header2 = ['Назавание', 'Тип', 'Тип 2', 'Дата']
        self.plgua.setHorizontalHeaderLabels(header2)
        self.grpobj.clear()
        header2 = ['Группа',]
        self.grpobj.setHorizontalHeaderLabels(header2)
        self.oneobj.clear()
        header2 = ['Объект в группе',]
        self.oneobj.setHorizontalHeaderLabels(header2)

        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        self.position_in_lb = self.names.currentRow()  # take position in cred.line lb
        self.position_in_lb = str(self.position_in_lb + 1)

        cursor.execute('SELECT Agreement, AgrDate FROM NameAgreement WHERE idSend = (?)',
                       (self.position_in_lb,))
        agrdate = cursor.fetchall()
        self.agrd.setRowCount(len(agrdate))
        # self.agrd.clear()  # i can't remember for what that option, let it remain just in case
        # header1 = ['Договор', 'Дата договора']
        # self.agrd.setHorizontalHeaderLabels(header1)
        i = 0
        self.transagrd = []  # for know names of agreem
        for item in agrdate:
            self.agrd.setItem(i, 0, QTableWidgetItem(item[0]))
            self.agrd.setItem(i, 1, QTableWidgetItem(item[1]))
            self.transagrd.append(item[0])
            i += 1

        cursor.execute('SELECT Type FROM NameAgreement WHERE idSend = (?)',
                       (self.position_in_lb,))  # '()' and ',' - it's important!
        curr_type_cred_line = cursor.fetchall()  # (!) think up - can possible to take arguments for chdir?
        self.curr_type_cred_line = curr_type_cred_line[0]

        conn.close()

    def attrib_agree(self):
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        try:
            if self.curr_type_cred_line[0] == 'Физ.лицо':
                cursor.execute(
                    'SELECT Adjudications, Application, ConsentSpou, MainContract, OfficialCorr, Questionnaire, '
                    'RussianPassp FROM DocumAgreem WHERE idSend = (?)', (self.position_in_lb,))
            else:
                cursor.execute(
                    'SELECT Adjudications, Application, ApprovalTran, ExtractUSRLE, ListParShare, MainContract, '
                    'OfficialCorr, Questionnaire FROM DocumAgreem WHERE idSend = (?)', (self.position_in_lb,))

            name = cursor.fetchall()

            self.position_in_lb_right = self.pos
            self.att_lay = QWidget()
            self.att_lay.layout = QGridLayout()
            self.att_lay.setLayout(self.att_lay.layout)
            self.att_lay.setWindowTitle('Просмотр атрибутов договора')
            self.att_lay.setGeometry(30, 80, 1000, 300)
            self.att_lay.layout.setAlignment(Qt.AlignCenter)

            try:
                def arrange_info(place, step_down, list_with_words, attribute_len):
                    self.data_from_attrib = []

                    clear_words = []
                    w = 0
                    try:
                        while w != len(list_with_words):
                            text = name[self.position_in_lb_right][w]
                            qw = text.split(r', ')
                            for i in qw:
                                i = re.sub(r'\'', '', i)
                                i = re.sub(r'\[', '', i)
                                i = re.sub(r'\]', '', i)
                                clear_words.append(i)
                            w += 1
                    except AttributeError:
                        pass

                    list_with_words = clear_words
                    word = 0
                    step = 2

                    for i in attribute_len:  # i = quantity of needed labels
                        start = 0
                        offset = 2
                        while start != i:
                            entry = QLineEdit(list_with_words[word])
                            entry.setReadOnly(True)
                            if len(attribute_len) == 7:  # make skips for attributes
                                if step == 4:
                                    step += 1
                                if step == 6:
                                    step += 2
                            else:
                                if step == 5:
                                    step += 1
                            place.addWidget(entry, step, offset)
                            self.data_from_attrib.append(entry)
                            start += 1
                            offset += 1
                            word += 1
                        step += step_down

                def receive_list_with_len_attributes():  # (TO-DO) make flexible func
                    self.Adjudications = ('Истец', 'Ответчик', 'Третьи лица', 'Номер дела', 'Инстанция')
                    self.Application = ('Дата анкеты',)
                    self.ApprovalTran = (
                        'Дата собрания', 'Участники собрания', 'Председатель собрания', 'Секретарь')
                    self.ConsentSpou = ('Дата согласия',)
                    self.ExtractUSRLE = ('Дата выписки', 'Директор', 'Участники общества')
                    self.ListParShare = ('Дата списка', 'Участник №1', 'Доля уч.№1', 'Участник №2', 'Доля уч.№2')
                    self.MainContract = ('Кредитор / Гарант', 'Заемщик / Принципал', 'Бенефициар', '№ договора',
                                         'Дата дог-ра', 'Сумма сделки', 'Срок сделки',
                                         'Подписант от Кредитора', 'Подписант от Заемщика')
                    self.OfficialCorr = ('Отправитель', 'Адресат', 'Исх.№', 'Дата исх.№', 'Вх.№', 'Дата вх.№')
                    self.Questionnaire = ('Дата анкеты',)
                    self.RussianPassp = ('Серия и номер',)

                    self.len_attrib = []

                    if self.curr_type_cred_line[0] == 'Юр.лицо':
                        self.len_attrib.append(len(self.Questionnaire))  # Aou
                        self.len_attrib.append(len(self.ExtractUSRLE))  # Aou
                        self.len_attrib.append(len(self.Application))  # o
                        self.len_attrib.append(len(self.ApprovalTran))  # o
                        self.len_attrib.append(len(self.MainContract))  # o
                        self.len_attrib.append(len(self.OfficialCorr))  # Aou
                        self.len_attrib.append(len(self.ListParShare))  # Aou
                        self.len_attrib.append(len(self.Adjudications))  # Aou
                        labels_name = self.folders_org
                    else:
                        self.len_attrib.append(len(self.Questionnaire))  # Aou
                        self.len_attrib.append(len(self.Application))  # Aou
                        self.len_attrib.append(len(self.MainContract))  # U
                        self.len_attrib.append(len(self.OfficialCorr))  # Aou
                        self.len_attrib.append(len(self.RussianPassp))  # Aou
                        self.len_attrib.append(len(self.ConsentSpou))  # Aou
                        self.len_attrib.append(len(self.Adjudications))  # U
                        labels_name = self.folders_entr
                    self.arrange_labels(self.att_lay.layout, labels_name, 1, 0, 2)
                    return self.len_attrib

                attribute_len_list = receive_list_with_len_attributes()
                arrange_info(place=self.att_lay.layout, step_down=2,
                             list_with_words=name[self.position_in_lb_right],
                             attribute_len=attribute_len_list)
                self.att_lay.show()
            except IndexError:
                QMessageBox.warning(self, 'Ошибка', 'Атрибуты отсуствуют!')  # make this in another attr func too



        except AttributeError:
            QMessageBox.information(self, 'Сообщение', 'Вы не выбрали договор')
        except TypeError:
            QMessageBox.information(self, 'Сообщение', 'Сначала нажмите на нужный договор')

        self.pos = 'zero'
        conn.close()

    def view_g_pl(self):
        self.pos = int(self.agrd.currentRow())  # get correct access to attributes (if no selected - error)
        self.grpobj.clear()
        header2 = ['Группа',]
        self.grpobj.setHorizontalHeaderLabels(header2)

        self.oneobj.clear()
        header2 = ['Объект в группе',]
        self.oneobj.setHorizontalHeaderLabels(header2)

        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        self.position_in_lb2 = self.names.currentRow()  # take position in cred.line lb
        self.position_in_lb2 = str(self.position_in_lb2 + 1)

        self.docagrname = self.agrd.currentRow()  # for know names of agreem

        try:
            cursor.execute('SELECT Name, Type, Type2, Date, DocumAgreemID FROM PledGuar WHERE idSend = (?) AND DocumAgreemID = (?)',
                       (self.position_in_lb2, self.transagrd[self.docagrname]))
        except AttributeError:
            pass
        gupldata = cursor.fetchall()
        self.plgua.setRowCount(len(gupldata))

        i = 0
        self.transgupl = []  # for know names of gu/pl
        for item in gupldata:
            self.plgua.setItem(i, 0, QTableWidgetItem(item[0]))
            self.plgua.setItem(i, 1, QTableWidgetItem(item[1]))
            self.plgua.setItem(i, 2, QTableWidgetItem(item[2]))
            self.plgua.setItem(i, 3, QTableWidgetItem(item[3]))
            self.transgupl.append(item[0])
            i += 1

        # cursor.execute('SELECT Type FROM NameAgreement WHERE idSend = (?)',
        #                (self.position_in_lb,))  # '()' and ',' - it's important!
        # curr_type_cred_line = cursor.fetchall()  # (!) think up - can possible to take arguments for chdir?
        # self.curr_type_cred_line = curr_type_cred_line[0]

        conn.close()

    def attrib_agree_gupl(self):
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        try:
            if self.curr_type_cred_line[0] == 'Физ.лицо':
                cursor.execute(
                    'SELECT Adjudications, ConsentSpou, OfficialCorr, Questionnaire, RussianPassp, SuretAgrPledg '
                    'FROM DocumGuPl WHERE idSend = (?)', (self.position_in_lb,))
            else:
                cursor.execute(
                    'SELECT Adjudications, ApprovalTran, ConsentSpou, ExtractUSRLE, OfficialCorr, Questionnaire, '
                    'SuretAgrPledg FROM DocumGuPl WHERE idSend = (?)', (self.position_in_lb,))

            name = cursor.fetchall()
            check_for_none = name[0]

            if check_for_none[0] is None:
                QMessageBox.warning(self, 'Ошибка', 'Атрибуты отсуствуют!')
            else:
                self.position_in_lb_right = self.pos2
                self.att_lay = QWidget()
                self.att_lay.layout = QGridLayout()
                self.att_lay.setLayout(self.att_lay.layout)
                self.att_lay.setWindowTitle('Просмотр атрибутов залогодателя / поручителя')
                self.att_lay.setGeometry(30, 80, 1000, 300)
                self.att_lay.layout.setAlignment(Qt.AlignCenter)

                try:
                    def arrange_info(place, step_down, list_with_words, attribute_len):
                        self.data_from_attrib = []

                        clear_words = []
                        w = 0
                        try:
                            while w != len(list_with_words):
                                text = name[self.position_in_lb_right][w]
                                qw = text.split(r', ')
                                for i in qw:
                                    i = re.sub(r'\'', '', i)
                                    i = re.sub(r'\[', '', i)
                                    i = re.sub(r'\]', '', i)
                                    clear_words.append(i)
                                w += 1
                        except AttributeError:
                            pass

                        list_with_words = clear_words
                        word = 0
                        step = 3

                        for i in attribute_len:  # i = quantity of needed labels
                            start = 0
                            offset = 2
                            while start != i:
                                entry = QLineEdit(list_with_words[word])
                                entry.setReadOnly(True)
                                if len(attribute_len) == 7:  # make skips for attributes
                                    if step == 4:
                                        step += 1
                                    if step == 6:
                                        step += 2
                                else:
                                    if step == 5:
                                        step += 1
                                place.addWidget(entry, step, offset)
                                self.data_from_attrib.append(entry)
                                start += 1
                                offset += 1
                                word += 1
                            step += step_down

                    def receive_list_with_len_attributes():  # (TO-DO) make flexible func
                        self.Adjudications = ('Истец', 'Ответчик', 'Третьи лица', 'Номер дела', 'Инстанция')
                        self.Application = ('Дата анкеты',)
                        self.ApprovalTran = ('Дата собрания', 'Участники собрания', 'Председатель собрания', 'Секретарь')
                        self.ConsentSpou = ('Дата согласия',)
                        self.ExtractUSRLE = ('Дата выписки', 'Директор', 'Участники общества')
                        self.ListParShare = ('Дата списка', 'Участник №1', 'Доля уч.№1', 'Участник №2', 'Доля уч.№2')
                        self.MainContract = ('Кредитор / Гарант', 'Заемщик / Принципал', 'Бенефициар', '№ договора',
                                             'Дата дог-ра', 'Сумма сделки', 'Срок сделки',
                                             'Подписант от Кредитора', 'Подписант от Заемщика')
                        self.OfficialCorr = ('Отправитель', 'Адресат', 'Исх.№', 'Дата исх.№', 'Вх.№', 'Дата вх.№')
                        self.Questionnaire = ('Дата анкеты',)
                        self.RussianPassp = ('Серия и номер',)
                        self.ConsEncumb = ('Дата согласия', 'Адрес объекта', 'Кадастровый (или условный) номер',
                                           'Тип обременения', 'Срок согласия')
                        self.SuretAgrPledg = ('Дата договора', 'Кредитор / Гарант', 'Поручитель / Залогодатель',
                                              'Срок обеспечения', 'Рег.номер записи об ипотеке')

                        self.len_attrib = []

                        if self.curr_type_cred_line[0] == 'Юр.лицо':
                            self.len_attrib.append(len(self.Questionnaire))  # Aou
                            self.len_attrib.append(len(self.ExtractUSRLE))  # Aou
                            self.len_attrib.append(len(self.SuretAgrPledg))  # o
                            self.len_attrib.append(len(self.ApprovalTran))  # o
                            self.len_attrib.append(len(self.OfficialCorr))  # o
                            self.len_attrib.append(len(self.ConsentSpou))  # Aou
                            self.len_attrib.append(len(self.Adjudications))  # Aou
                            labels_name2 = self.folders_gp_org
                        else:
                            self.len_attrib.append(len(self.Questionnaire))  # Aou
                            self.len_attrib.append(len(self.SuretAgrPledg))  # Aou
                            self.len_attrib.append(len(self.OfficialCorr))  # U
                            self.len_attrib.append(len(self.RussianPassp))  # Aou
                            self.len_attrib.append(len(self.ConsentSpou))  # Aou
                            self.len_attrib.append(len(self.Adjudications))  # Aou
                            labels_name2 = self.folders_gp_entr
                        self.arrange_labels(self.att_lay.layout, labels_name2, 2, 0, 2)
                        return self.len_attrib

                    attribute_len_list = receive_list_with_len_attributes()
                    arrange_info(place=self.att_lay.layout, step_down=2, list_with_words=name[self.position_in_lb_right],
                                 attribute_len=attribute_len_list)

                    self.att_lay.show()
                except IndexError:
                    # self.clear_qline()  # FIX BUG (incorrect attributes when < or > (???) 1 agr.)
                    # UPD: TEST, bug doesn't exists
                    pass
        except AttributeError:
            QMessageBox.information(self, 'Сообщение', 'Вы не выбрали залогодателя / поручителя')
        except TypeError:
            QMessageBox.information(self, 'Сообщение', 'Сначала нажмите на нужного залогодателя / поручителя')

        self.pos2 = 'zero'
        conn.close()

    def view_grp_obj(self):
        self.pos2 = int(self.plgua.currentRow())
        self.oneobj.clear()
        header2 = ['Объект в группе',]
        self.oneobj.setHorizontalHeaderLabels(header2)


        # make correct clearing (!)
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        self.position_in_lb3 = self.names.currentRow()  # take position in cred.line lb
        self.position_in_lb3 = str(self.position_in_lb3 + 1)

        self.plguaname = self.plgua.currentRow()

        try:
            cursor.execute('SELECT GlobalName FROM GroupObj WHERE idSend = (?) AND PledGuarID = (?) GROUP BY GlobalName',
                       (self.position_in_lb3, self.transgupl[self.plguaname]))
        except AttributeError:
            pass
        grpobjdata = cursor.fetchall()
        self.grpobj.setRowCount(len(grpobjdata))

        i = 0
        self.transglobnam = []  # for know global name of object
        for item in grpobjdata:
            self.grpobj.setItem(i, 0, QTableWidgetItem(item[0]))
            self.transglobnam.append(item[0])
            i += 1

        # cursor.execute('SELECT Type FROM NameAgreement WHERE idSend = (?)',
        #                (self.position_in_lb,))  # '()' and ',' - it's important!
        # curr_type_cred_line = cursor.fetchall()  # (!) think up - can possible to take arguments for chdir?
        # self.curr_type_cred_line = curr_type_cred_line[0]

        conn.close()

    def view_obj(self):
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()

        self.position_in_lb4 = self.names.currentRow()  # take position in cred.line lb
        self.position_in_lb4 = str(self.position_in_lb4 + 1)

        self.grpobjcurr = self.grpobj.currentRow()

        try:
            cursor.execute('SELECT Name FROM GroupObj WHERE idSend = (?) AND GlobalName = (?)',
                       (self.position_in_lb4, self.transglobnam[self.grpobjcurr]))
        except AttributeError:
            pass
        objdata = cursor.fetchall()
        self.oneobj.setRowCount(len(objdata))

        i = 0
        for item in objdata:
            self.oneobj.setItem(i, 0, QTableWidgetItem(item[0]))
            i += 1

        # cursor.execute('SELECT Type FROM NameAgreement WHERE idSend = (?)',
        #                (self.position_in_lb,))  # '()' and ',' - it's important!
        # curr_type_cred_line = cursor.fetchall()  # (!) think up - can possible to take arguments for chdir?
        # self.curr_type_cred_line = curr_type_cred_line[0]

        conn.close()

    def attrib_agree_obj(self):
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()
        self.pos3 = int(self.oneobj.currentRow())

        try:
            cursor.execute('SELECT CertifOwner, ContrSale, ExtracUSRRE FROM GroupObj WHERE idSend = (?)', (self.position_in_lb,))
            name = cursor.fetchall()
            check_for_none = name[0]

            if check_for_none[0] is None:
                QMessageBox.warning(self, 'Ошибка', 'Атрибуты отсуствуют!')
            if self.pos3 == -1:
                QMessageBox.information(self, 'Сообщение', 'Вы не выбрали объект')
            else:
                self.position_in_lb_right = self.pos3
                self.att_lay = QWidget()
                self.att_lay.layout = QGridLayout()
                self.att_lay.setLayout(self.att_lay.layout)
                self.att_lay.setWindowTitle('Просмотр атрибутов объекта')
                self.att_lay.setGeometry(30, 80, 1000, 300)
                self.att_lay.layout.setAlignment(Qt.AlignCenter)

                try:
                    def arrange_info(place, step_down, list_with_words, attribute_len):
                        self.data_from_attrib = []

                        clear_words = []
                        w = 0
                        try:
                            while w != len(list_with_words):
                                text = name[self.position_in_lb_right][w]
                                qw = text.split(r', ')
                                for i in qw:
                                    i = re.sub(r'\'', '', i)
                                    i = re.sub(r'\[', '', i)
                                    i = re.sub(r'\]', '', i)
                                    clear_words.append(i)
                                w += 1
                        except AttributeError:
                            pass

                        list_with_words = clear_words
                        word = 0
                        step = 2

                        for i in attribute_len:  # i = quantity of needed labels
                            start = 0
                            offset = 2
                            while start != i:
                                entry = QLineEdit(list_with_words[word])
                                entry.setReadOnly(True)
                                if len(attribute_len) == 7:  # make skips for attributes
                                    if step == 4:
                                        step += 1
                                    if step == 6:
                                        step += 2
                                else:
                                    if step == 5:
                                        step += 1
                                place.addWidget(entry, step, offset)
                                self.data_from_attrib.append(entry)
                                start += 1
                                offset += 1
                                word += 1
                            step += step_down

                    def receive_list_with_len_attributes():  # (TO-DO) make flexible func
                        self.CertifOwner = ('Дата свидетельства', 'Адрес объекта', 'Кадастровый (или условный) номер')
                        self.ContrSale = ('Продавец', 'Покупатель', 'Дата договора', 'Адрес объекта',
                                          'Кадастровый (или условный) номер')
                        self.ExtracUSRRE = ('Дата выписки', 'Адрес объекта', 'Кадастровый (или условный) номер')

                        self.len_attrib = []

                        self.len_attrib.append(len(self.CertifOwner))  # Aou
                        self.len_attrib.append(len(self.ContrSale))  # Aou
                        self.len_attrib.append(len(self.ExtracUSRRE))  # o
                        self.arrange_labels(self.att_lay.layout, self.folder_grp_obj, 1, 0, 2)
                        return self.len_attrib

                    attribute_len_list = receive_list_with_len_attributes()
                    arrange_info(place=self.att_lay.layout, step_down=2, list_with_words=name[self.position_in_lb_right],
                                 attribute_len=attribute_len_list)

                    self.att_lay.show()
                except IndexError:
                    # self.clear_qline()  # FIX BUG (incorrect attributes when < or > (???) 1 agr.)
                    # UPD: TEST, bug doesn't exists
                    pass
        except AttributeError:
            QMessageBox.information(self, 'Сообщение', 'Вы не выбрали объект')
        except TypeError:
            QMessageBox.information(self, 'Сообщение', 'Сначала нажмите на нужный объект')
        except IndexError:
            QMessageBox.information(self, 'Сообщение', 'Вы не выбрали объект')

        self.pos3 = 'zero'  # small bug - button work if you don't select something (remember last pos)
        conn.close()


sys._excepthook = sys.excepthook  # for catching pyqt c++ errors
def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook


def main():
    def start_mode(parent, mode):
        st = ''
        if mode == 'adding':
            st = AddingMode()
        if mode == 'view':
            st = ViewMode()
        if mode == 'search':
            st = SearchMode()
        if mode == 'update':
            QMessageBox.information(root, 'Сообщение', 'Режим в разработке')

        root.setDisabled(True)
        go_to_home_screen = st.exec_()
        if go_to_home_screen == 0:
            root.setDisabled(False)
            root.activateWindow()




    app = QApplication(sys.argv)
    ico = QIcon('icon.png')
    app.setWindowIcon(ico)  # very important action

    root = QWidget()
    root.layout = QGridLayout()
    root.setLayout(root.layout)
    root.setGeometry(30, 30, 400, 400)
    root.layout.setAlignment(Qt.AlignCenter)

    root.setWindowTitle('Кредитный договор (версия 0.7)')
    root.label_start = QLabel('Выберите режим работы:\n')
    root.label_start.setAlignment(Qt.AlignCenter)
    root.layout.addWidget(root.label_start, 0, 1)
    root.label_down = QLabel('\nОБРАТИТЕ ВНИМАНИЕ!\nРекомендуемое разрешение\nэкрана для комфортной'
                             '\nработы 1280x1024 (19* монитор)')
    root.label_down.setAlignment(Qt.AlignCenter)
    root.layout.addWidget(root.label_down, 5, 1)

    root.butt = QPushButton(text='Добавить кредитную линию')
    root.butt.clicked.connect(lambda: start_mode(root, mode='adding'))
    root.layout.addWidget(root.butt, 1, 1)
    root.butt = QPushButton(text='Просмотреть кредитную линии')
    root.butt.clicked.connect(lambda: start_mode(root, mode='view'))
    root.layout.addWidget(root.butt, 2, 1)
    root.butt = QPushButton(text='Обновить кредитную линию')
    root.butt.clicked.connect(lambda: start_mode(root, mode='update'))
    root.layout.addWidget(root.butt, 3, 1)
    root.butt = QPushButton(text='Поисковый запрос')
    root.butt.clicked.connect(lambda: start_mode(root, mode='search'))
    root.layout.addWidget(root.butt, 4, 1)

    start_mode(root, mode='adding')  # DEBUG (right - delete this row)

    root.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print('\tPROGRAM IN DEBUG MODE! (check files in folders is disabled, view mode in auto-start')
    print('\t\tADDING MODE - 95% (95% tested)'
          '\n\t\tVIEW MODE - 90% (80% tested)'
          '\n\t\tSEARCH MODE - 10% (0% tested)'
          '\n\t\tUPDATE MODE - 40% (0% tested)\n')
    main()
