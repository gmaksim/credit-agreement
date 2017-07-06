from tkinter import *
from tkinter import messagebox
from datetime import date
import os

# class for pledgor/guarantor (to use in second step)
class PledgorGuarantor:
    inFuture = 'addItLater'


def step_2_save_and_step_3(credit_line_name_imp, credit_line_agreement_imp):
    put_step2 = Tk()
    put_step2.title("Add new information. Part 2")
    put_step2.geometry("600x700+200+200")
    label_start = Label(text="Add information about agreement")
    label_start.place(relx=.01, rely=.01, height=60, width=250)

    official_correspondence_label = Label(text='Official correspondence', fg="#eee", bg="#333")
    official_correspondence_label.place(relx=.01, rely=.10, height=25, width=60)

    analyze_folders_btn = Button(text='Save and next step', height=1, width=20, command=dirs_to_analyze)
    analyze_folders_btn.place(relx=.12, rely=.30, height=30, width=130)

    make_folder_in_step2()
    make_clients_folders(credit_line_name_imp, credit_line_agreement_imp)
    put_step2.mainloop()


def make_folder_in_step2():
    b = os.path.exists('CLIENTS')
    if b is False:
        os.mkdir('CLIENTS')
        messagebox.showinfo('Information', 'CLIENTS folder created')


def make_clients_folders(credit_line_name_imp, credit_line_agreement_imp):
    os.chdir('CLIENTS')
    b = os.path.exists(credit_line_name_imp)
    if b is False:
        q = credit_line_name_imp + '//' + credit_line_agreement_imp
        os.makedirs(q)
        os.chdir(q)
        z = 0
        while z != 3:  # (!offset)
            folders_to_create = ('Official correspondence', 'Judgments', 'CreditAgr')
            folder = folders_to_create[z]
            os.mkdir(folder)
            z += 1
    else:
        print('realization for additional agreement (later)')
    global dirs_way
    dirs_way = 'CLIENTS' + '//' + credit_line_name_imp + '//' + credit_line_agreement_imp


def dirs_to_analyze():
    dirs_way = 'C:'  # (!magic) I do not have many thoughts how it fixed 'winerror3', but it works!
    rr = os.listdir(path=dirs_way)
    print(rr)
