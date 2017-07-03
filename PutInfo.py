#! mode for add info
from tkinter import *
from tkinter import messagebox
from datetime import date
import os

# save information in file
def credit_line_save():
    b = os.path.exists('TXT_files')  # (D) make a check with 'file exist'
    if b == False:
        os.mkdir('TXT_files')
        messagebox.showinfo('Information', 'TXT_files folder created')
        q = open('TXT_files//credLineFile.txt', 'w')
        messagebox.showinfo('Information', 'credLineFile text file created')
        q.close()
        b = True
    if b == True:
        cred_line_fle = open('TXT_files//credLineFile.txt', 'a')

        # try mmap; or seek/read;
        # count = 0
        # count += 1
        # count = str(count)
        # cred_line_fle.write(str(count))
        # cred_line_fle.write(str(':'))

        cred_line_fle.write(str(creditLine_name.get()))
        cred_line_fle.write(str('\n'))  # (Q) maybe can realize it in another way?
        cred_line_fle.write(str(creditLine_date.get()))
        cred_line_fle.write(str('\n'))
        cred_line_fle.close()

def credit_line_part2_save():
    b = os.path.exists('TXT_files')  # (D) make a check with 'file exist'
    if b == False:
        os.mkdir('TXT_files')
        messagebox.showinfo('Information', 'TXT_files folder created')
        z = open('TXT_files//Part2_credLineFile.txt', 'w')
        messagebox.showinfo('Information', 'Part2_credLineFile text file created')
        z.close()
        b = True
    if b == True:
        cred_line_fle = open('TXT_files//Part2_credLineFile.txt', 'a')
        cred_line_fle.write(str(creditLine_Surname.get()))
        cred_line_fle.write(str('\n'))  # (Q) maybe can realize it in another way?
        cred_line_fle.write(str(creditLine_passport.get()))
        cred_line_fle.write(str('\n'))
        cred_line_fle.close()

# get date and put into entry (to use in first step)
def credit_line_date():
    today = date.today()
    creditLine_entry_date.insert(END, today)

# class for pledgor/guarantor (to use in second step)
class PledgorGuarntor:
    inFuture = 'addItLater'

put = Tk()
put.title("Add mode")
put.geometry("600x700+200+200")

# add info (first step)
creditLine_name = StringVar()
creditLine_entry_name = Entry(textvariable=creditLine_name)
creditLine_entry_name.place(relx=.12, rely=.1, height=25, width=130)

creditLine_date = StringVar()
creditLine_entry_date = Entry(textvariable=creditLine_date)
creditLine_entry_date.place(relx=.12, rely=.15, height=25, width=130)
credit_line_date()

labelName = Label(text="Name", fg="#eee", bg="#333")
labelName.place(relx=.01, rely=.1, height=25, width=50)
labelDate = Label(text="Date", fg="#eee", bg="#333")
labelDate.place(relx=.01, rely=.15, height=25, width=50)

creditLine_btn = Button(text='Save', height=1, width=20, command=credit_line_save)
creditLine_btn.place(relx=.12, rely=.2, height=30, width=130)

# for files (second step)
creditLine_Surname = StringVar()
creditLine_entry_surname = Entry(textvariable=creditLine_Surname)
creditLine_entry_surname.place(relx=.12, rely=.25, height=25, width=130)

creditLine_passport = StringVar()
creditLine_entry_passport = Entry(textvariable=creditLine_passport)
creditLine_entry_passport.place(relx=.12, rely=.30, height=25, width=130)

labelSurname = Label(text="Surname", fg="#eee", bg="#333")
labelSurname.place(relx=.01, rely=.25, height=25, width=50)
labelPassport = Label(text="Passport", fg="#eee", bg="#333")
labelPassport.place(relx=.01, rely=.30, height=25, width=50)

creditLine_btn2 = Button(text='Save', height=1, width=20, command=credit_line_part2_save)
creditLine_btn2.place(relx=.12, rely=.35, height=30, width=130)

put.mainloop()