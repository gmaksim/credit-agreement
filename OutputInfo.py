#! mode for view information
from tkinter import *
import sqlite3
output = Tk()
output.title("View mode")
output.geometry("600x700+200+200")

def open_file():

    conn = sqlite3.connect('DATA//firstBase.sqlite')
    cursor = conn.cursor()

    cursor.execute('SELECT Name FROM ANAME')
    result = cursor.fetchall()

    list_box = Listbox()
    list_box.place(relx=.30, rely=.1, height=130, width=130)

    for item in result:
        list_box.insert(END, item)



    conn.close()


    # with open('DATA//data.csv', 'r') as file:
    #     all_line = csv.DictReader(file)
    #     full_list_box = Listbox()  # make a listbox with full info (name + date)
    #     full_list_box.place(relx=.30, rely=.1, height=130, width=130)
    #     for row in all_line:
    #         full_list_box.insert(END, row['Name'])

        # begin = 0  # start position of listbox (to separate name and date)
        # end = full_list_box.size()  # final position of listbox
        #
        # global cut_list_box  # (Q) that's bad, (D) need to fix it later
        # cut_list_box = Listbox()
        # cut_list_box.place(relx=.12, rely=.1, height=130, width=130)
        #
        # while begin != end:
        #     cut_data = full_list_box.get(begin)
        #     cut_list_box.insert(END, cut_data)
        #     begin += 2  # (!offset)
        #
        # file.close()


# def open_file2(start, finish):
#     with open('DATA//01_agree.txt', 'r') as file2:
#         all_line_2 = file2.readlines()
#         full_list_box_2 = Listbox()
#         for i in all_line_2:
#             full_list_box_2.insert(END, i)
#         full_list_box_2.place(relx=.30, rely=.1, height=130, width=130)
#
#         all_line_3 = full_list_box_2.get(start, finish)
#         for i in all_line_3:
#             full_list_box_2.insert(0, i)
#         full_list_box_2.delete(2, END)  # (!offset) delete all elements after 2 row
#
#         file2.close()

#
# def push_left_button(nothing):
#     what_select = cut_list_box.curselection()
#     start = cut_list_box.index(what_select)
#     start = int(start)
#     finish = start + start + 1  # (!offset) make a finish index of another file
#     open_file2(start, finish)
#

def main():
    open_file()
    # full_list_box_2 = Listbox()
    # full_list_box_2.place(relx=.30, rely=.1, height=130, width=130)
    # cut_list_box.bind('<<ListboxSelect>>', push_left_button)

main()
output.mainloop()
