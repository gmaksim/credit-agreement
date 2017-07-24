#! temp .py file to check some part of code
from tkinter import *  # (TO-DO) import what's needed
from tkinter import messagebox
from datetime import date
import os
import sqlite3
import sys


# in test
# class ArrangeWidget:
#     def __init__(self, master):
#         self.master = master
#         print('test')
#
#     def arrange_name_labels(self, place_tk, list_with_names, step_down):  # step_down = 0.10 (example)
#         start = 0
#         stop = len(list_with_names)  # (TO-DO) check arrange_attribute, possible make func without fldrs?
#         labels_gc = []
#         while start != stop:
#             label_name = Label(place_tk, text=list_with_names[start], fg="#eee", bg="#333")
#             label_name.place(relx=step_down, rely=.10, height=25, width=150)
#             labels_gc.append(label_name)
#             start += 1
#
# class AddMode:
#     def __init__(self, master):
#         self.master = master
#         root.title("Add new information. Part 1")
#         root.geometry("600x700+100+100")
#
#         test = [1, 2, 3]
#         ArrangeWidget.arrange_name_labels(self, place_tk=root, list_with_names=test, step_down=0.1)
#
# if __name__ == "__main__":
#     root = Tk()
#     AddMode(root)
#     root.mainloop()


def arrange_name_labels(place_tk, list_with_names, step_down):  # step_down = 0.10 (example)
    start = 0
    stop = len(list_with_names)  # (TO-DO) check arrange_attribute, possible make func without fldrs?
    labels_gc = []
    x = 0.10
    while start != stop:
        label_name = Label(place_tk, text=list_with_names[start], fg="#eee", bg="#333")
        label_name.place(relx=.1, rely=x, height=25, width=150)
        labels_gc.append(label_name)
        x += step_down
        start += 1

root = Tk()
root.title("Add new information. Part 1")
root.geometry("600x700+100+100")

test = ['hgfh', 'hgf', 'fdfd']
arrange_name_labels(place_tk=root, list_with_names=test, step_down=0.1)
root.mainloop()
