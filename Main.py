#! main interface
from tkinter import *

#! (!) you have a 2 global variables (!)
#! dirs, cut_list_box

root = Tk()
root.title("Main")
root.geometry("600x700+200+200")

main_menu = Menu()

file_menu = Menu()
file_menu.add_command(label="View")
file_menu.add_command(label="Add")
file_menu.add_separator()
file_menu.add_command(label="Exit")

main_menu.add_cascade(label="Mode", menu=file_menu)
main_menu.add_cascade(label="About")

root.config(menu=main_menu)

root.mainloop()
