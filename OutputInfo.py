#! main interface
from tkinter import *
from tkinter import messagebox
import os


root = Tk()
root.title("Main")
root.geometry("600x700+200+200")

def open_file():
    with open('TXT_files//credLineFile.txt', 'r') as file:
        allLine = file.readlines()
        lineListBox = Listbox()

        for i in allLine:
            lineListBox.insert(END, i)
        lineListBox.grid(row=0, column=0)

        tex = Text(root, width=20, height=3, font="12", wrap=WORD)
        tex.grid(row=0, column=2, padx=20, pady=10)

        def push_left_button(WTF):

            whtSelect = lineListBox.curselection()
            b = lineListBox.index(whtSelect)
            b = int(b)

            if b == 1:
                tex.delete(1.0, END)
                tex.insert(END, "Some information")
            else:
                tex.delete(1.0, END)
                tex.insert(END, "nothing here")

        lineListBox.bind('<Double-Button-1>', push_left_button)
        file.close()


open_file()
root.mainloop()
