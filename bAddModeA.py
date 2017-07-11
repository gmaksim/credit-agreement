#! mode for add info
from tkinter import *
from tkinter import messagebox
from datetime import date
import os
import sqlite3
import bAddModeB

add_mode_A = Tk()
add_mode_A.title("Add new information. Part 1")
add_mode_A.geometry("600x700+100+100")


def make_db():
    b = os.path.exists('DATA')
    if b is False:
        os.mkdir('DATA')
        messagebox.showinfo('Information', 'DATA folder created')
        conn = sqlite3.connect('DATA//firstBase.sqlite')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE ANAME (id integer PRIMARY KEY, Name text NULL, Date text NULL, idSend integer NULL)')
        cursor.execute('CREATE TABLE AAGRE (id integer PRIMARY KEY, Agreement text NULL, AgrDate text NULL, idSend integer NULL)')
        conn.close()


def save_and_step_2():
    credit_line_name_imp = str(creditLine_name.get())
    credit_line_agreement_imp = str(creditLine_agreement.get())
    credit_line_date_imp = str(creditLine_date.get())
    credit_line_agrdate_imp = str(creditLine_agr_date.get())
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
            cursor.execute('INSERT INTO ANAME (Name, Date, idSend) VALUES (?, ?, ?)',
                           (credit_line_name_imp, credit_line_date_imp, 1))
            cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
                           (credit_line_agreement_imp, credit_line_agrdate_imp, 1))
        else:
            cursor.execute('SELECT idSend FROM ANAME')
            numbers_id_res = cursor.fetchall()
            max_numbers = str(max(numbers_id_res))  # take max number of idSend, convert to str type to possible cut
            last_number_id_res = int(max_numbers[1:-2]) + 1  # cut '(,)' around number, convert to int and plus one
            cursor.execute('INSERT INTO ANAME (Name, Date, idSend) VALUES (?, ?, ?)',
                           (credit_line_name_imp, credit_line_date_imp, last_number_id_res))
            cursor.execute('INSERT INTO AAGRE (Agreement, AgrDate, idSend) VALUES (?, ?, ?)',
                           (credit_line_agreement_imp, credit_line_agrdate_imp, last_number_id_res))
        conn.commit()
        conn.close()
        add_mode_A.destroy()
        bAddModeB.main(credit_line_name_imp, credit_line_agreement_imp)


def get_current_date():
    today = date.today()
    creditLine_entry_date.insert(END, today)
    creditLine_entry_agr_date.insert(END, today)


# elements (step 1)
labelStart = Label(text="Add name of organization and # of agreement")
labelStart.place(relx=.01, rely=.01, height=60, width=250)

creditLine_name = StringVar()
creditLine_entry_name = Entry(textvariable=creditLine_name)
creditLine_entry_name.place(relx=.12, rely=.1, height=25, width=130)

creditLine_date = StringVar()
creditLine_entry_date = Entry(textvariable=creditLine_date)
creditLine_entry_date.place(relx=.12, rely=.15, height=25, width=130)

creditLine_agreement = StringVar()
creditLine_entry_agreement = Entry(textvariable=creditLine_agreement)
creditLine_entry_agreement.place(relx=.12, rely=.20, height=25, width=130)

creditLine_agr_date = StringVar()
creditLine_entry_agr_date = Entry(textvariable=creditLine_agr_date)
creditLine_entry_agr_date.place(relx=.12, rely=.25, height=25, width=130)

labelName = Label(text="Name", fg="#eee", bg="#333")
labelName.place(relx=.01, rely=.10, height=25, width=60)
labelDate = Label(text="Date", fg="#eee", bg="#333")
labelDate.place(relx=.01, rely=.15, height=25, width=60)
labelAgreement = Label(text="Agreement", fg="#eee", bg="#333")
labelAgreement.place(relx=.01, rely=.20, height=25, width=60)
labelAgrDate = Label(text="Agr. date", fg="#eee", bg="#333")
labelAgrDate.place(relx=.01, rely=.25, height=25, width=60)

get_current_date()
make_db()
creditLine_btn = Button(text='Save and next step', height=1, width=20, command=save_and_step_2)
creditLine_btn.place(relx=.12, rely=.30, height=30, width=130)

add_mode_A.mainloop()
