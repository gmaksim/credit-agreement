#! mode for add info
from tkinter import *
from tkinter import messagebox
from datetime import date
import os
import sqlite3


def get_current_date():
    today = date.today()
    creditLine_entry_date.insert(END, today)
    creditLine_entry_agr_date.insert(END, today)


def make_db():
    b = os.path.exists('DATA')
    if b is False:
        os.mkdir('DATA')
        messagebox.showinfo('Information', 'DATA folder created')
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE ANAME (id integer PRIMARY KEY, Name text NULL, Date text NULL, Type text NULL, idSend integer NULL)')
        cursor.execute('CREATE TABLE AAGRE (id integer PRIMARY KEY, Agreement text NULL, AgrDate text NULL, idSend integer NULL)')
        conn.close()


def save_start_info():
    credit_line_name_imp = str(creditLine_name.get())
    credit_line_agreement_imp = str(creditLine_agreement.get())
    credit_line_date_imp = str(creditLine_date.get())
    credit_line_agrdate_imp = str(creditLine_agr_date.get())
    credit_line_name_type = str(creditLine_type.get())
    len1 = len(credit_line_name_imp)
    len2 = len(credit_line_agreement_imp)

    if len1+len2 == 0:
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
        add_mode_A.destroy()
        files_widget(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type)


def files_widget(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type):
    add_mode_B = Tk()
    add_mode_B.title("Add new information. Part 2")
    add_mode_B.geometry("600x700+100+100")

    make_clients_folders(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type)

    if credit_line_name_type == 'Organization':
        a1 = Label(text='Adjudications', fg="#eee", bg="#333")
        a1.place(relx=.01, rely=.10, height=25, width=150)
        a2 = Label(text='Application', fg="#eee", bg="#333")
        a2.place(relx=.01, rely=.15, height=25, width=150)
        a3 = Label(text='Approval of the transaction', fg="#eee", bg="#333")
        a3.place(relx=.01, rely=.20, height=25, width=150)
        a4 = Label(text='Extract USRLE', fg="#eee", bg="#333")
        a4.place(relx=.01, rely=.25, height=25, width=150)
        a5 = Label(text='List of participants or shareholders register', fg="#eee", bg="#333")
        a5.place(relx=.01, rely=.30, height=25, width=150)
        a6 = Label(text='Main contract', fg="#eee", bg="#333")
        a6.place(relx=.01, rely=.35, height=25, width=150)
        a7 = Label(text='Official correspondence', fg="#eee", bg="#333")
        a7.place(relx=.01, rely=.40, height=25, width=150)
        a8 = Label(text='Questionnaire', fg="#eee", bg="#333")
        a8.place(relx=.01, rely=.45, height=25, width=150)

        q1 = Label(text='', fg="#eee", bg="#cccccc")
        q1.place(relx=.28, rely=.10, height=25, width=40)
        q2 = Label(text='', fg="#eee", bg="#cccccc")
        q2.place(relx=.28, rely=.15, height=25, width=40)
        q3 = Label(text='', fg="#eee", bg="#cccccc")
        q3.place(relx=.28, rely=.20, height=25, width=40)
        q4 = Label(text='', fg="#eee", bg="#cccccc")
        q4.place(relx=.28, rely=.25, height=25, width=40)
        q5 = Label(text='', fg="#eee", bg="#cccccc")
        q5.place(relx=.28, rely=.30, height=25, width=40)
        q6 = Label(text='', fg="#eee", bg="#cccccc")
        q6.place(relx=.28, rely=.35, height=25, width=40)
        q7 = Label(text='', fg="#eee", bg="#cccccc")
        q7.place(relx=.28, rely=.40, height=25, width=40)
        q8 = Label(text='', fg="#eee", bg="#cccccc")
        q8.place(relx=.28, rely=.45, height=25, width=40)

    else:
        a1 = Label(text='Adjudications', fg="#eee", bg="#333")
        a1.place(relx=.01, rely=.10, height=25, width=150)
        a2 = Label(text='Application', fg="#eee", bg="#333")
        a2.place(relx=.01, rely=.15, height=25, width=150)
        a3 = Label(text='Consent of the spouse', fg="#eee", bg="#333")
        a3.place(relx=.01, rely=.20, height=25, width=150)
        a4 = Label(text='Main contract', fg="#eee", bg="#333")
        a4.place(relx=.01, rely=.25, height=25, width=150)
        a5 = Label(text='Official correspondence', fg="#eee", bg="#333")
        a5.place(relx=.01, rely=.30, height=25, width=150)
        a6 = Label(text='Questionnaire', fg="#eee", bg="#333")
        a6.place(relx=.01, rely=.35, height=25, width=150)
        a7 = Label(text='Russian passport', fg="#eee", bg="#333")
        a7.place(relx=.01, rely=.40, height=25, width=150)

        q1 = Label(text='', fg="#eee", bg="#cccccc")
        q1.place(relx=.28, rely=.10, height=25, width=40)
        q2 = Label(text='', fg="#eee", bg="#cccccc")
        q2.place(relx=.28, rely=.15, height=25, width=40)
        q3 = Label(text='', fg="#eee", bg="#cccccc")
        q3.place(relx=.28, rely=.20, height=25, width=40)
        q4 = Label(text='', fg="#eee", bg="#cccccc")
        q4.place(relx=.28, rely=.25, height=25, width=40)
        q5 = Label(text='', fg="#eee", bg="#cccccc")
        q5.place(relx=.28, rely=.30, height=25, width=40)
        q6 = Label(text='', fg="#eee", bg="#cccccc")
        q6.place(relx=.28, rely=.35, height=25, width=40)
        q7 = Label(text='', fg="#eee", bg="#cccccc")
        q7.place(relx=.28, rely=.40, height=25, width=40)

    label_start = Label(text="Now you need to put files in folders")
    label_start.place(relx=.01, rely=.01, height=60, width=250)

    analyze_folders_btn = Button(text='Check files', height=1, width=20, command=analyze_folders)
    analyze_folders_btn.place(relx=.08, rely=.50, height=30, width=130)

    add_mode_B.mainloop()


def make_clients_folders(credit_line_name_imp, credit_line_agreement_imp, credit_line_name_type):
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
            folders = ('Official correspondence', 'Adjudications', 'Main contract', 'Questionnaire', 'Application',
                       'Approval of the transaction', 'Extract USRLE', 'List of participants or shareholders register')
        else:
            folders = ('Official correspondence', 'Adjudications', 'Main contract', 'Questionnaire', 'Application',
                       'Consent of the spouse', 'Russian passport')
        d = len(folders)
        while z != d:
            folder = folders[z]
            os.mkdir(folder)
            z += 1
    else:
        print('realization for additional agreement (later)')


def analyze_folders():
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
        add_attribute()
    else:
        print('no')


def add_attribute():
    print('all pass')


add_mode_A = Tk()
add_mode_A.title("Add new information. Part 1")
add_mode_A.geometry("600x700+100+100")

labelStart = Label(text="Add name of organization and # of agreement")
labelStart.place(relx=.01, rely=.01, height=60, width=250)

creditLine_name = StringVar()
creditLine_entry_name = Entry(textvariable=creditLine_name)
creditLine_entry_name.place(relx=.12, rely=.1, height=25, width=130)

creditLine_type = StringVar()
creditLine_type.set('Organization')
creditLine_rb_type = Radiobutton(value='Organization', variable=creditLine_type, text='Organization', state='normal')
creditLine_rb_type.place(relx=.12, rely=.15, height=25, width=130)
creditLine_rb_type_2 = Radiobutton(value='Entrepreneur', variable=creditLine_type, text='Entrepreneur')
creditLine_rb_type_2.place(relx=.12, rely=.20, height=25, width=130)

creditLine_date = StringVar()
creditLine_entry_date = Entry(textvariable=creditLine_date)
creditLine_entry_date.place(relx=.12, rely=.25, height=25, width=130)

creditLine_agreement = StringVar()
creditLine_entry_agreement = Entry(textvariable=creditLine_agreement)
creditLine_entry_agreement.place(relx=.12, rely=.30, height=25, width=130)

creditLine_agr_date = StringVar()
creditLine_entry_agr_date = Entry(textvariable=creditLine_agr_date)
creditLine_entry_agr_date.place(relx=.12, rely=.35, height=25, width=130)

labelName = Label(text="Name", fg="#eee", bg="#333")
labelName.place(relx=.01, rely=.10, height=25, width=60)
labelType = Label(text="Type", fg="#eee", bg="#333")
labelType.place(relx=.01, rely=.15, height=25, width=60)
labelDate = Label(text="Date", fg="#eee", bg="#333")
labelDate.place(relx=.01, rely=.25, height=25, width=60)
labelAgreement = Label(text="Agreement", fg="#eee", bg="#333")
labelAgreement.place(relx=.01, rely=.30, height=25, width=60)
labelAgrDate = Label(text="Agr. date", fg="#eee", bg="#333")
labelAgrDate.place(relx=.01, rely=.35, height=25, width=60)

creditLine_btn = Button(text='Save and next step', height=1, width=20, command=save_start_info)
creditLine_btn.place(relx=.12, rely=.40, height=30, width=130)

get_current_date()
make_db()
add_mode_A.mainloop()