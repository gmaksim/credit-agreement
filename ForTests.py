#! temp .py file to check some part of code

#! mode for view information (A1 VARIANT)
# from tkinter import *
#
# output = Tk()
# output.title("View mode")
# output.geometry("600x700+200+200")
#
# def open_file():
#     with open('TXT_files//credLineFile.txt', 'r') as file:
#
#         all_line = file.readlines()
#         line_list_box = Listbox()
#         for i in all_line:
#             line_list_box.insert(END, i)
#             line_list_box.place(relx=.12, rely=.1, height=130, width=130)
#
#         def push_left_button(nothing):
#             what_select = line_list_box.curselection()
#             start = line_list_box.index(what_select)
#             start = int(start)
#             start += start  # make a start index of another file
#             finish = start+3  # make a finish index of another file
#
#             with open('TXT_files//Part2_credLineFile.txt', 'r') as file2:
#
#                 all_line_2 = file2.readlines()
#                 line_list_box_2 = Listbox()
#                 for i in all_line_2:
#                     line_list_box_2.insert(END, i)
#                 line_list_box_2.place(relx=.30, rely=.1, height=130, width=130)
#
#                 all_line_3 = line_list_box_2.get(start, finish)  # take start and finish data
#                 for i in all_line_3:
#                     line_list_box_2.insert(0, i)
#                 line_list_box_2.delete(4, END)  # delete all elements after 4 row
#
#         line_list_box.bind('<<ListboxSelect>>', push_left_button)
#         file.close()
#
# open_file()
# output.mainloop()

#! count for 2 on 4
# start += start  # make a start index of another file
# finish = start + 3  # (!change) make a finish index of another file