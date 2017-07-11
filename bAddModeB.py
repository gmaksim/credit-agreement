from tkinter import *
from tkinter import messagebox
import os


# class for pledgor/guarantor (to use in second step)
class PledgorGuarantor:
    inFuture = 'addItLater'


def main(credit_line_name_imp, credit_line_agreement_imp):
    add_mode_B = Tk()
    add_mode_B.title("Add new information. Part 2")
    add_mode_B.geometry("600x700+100+100")

    make_folder_in_step2()
    make_clients_folders(credit_line_name_imp, credit_line_agreement_imp)

    label_start = Label(text="Now you need to put files in folders")
    label_start.place(relx=.01, rely=.01, height=60, width=250)

    off_corr_label = Label(text='Official correspondence', fg="#eee", bg="#333")
    off_corr_label.place(relx=.01, rely=.10, height=25, width=150)
    jud_label = Label(text='Judgments', fg="#eee", bg="#333")
    jud_label.place(relx=.01, rely=.15, height=25, width=150)
    cred_agr_label = Label(text='Credit Agreement', fg="#eee", bg="#333")
    cred_agr_label.place(relx=.01, rely=.20, height=25, width=150)

    check_off_corr_label = Label(text='', fg="#eee", bg="#cccccc")
    check_off_corr_label.place(relx=.28, rely=.10, height=25, width=40)
    check_jud_label = Label(text='', fg="#eee", bg="#cccccc")
    check_jud_label.place(relx=.28, rely=.15, height=25, width=40)
    check_cred_agr_label = Label(text='', fg="#eee", bg="#cccccc")
    check_cred_agr_label.place(relx=.28, rely=.20, height=25, width=40)

    analyze_folders_btn = Button(text='Check files', height=1, width=20, command=dirs_to_analyze)
    analyze_folders_btn.place(relx=.08, rely=.25, height=30, width=130)

    add_mode_B.mainloop()


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
        folders = ('Official correspondence', 'Judgments', 'Credit Agreement')
        d = len(folders)
        while z != d:
            folder = folders[z]
            os.mkdir(folder)
            z += 1
    else:
        print('realization for additional agreement (later)')


def dirs_to_analyze():
    # to know add user file in folder or no
    file_exists = []
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

    check_off_corr_label = Label(text='', fg="#eee", bg=make_color())
    check_off_corr_label.place(relx=.28, rely=.10, height=25, width=40)
    check_jud_label = Label(text='', fg="#eee", bg=make_color())
    check_jud_label.place(relx=.28, rely=.15, height=25, width=40)
    check_cred_agr_label = Label(text='', fg="#eee", bg=make_color())
    check_cred_agr_label.place(relx=.28, rely=.20, height=25, width=40)

    # check all files add or no
    r = len(file_exists)
    j = 0
    q = '#00ff7d'
    for i in file_exists:
        if i == q:
            j += 1
    if j == r:
        add_attribute()
    else:
        messagebox.showinfo('Information', 'Add all files, please')


def add_attribute():
    print('all pass')