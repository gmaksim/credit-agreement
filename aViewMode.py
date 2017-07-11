#! mode for view information
from tkinter import *
import sqlite3
import os
output = Tk()
output.title("View mode")
output.geometry("600x700+100+100")
conn = sqlite3.connect('DATA//firstBase.sqlite')
cursor = conn.cursor()


def main():
    cursor.execute('SELECT Name FROM ANAME')
    aname_table = cursor.fetchall()
    aname_list_box = Listbox()
    aname_list_box.place(relx=.30, rely=.1, height=130, width=130)
    for item in aname_table:
        aname_list_box.insert(END, item)
    aagre_list_box = Listbox()
    aagre_list_box.place(relx=.60, rely=.1, height=130, width=130)

    def paste_agr(nothing):
        position_in_lb = aname_list_box.curselection()
        cursor.execute('SELECT idSend FROM ANAME WHERE id=?', (position_in_lb))
        id_selected = cursor.fetchall()
        if id_selected == []:  # (!) maybe bad coding style, need to think how to fix it
            id_selected = 1
        else:  # 1 and >
            id_selected = str(id_selected)  # convert list to str
            id_selected = int(id_selected[2:-3]) + 1  # cut str then convert to int and +1
            # to have correct offset (position in another table)
        cursor.execute('SELECT Agreement FROM AAGRE WHERE idSend = (?) ORDER BY id DESC',
                       (id_selected,))  # '()' and ',' - it's important!
        aagre_table = cursor.fetchall()
        aagre_list_box = Listbox()
        aagre_list_box.place(relx=.60, rely=.1, height=130, width=130)
        for item in aagre_table:
            aagre_list_box.insert(0, item)

        def paste_folders(nothing):  # need to fix on idSend
            cursor.execute('SELECT Agreement FROM AAGRE WHERE idSend = (?) ORDER BY id DESC',
                           (id_selected,))  # '()' and ',' - it's important!
            aagre_table = cursor.fetchall()
            for item in aagre_table:
                print(item)

            # folder_name = str(aagre_list_box.curselection())
            # folder_name = int(folder_name[1:-2]) + 1
            # cursor.execute('SELECT Agreement FROM AAGRE WHERE id=?', (folder_name,))
            # curr_fold_name = cursor.fetchall()
            # print(curr_fold_name)
            # curr_fold_name = str(curr_fold_name)
            # curr_fold_name = curr_fold_name[3:-4]
            # print(curr_fold_name)


        aagre_list_box.bind('<<ListboxSelect>>', paste_folders)




    aname_list_box.bind('<<ListboxSelect>>', paste_agr)

main()
output.mainloop()
conn.close()
