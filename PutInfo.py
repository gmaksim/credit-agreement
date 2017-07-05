#! mode for add info
from tkinter import *
from tkinter import messagebox
from datetime import date
import os
import PutInfo_pt2
put = Tk()
put.title("Add new information. Part 1")
put.geometry("600x700+200+200")


def make_folders_and_files():
    b = os.path.exists('DATA')  # (D) make a check with 'file exist'
    if b is False:
        os.mkdir('DATA')
        messagebox.showinfo('Information', 'DATA folder created')
        q = open('DATA//00_names.txt', 'w')
        messagebox.showinfo('Information', '00_names created')
        q.close()
        z = open('DATA//01_agree.txt', 'w')
        messagebox.showinfo('Information', '01_agree created')
        z.close()


def save_and_step_2():
    cred_line_fle = open('DATA//00_names.txt', 'a')
    cred_line_fle.write(str(creditLine_name.get()))
    cred_line_fle.write(str('\n'))  # (Q) maybe can realize it in another way?
    cred_line_fle.write(str(creditLine_date.get()))
    cred_line_fle.write(str('\n'))
    cred_line_fle.close()

    cred_line_fle = open('DATA//01_agree.txt', 'a')
    cred_line_fle.write(str(creditLine_agreement.get()))
    cred_line_fle.write(str('\n'))  # (Q) maybe can realize it in another way?
    cred_line_fle.write(str(creditLine_date.get()))
    cred_line_fle.write(str('\n'))
    cred_line_fle.close()

    credit_line_name_imp = str(creditLine_name.get())
    credit_line_agreement_imp = str(creditLine_agreement.get())
    put.destroy()
    PutInfo_pt2.step_2_save_and_step_3(credit_line_name_imp, credit_line_agreement_imp)


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
labelAgrDate = Label(text="Passport", fg="#eee", bg="#333")
labelAgrDate.place(relx=.01, rely=.25, height=25, width=60)

get_current_date()
make_folders_and_files()
creditLine_btn = Button(text='Save and next step', height=1, width=20, command=save_and_step_2)
creditLine_btn.place(relx=.12, rely=.30, height=30, width=130)

put.mainloop()
