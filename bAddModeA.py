#! mode for add info
from tkinter import *
from tkinter import messagebox
from datetime import date
import os
import sqlite3


class AddMode:
    def __init__(self, master):
        self.master = master
        root.title("Add new information. Part 1")
        root.geometry("600x700+100+100")

        self.labelStart = Label(text="Add name of organization and # of agreement")
        self.labelStart.place(relx=.01, rely=.01, height=60, width=250)

        self.creditLine_name = StringVar()
        self.creditLine_entry_name = Entry(textvariable=self.creditLine_name)
        self.creditLine_entry_name.place(relx=.12, rely=.1, height=25, width=130)

        self.creditLine_type = StringVar()
        self.creditLine_type.set('Organization')
        self.creditLine_rb_type = Radiobutton(value='Organization', variable=self.creditLine_type,
                                              text='Organization')
        self.creditLine_rb_type.place(relx=.12, rely=.15, height=25, width=130)
        self.creditLine_rb_type_2 = Radiobutton(value='Entrepreneur', variable=self.creditLine_type,
                                                text='Entrepreneur')
        self.creditLine_rb_type_2.place(relx=.12, rely=.20, height=25, width=130)

        self.creditLine_date = StringVar()
        self.creditLine_entry_date = Entry(textvariable=self.creditLine_date)
        self.creditLine_entry_date.place(relx=.12, rely=.25, height=25, width=130)

        self.creditLine_agreement = StringVar()
        self.creditLine_entry_agreement = Entry(textvariable=self.creditLine_agreement)
        self.creditLine_entry_agreement.place(relx=.12, rely=.30, height=25, width=130)

        self.creditLine_agr_date = StringVar()
        self.creditLine_entry_agr_date = Entry(textvariable=self.creditLine_agr_date)
        self.creditLine_entry_agr_date.place(relx=.12, rely=.35, height=25, width=130)

        self.labelName = Label(text="Name", fg="#eee", bg="#333")
        self.labelName.place(relx=.01, rely=.10, height=25, width=60)
        self.labelType = Label(text="Type", fg="#eee", bg="#333")
        self.labelType.place(relx=.01, rely=.15, height=25, width=60)
        self.labelDate = Label(text="Date", fg="#eee", bg="#333")
        self.labelDate.place(relx=.01, rely=.25, height=25, width=60)
        self.labelAgreement = Label(text="Agreement", fg="#eee", bg="#333")
        self.labelAgreement.place(relx=.01, rely=.30, height=25, width=60)
        self.labelAgrDate = Label(text="Agr. date", fg="#eee", bg="#333")
        self.labelAgrDate.place(relx=.01, rely=.35, height=25, width=60)

        self.creditLine_btn = Button(text='Save and next step', height=1, width=20, command=self.save_start_info)
        self.creditLine_btn.place(relx=.12, rely=.40, height=30, width=130)

        # folders for type of name # (TO-DO) push it to DB and create execute-select
        self.folders_org = ('Adjudications', 'Application', 'Approval of the transaction', 'Extract USRLE',
                            'List of participants or shareholders register', 'Main contract',
                            'Official correspondence', 'Questionnaire')
        self.folders_entr = ('Adjudications', 'Application', 'Consent of the spouse', 'Main contract',
                             'Official correspondence', 'Questionnaire', 'Russian passport')

        # lists for labels name  # (TO-DO) push it to DB and create execute-select
        self.Adjudications = ('Plaintiff', 'Respondent', 'Third parties', 'Case number', 'Instance')
        self.Application = ('Profile Date',)
        self.ApprovalTran = ('meeting Date', 'participants of the meeting', 'Chairman of meeting', 'Secretary')
        self.ConsentSpou = ('Date',)
        self.ExtractUSRLE = ('date of issue', 'director', 'members of society')
        self.ListParShare = ('list Date', 'Member №1', 'member share №1', 'Member №2', 'member share №2')
        self.MainContract = ('The lender / guarantor', 'Borrower / Principal', 'beneficiary', 'contract number', 'Date of contract',
                             'The amount of the transaction', 'Contract fee Period', 'Signatory of the Creditor', 'Signatory of the Borrower')
        self.OfficialCorr = ('Sender', 'Destination', 'Outgoing №', 'Date Outgoing №', 'Incoming №', 'Date Incoming №')
        self.Questionnaire = ('Profile Date',)
        self.RussianPassp = ('Number',)

        # lists to put in insert
        self.sum_org_attr = (self.Adjudications + self.Application + self.ApprovalTran + self.ExtractUSRLE +
                             self.ListParShare + self.MainContract + self.OfficialCorr + self.Questionnaire)
        self.sum_entr_attr = (self.Adjudications + self.Application + self.ConsentSpou + self.MainContract +
                              self.OfficialCorr + self.Questionnaire + self.RussianPassp)

        # delete it after test
        self.attr = ('Plaintiff', 'Respondent', 'Third parties', 'Case number', 'Instance', 'Profile Date',
                           'meeting Date', 'participants of the meeting', 'Chairman of meeting', 'Secretary', 'Date',
                           'date of issue', 'director', 'members of society', 'list Date', 'Member №1',
                           'member share №1', 'Member №2', 'member share №2', 'The lender / guarantor',
                           'Borrower / Principal', 'beneficiary', 'contract number', 'Date of contract',
                           'The amount of the transaction', 'Contract fee Period', 'Signatory of the Creditor',
                           'Signatory of the Borrower', 'Sender', 'Destination', 'Outgoing №', 'Date Outgoing №',
                           'Incoming №', 'Date Incoming №', 'Profile Date', 'Number')

        self.get_current_date(self)
        self.make_db()

    def get_current_date(self, nothing):
        today = date.today()
        self.creditLine_entry_date.insert(END, today)
        self.creditLine_entry_agr_date.insert(END, today)

    @staticmethod
    def make_db():
        b = os.path.exists('DATA')
        if b is False:
            os.mkdir('DATA')
            messagebox.showinfo('Information', 'DATA folder and DB file created')
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute(  # (TO-DO) make it right (executescript)
                'CREATE TABLE ANAME (id integer PRIMARY KEY, Name text NULL, Date text NULL, Type text NULL, idSend integer NULL)')
            cursor.execute(
                'CREATE TABLE AAGRE (id integer PRIMARY KEY, Agreement text NULL, AgrDate text NULL, idSend integer NULL)')
            cursor.execute(
                'CREATE TABLE BDOCAGRE (id integer PRIMARY KEY, Adjudications text NULL, Application text NULL, '
                'ApprovalTran text NULL, ConsentSpou text NULL, ExtractUSRLE text NULL, ListParShare text NULL, '
                'MainContract text NULL, OfficialCorr text NULL, Questionnaire text NULL, RussianPassp text NULL, idSend integer NULL)')
            conn.close()

    def save_start_info(self):
        credit_line_name_imp = str(self.creditLine_name.get())
        credit_line_agreement_imp = str(self.creditLine_agreement.get())
        credit_line_date_imp = str(self.creditLine_date.get())
        credit_line_agrdate_imp = str(self.creditLine_agr_date.get())
        self.credit_line_name_type = str(self.creditLine_type.get())
        len1 = len(credit_line_name_imp)
        len2 = len(credit_line_agreement_imp)

        if len1 + len2 == 0:
            messagebox.showinfo('Information', 'Please type name and # of agreement')
        elif len1 <= 0 or len2 <= 0:
            messagebox.showinfo('Information', 'Please type name or # of agreement')
        else:
            conn = sqlite3.connect('DATA//firstBase.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT idSend FROM ANAME')
            number_id_res = cursor.fetchone()

            if number_id_res is None:
                cursor.execute('INSERT INTO ANAME (Name, Date, Type, idSend) VALUES (?, ?, ?, ?)',
                               (credit_line_name_imp, credit_line_date_imp, self.credit_line_name_type, 1))
                cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
                               (credit_line_agreement_imp, credit_line_agrdate_imp, 1))
            else:
                cursor.execute('SELECT idSend FROM ANAME')
                numbers_id_res = cursor.fetchall()
                max_numbers = str(max(numbers_id_res))  # take max number of idSend, convert to str type to possible cut
                last_number_id_res = int(max_numbers[1:-2]) + 1  # cut '(,)' around number, convert to int and plus one
                cursor.execute('INSERT INTO ANAME (Name, Date, Type, idSend) VALUES (?, ?, ?, ?)',
                               (credit_line_name_imp, credit_line_date_imp, self.credit_line_name_type, last_number_id_res))
                cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
                               (credit_line_agreement_imp, credit_line_agrdate_imp, last_number_id_res))
            conn.commit()
            conn.close()
            self.create_new_window(credit_line_name_imp, credit_line_agreement_imp, self.credit_line_name_type)

    def make_clients_folders(self, credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type):
        b = os.path.exists('CLIENTS')
        if b is False:
            os.mkdir('CLIENTS')
            messagebox.showinfo('Information', 'CLIENTS folder created')
        os.chdir('CLIENTS')
        b = os.path.exists(credit_line_name_imp)
        if b is False:
            q = credit_line_name_imp + '//' + credit_line_agreement_imp
            os.makedirs(q)
            os.chdir(q)
            z = 0
            if credit_line_name_type == 'Organization':
                folders = self.folders_org
            else:
                folders = self.folders_entr
            d = len(folders)
            while z != d:
                folder = folders[z]
                os.mkdir(folder)
                z += 1
        else:
            print('realization for additional agreement (later)')

    def create_new_window(self, credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type):
        root.withdraw()
        self.add_file_level = Toplevel()
        self.add_file_level.title("Add new information. Part 2")
        self.add_file_level.geometry("600x700+100+100")
        self.make_clients_folders(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type)

        label_start = Label(self.add_file_level, text="Now you need to put files in folders")
        label_start.place(relx=.01, rely=.01, height=60, width=250)

        if credit_line_name_type == 'Organization':
            self.arrange_labels(self.folders_org, stepX=.28, stepY=.05, place=self.add_file_level)
        else:
            self.arrange_labels(self.folders_entr, stepX=.28, stepY=.05, place=self.add_file_level)

        analyze_folders_btn = Button(self.add_file_level, text='Check files', height=1, width=20, command=self.add_attribute)  # (IN TEST) CHANGE TO analyze_folders
        analyze_folders_btn.place(relx=.08, rely=.50, height=30, width=130)

    def arrange_labels(self, fldrs, stepX, stepY, place):
        z = 0
        y = .10
        x = len(fldrs)  # (TO-DO) check arrange_attribute, possible make func without fldrs?
        labels_gc = []
        while z != x:
            label_name = Label(place, text=fldrs[z], fg="#eee", bg="#333")
            label_name.place(relx=.01, rely=y, height=25, width=150)
            label_color = Label(place, text='', fg="#eee", bg="#cccccc")
            label_color.place(relx=stepX, rely=y, height=25, width=40)
            labels_gc.append(label_name)
            labels_gc.append(label_color)
            z += 1
            y += stepY

    def analyze_folders(self):  # (TO-DO) make it right (this func too long and hard to understanding)
        # check add file or no (in folder) and make []
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
        def count():  # "static" count
            try:
                count.a += 1
            except AttributeError:
                count.a = 0
            return count.a

        def make_color():
            curr_color = file_exists[count()]
            return curr_color

        s = 0
        y = .10
        while s != len_dirs:
            q1 = Label(text='', fg="#eee", bg=make_color())
            q1.place(relx=.28, rely=y, height=25, width=40)
            s += 1
            y += .05

        # check for start add_attribute func
        null_documents = ['Adjudications', 'Official correspondence']
        for q in null_documents:
            for i in dirs_without_docs:
                if i == q:
                    c = dirs_without_docs.index(q)
                    dirs_without_docs.pop(c)
        if dirs_without_docs == []:
            self.add_attribute()
        else:
            messagebox.showinfo('Information', 'Add all needed files, please')

    def add_attribute(self):
        self.add_file_level.withdraw()
        self.attribute_level = Toplevel()
        self.attribute_level.title("Add new information. Part 3")
        self.attribute_level.geometry("820x700+100+100")

        labelStart = Label(self.attribute_level, text="Add attributes for documents")
        labelStart.place(relx=.01, rely=.01, height=60, width=250)

        creditLine_btn = Button(self.attribute_level, text='Save and next step',
                                height=1, width=20, command=self.save_attributes)
        creditLine_btn.place(relx=.01, rely=.90, height=30, width=130)

        if self.credit_line_name_type == 'Organization':
            self.arrange_labels(self.folders_org, stepX=.20, stepY=.1, place=self.attribute_level)
            self.arrange_attribute(self.sum_org_attr, stepX=.11, stepY=.1, place=self.attribute_level)
        else:
            self.arrange_labels(self.folders_entr, stepX=.20, stepY=.1, place=self.attribute_level)
            self.arrange_attribute(self.sum_entr_attr, stepX=.15, stepY=.1, place=self.attribute_level)

        self.attribute_level.mainloop()

    def arrange_attribute(self, sum_attr, stepX, stepY, place):

        def attribute_all_len(type):  # (TO-DO) do it shorter
            len_attrib = []
            if type == 'org':
                len_attrib.append(len(self.Adjudications))  # Aou
                len_attrib.append(len(self.Application))  # Aou
                len_attrib.append(len(self.ApprovalTran))  # o
                len_attrib.append(len(self.ExtractUSRLE))  # o
                len_attrib.append(len(self.ListParShare))  # o
                len_attrib.append(len(self.MainContract))  # Aou
                len_attrib.append(len(self.OfficialCorr))  # Aou
                len_attrib.append(len(self.Questionnaire))  # Aou
            else:
                len_attrib.append(len(self.Adjudications))  # Aou
                len_attrib.append(len(self.Application))  # Aou
                len_attrib.append(len(self.ConsentSpou))  # U
                len_attrib.append(len(self.MainContract))  # Aou
                len_attrib.append(len(self.OfficialCorr))  # Aou
                len_attrib.append(len(self.Questionnaire))  # Aou
                len_attrib.append(len(self.RussianPassp))  # U
            return len_attrib

        # receive correct list with len all attribute
        type_send = 'none'
        if self.credit_line_name_type == 'Organization':
            type_send = 'org'
        attribute_len_list = attribute_all_len(type=type_send)

        # arrange attribute in GUI and insert what's need type in entry
        u = 0
        y = .15
        labels_gc_2 = []
        for i in attribute_len_list:
            z = 0
            x = .01
            while z != i:
                self.attrib_data = StringVar()
                self.attrib_data_entry = Entry(place, textvariable=self.attrib_data)
                self.attrib_data_entry.place(relx=x, rely=y, height=25, width=80)
                labels_gc_2.append(self.attrib_data_entry)
                z += 1
                x += stepX
                self.attrib_data_entry.insert(END, sum_attr[u])
                u += 1
            y += stepY

    def save_attributes(self):
        print('go')

if __name__ == "__main__":
    root = Tk()
    my_gui = AddMode(root)

    # for future function
    main_menu = Menu()
    file_menu = Menu()
    file_menu.add_command(label="View")
    file_menu.add_command(label="Add")
    file_menu.add_separator()
    file_menu.add_command(label="Exit")
    main_menu.add_cascade(label="Mode", menu=file_menu)
    main_menu.add_cascade(label="About")
    root.config(menu=main_menu)

    root.mainloop()
