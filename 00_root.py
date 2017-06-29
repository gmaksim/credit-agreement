#! main interface
from tkinter import *
from tkinter import messagebox
import os

#! import information in file
def credit_line_save():
    # make a check with "file exists - yes/no" and correct F/T folder check
    b = os.path.exists('TXT_files')
    if b == False:
        messagebox.showinfo('Information', 'TXT_files folder created')
        os.mkdir('TXT_files')
        b = True
    if b == True:
        cred_line_fle = open('TXT_files//credLineFile.txt', 'w')
        cred_line_fle.write(str(creditLine_data.get()))
        cred_line_fle.close()

# def credit_line_date():
#     # add function to insert current date

root = Tk()
root.title("Main")
root.geometry("600x700+200+200")

creditLine_data = StringVar()
creditLine_entry = Entry(textvariable=creditLine_data)
# creditLine_entry.place(relx=.1, rely=.1)
creditLine_entry.place(x=1, y=1)
creditLine_btn = Button(command=credit_line_save)
creditLine_btn.place(x=150, y=8)

# creditLineDate_entry = Entry()
# creditLineDate_entry.place(command=credit_line_date())

root.mainloop()