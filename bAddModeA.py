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

        self.folders_org = ('Adjudications', 'Application', 'Approval of the transaction', 'Extract USRLE',
                            'List of participants or shareholders register', 'Main contract',
                            'Official correspondence', 'Questionnaire')
        self.folders_entr = ('Adjudications', 'Application', 'Consent of the spouse', 'Main contract',
                             'Official correspondence', 'Questionnaire', 'Russian passport')

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
            cursor.execute(
                'CREATE TABLE ANAME (id integer PRIMARY KEY, Name text NULL, Date text NULL, Type text NULL, idSend integer NULL)')
            cursor.execute(
                'CREATE TABLE AAGRE (id integer PRIMARY KEY, Agreement text NULL, AgrDate text NULL, idSend integer NULL)')
            cursor.execute(
                'CREATE TABLE BDOCAGRE (id integer PRIMARY KEY, Application text NULL, ApprovalTran text NULL, '
                'ConsentSpou text NULL, ExtractUSRLE text NULL, ListParShare text NULL, MainContract text NULL, '
                'OfficialCorr text NULL, Questionnaire text NULL, RussianPassp text NULL, idSend integer NULL)')
            conn.close()

    def save_start_info(self):
        credit_line_name_imp = str(self.creditLine_name.get())
        credit_line_agreement_imp = str(self.creditLine_agreement.get())
        credit_line_date_imp = str(self.creditLine_date.get())
        credit_line_agrdate_imp = str(self.creditLine_agr_date.get())
        credit_line_name_type = str(self.creditLine_type.get())
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
                               (credit_line_name_imp, credit_line_date_imp, credit_line_name_type, 1))
                cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
                               (credit_line_agreement_imp, credit_line_agrdate_imp, 1))
            else:
                cursor.execute('SELECT idSend FROM ANAME')
                numbers_id_res = cursor.fetchall()
                max_numbers = str(max(numbers_id_res))  # take max number of idSend, convert to str type to possible cut
                last_number_id_res = int(max_numbers[1:-2]) + 1  # cut '(,)' around number, convert to int and plus one
                cursor.execute('INSERT INTO ANAME (Name, Date, Type, idSend) VALUES (?, ?, ?, ?)',
                               (credit_line_name_imp, credit_line_date_imp, credit_line_name_type, last_number_id_res))
                cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
                               (credit_line_agreement_imp, credit_line_agrdate_imp, last_number_id_res))
            conn.commit()
            conn.close()
            self.create_new_window(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type)

    def create_new_window(self, credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type):
        root.destroy()
        root2 = Tk()
        root2.title("Add new information. Part 2")
        root2.geometry("600x700+100+100")
        self.make_clients_folders(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type)

        label_start = Label(text="Now you need to put files in folders")
        label_start.place(relx=.01, rely=.01, height=60, width=250)

        if credit_line_name_type == 'Organization':
            self.arrange_labels(self.folders_org)
        else:
            self.arrange_labels(self.folders_entr)

        analyze_folders_btn = Button(text='Check files', height=1, width=20, command=self.analyze_folders)
        analyze_folders_btn.place(relx=.08, rely=.50, height=30, width=130)

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

    def arrange_labels(self, fldrs):
        z = 0
        y = .10
        x = len(fldrs)
        labels_gc = []
        while z != x:
            label_name = Label(text=fldrs[z], fg="#eee", bg="#333")
            label_name.place(relx=.01, rely=y, height=25, width=150)
            label_color = Label(text='', fg="#eee", bg="#cccccc")
            label_color.place(relx=.28, rely=y, height=25, width=40)
            labels_gc.append(label_name)
            labels_gc.append(label_color)
            z += 1
            y += .05

    def analyze_folders(self):
        # to know add user file in folder or no
        file_exists = []
        dirs_without_docs = []
        work_dir = os.getcwd()
        z = 0
        all_dirs_list = os.listdir()
        d = len(all_dirs_list)
        while z != d:
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

        # colour of labels (y/n file in folder)
        def count():  # "static" count
            try:
                count.a += 1
            except AttributeError:
                count.a = 0
            return count.a

        def make_color():
            curr_color = file_exists[count()]
            return curr_color

        q1 = Label(text='', fg="#eee", bg=make_color())
        q1.place(relx=.28, rely=.10, height=25, width=40)
        q2 = Label(text='', fg="#eee", bg=make_color())
        q2.place(relx=.28, rely=.15, height=25, width=40)
        q3 = Label(text='', fg="#eee", bg=make_color())
        q3.place(relx=.28, rely=.20, height=25, width=40)
        q4 = Label(text='', fg="#eee", bg=make_color())
        q4.place(relx=.28, rely=.25, height=25, width=40)
        q5 = Label(text='', fg="#eee", bg=make_color())
        q5.place(relx=.28, rely=.30, height=25, width=40)
        q6 = Label(text='', fg="#eee", bg=make_color())
        q6.place(relx=.28, rely=.35, height=25, width=40)
        q7 = Label(text='', fg="#eee", bg=make_color())
        q7.place(relx=.28, rely=.40, height=25, width=40)

        if d == 8:  # organization type it's 8 folders
            q8 = Label(text='', fg="#eee", bg=make_color())
            q8.place(relx=.28, rely=.45, height=25, width=40)

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
            print('no')

    def add_attribute(self):
        print('all pass')

if __name__ == "__main__":
    root = Tk()
    my_gui = AddMode(root)
    root.mainloop()
