#! mode for view information
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

# try to move project on pyqt5(+layouts) or use grid, pack
# and fix 'import *' - bad var.

output = Tk()
output.title("View mode")
output.geometry("600x700+100+100")
main_folder = os.getcwd()
conn = sqlite3.connect('DATA//firstBase.sqlite')
cursor = conn.cursor()

# make left listbox (credit line)
cursor.execute('SELECT Name FROM ANAME')
aname_table = cursor.fetchall()
aname_list_box = Listbox()
aname_list_box.place(relx=.30, rely=.1, height=130, width=130)
for item in aname_table:
    aname_list_box.insert(END, item)

# make empty right listbox (credit line credit agree.)
aagre_list_box = Listbox()
aagre_list_box.place(relx=.60, rely=.1, height=130, width=130)


# take position in left lb, and fix it
def past_cred_agr_in_lb(nothing):
    position_in_lb = aname_list_box.curselection()  # take position in left LB
    cursor.execute('SELECT idSend FROM ANAME WHERE id=?', (position_in_lb))  # select in db info with this idSend
    id_selected = cursor.fetchall()
    if id_selected == []:  # (!) think up - about another method  # make correct offset for db
        id_selected = 1
    else:  # 1 and >
        id_selected = str(id_selected)  # convert list to str
        id_selected = int(id_selected[2:-3]) + 1  # cut str then convert to int and +1
        # to have correct offset (position in another table)

    # make right listbox with correct ids
    cursor.execute('SELECT Agreement FROM AAGRE WHERE idSend = (?) ORDER BY id DESC',
                   (id_selected,))  # '()' and ',' - it's important!
    aagre_table = cursor.fetchall()  # print(aagre_table)  # (!) think up - can possible to take arguments for chdir?
    aagre_list_box = Listbox()
    aagre_list_box.place(relx=.60, rely=.1, height=130, width=130)
    for item in aagre_table:
        aagre_list_box.insert(0, item)

    # make down info with docs-folder of credit agree.
    def past_doc_fold_from_cred_agr(nothing):
        # take a name of subfolder (in clients/%cred.agr.%)
        cursor.execute('SELECT Agreement, idSend FROM AAGRE WHERE idSend = (?)',
                       (id_selected,))  # '()' and ',' - it's important!  # take cred.agr where needed credit line
        list_of_aagre_lb = cursor.fetchall()
        id_selected_2 = aagre_list_box.curselection()  # take position in cred.agr
        id_selected_2 = str(id_selected_2)  # convert to str
        id_selected_2 = int(id_selected_2[1:-2])  # cut str and convert to int
        agree_id_folder = list_of_aagre_lb[id_selected_2]  # in cred.agr. listbox take info with correct position
        agree_folder = agree_id_folder[0]  # take first param. (that's subfolder)

        # take a name of main folder (in clients)
        q = position_in_lb[0] + 1  # position in credit line + 1 (make correct offset)
        cursor.execute('SELECT Name, id FROM ANAME WHERE id=(?)', (q,))  # select info ANAME table with current position
        all_info = cursor.fetchall()
        curr_line = (all_info[0])  # take all line with name and id
        credline_folder = curr_line[0]  # tale only name of credit line (that's main folder)

        dirs_doc_view(agree_folder, credline_folder, main_folder)

    aagre_list_box.bind('<<ListboxSelect>>', past_doc_fold_from_cred_agr)


def dirs_doc_view(agree_folder, credline_folder, main_folder):
    os.chdir(main_folder)
    b = os.path.exists('CLIENTS')
    if b is False:
        messagebox.showinfo('WARNING', 'Check CLIENTS folder')
    os.chdir('CLIENTS')
    os.chdir(credline_folder)
    os.chdir(agree_folder)
    print(os.getcwd())

aname_list_box.bind('<<ListboxSelect>>', past_cred_agr_in_lb)
output.mainloop()
conn.close()
