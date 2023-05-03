from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter.ttk import Treeview
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import mysql.connector
from pymongo import MongoClient
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

SQL_PW = "123" ## will replace with actual password during demo

engine = create_engine(f'mysql+mysqlconnector://root:{SQL_PW}@localhost/ALS')
connection = engine.connect()



def create_member():
    membercreation = pd.read_sql_query('SELECT DISTINCT(Membership_ID) FROM Membership', engine)
    ID = stringcreateID.get()
    NAME = stringcreateName.get()
    FACULTY = stringcreateFaculty.get()
    PHONE = stringcreatePhone.get()
    EMAIL = stringcreateEmail.get()
    
    if ID != "" and NAME != "" and FACULTY != "" and PHONE != "" and EMAIL != "":
        if ID not in str(membercreation.Membership_ID):
            mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
            cs = mydb.cursor()
            statement = 'INSERT INTO Membership(Membership_ID, Name, Faculty, Phone, Email) values (%s, %s, %s, %s, %s)'
            insert = (f'{ID}', f'{NAME}', f'{FACULTY}', f'{PHONE}', f'{EMAIL}')
            cs.execute(statement, insert)
            mydb.commit()
            mydb.close()

            member_creation_success()
        else:
            member_creation_error()
    else:
        member_creation_error()


#----------------------------------delete member function-------------------------------------------

def delete_member():
  checkloans = pd.read_sql_query('SELECT DISTINCT Membership_ID FROM Loan', engine)
  checkreservations = pd.read_sql_query('SELECT DISTINCT Membership_ID FROM Reserve', engine)
  checkfines = pd.read_sql_query('SELECT DISTINCT Membership_ID FROM Fine', engine)
  ID = stringID.get()
  if ID not in str(checkloans.Membership_ID) and ID not in str(checkreservations.Membership_ID) and ID not in str(checkfines.Membership_ID):
    member_deletion_confirm()
  else:
    member_deletion_error()


#---------------------------------confirm delete function------------------------------------

def confirm_delete():
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    membercreation = pd.read_sql_query('SELECT DISTINCT(Membership_ID) FROM Membership', engine)
    cs = mydb.cursor()
    ID = stringID.get()
    statement = 'DELETE FROM Membership WHERE Membership_ID=%s'
    insert = (f'{ID}',)
    cs.execute(statement, insert)
    mydb.commit()
    mydb.close()

#----------------update member function -------------------------------------------
def update_member():
    memberidonly = pd.read_sql_query('SELECT DISTINCT Membership_ID FROM Membership', engine)
    memberupdation= pd.read_sql_query('SELECT * FROM Membership', engine)
    inputID = member_ID_input.get() #!!!

    if inputID in str(memberidonly.Membership_ID):
        mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
        cs = mydb.cursor()

        statement = 'DELETE FROM Membership WHERE Membership_ID=%s'
        insert = (f'{inputID}',)
        cs.execute(statement, insert)

        PHONE = member_phone_input.get()
        NAME = member_name_input.get()
        FACULTY = member_faculty_input.get()
        EMAIL = member_email_input.get()

        #if inputID not in str(memberupdation.Membership_ID):
        if NAME != "" and FACULTY != "" and PHONE != "" and EMAIL != "":
            statement2 = 'INSERT INTO Membership(Membership_ID, Name, Faculty, Phone, Email) values (%s, %s, %s, %s, %s)'
            insert2 = (f'{inputID}', f'{NAME}', f'{FACULTY}', f'{PHONE}', f'{EMAIL}')
            cs.execute(statement2, insert2)
            mydb.commit()
            mydb.close()

            member_update_success()

        else: 
            member_update_error()

    else: 
        member_update_error()

#-----------------------------aquire book function------------------------------------------

def aquire_book():
    bookaquisition = pd.read_sql_query('SELECT DISTINCT(Accession_No) FROM Book', engine)
    ACC = stringAccNo.get()
    TITLE = stringTitle.get()
    AUTHORS = stringAuthors.get()
    ISBN = stringISBN.get()
    PUBLISHER = stringPublisher.get()
    PUBYEAR = stringPubYear.get()
    
    if ACC != "" and TITLE != "" and AUTHORS != "" and ISBN != "" and PUBLISHER != "" and PUBYEAR != "":
        if ACC not in str(bookaquisition.Accession_No):
            mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
            cs = mydb.cursor()
            statement = 'INSERT INTO Book(Accession_No, Title, Author, ISBN, Publisher, Publication_Year) values (%s, %s, %s, %s, %s, %s)'
            insert = (f'{ACC}', f'{TITLE}', f'{AUTHORS}', f'{ISBN}', f'{PUBLISHER}', f'{PUBYEAR}')
            cs.execute(statement, insert)
            mydb.commit()
            mydb.close()

            book_success()
        else:
            add_book_error()
    else:
        add_book_error()


#--------------------------withdraw book function---------------------------------------

def withdraw_book_func():
    checkloans = pd.read_sql_query('SELECT Accession_No FROM Loan', engine)
    checkreservations = pd.read_sql_query('SELECT Accession_No FROM Reserve', engine)
    bookwithdrawal = pd.read_sql_query('SELECT DISTINCT Accession_No FROM Book', engine)
    ACC = stringwithdrawAccNo.get()

    if ACC not in str(checkloans.Accession_No):
        if ACC not in str(checkreservations.Accession_No):
            confirm()
        else:
            reserved_error()
    else:
        on_loan_error()


#-----------------------confirm withdraw function---------------------------------

def confirm_withdraw():
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    membercreation = pd.read_sql_query('SELECT DISTINCT Accession_No FROM Book', engine)
    cs = mydb.cursor()
    ACC = stringwithdrawAccNo.get()
    statement = 'DELETE FROM Book WHERE Accession_No=%s'
    insert = (f'{ACC}',)
    cs.execute(statement, insert)
    mydb.commit()
    mydb.close()


#------------------------------fine payment------------------------------------------

def pay_fine():
    checkfines = pd.read_sql_query('SELECT DISTINCT Membership_ID FROM Fine', engine)
    ID = stringpaymentID.get()
    AMOUNT = stringpaymentamt.get()
    paymentID = f'"{ID}"'

    checkamount = pd.read_sql_query('SELECT Fine_Amount FROM Fine WHERE Membership_ID = {};'.format(paymentID), engine)

    if ID in str(checkfines.Membership_ID):
        if AMOUNT == str(checkamount.Fine_Amount[0]):
            cfrm()
        else:
            error45()
    else:
        error44()


#------------------------------confirm payment-----------------------------------------

def confirm_payment():
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    membercreation = pd.read_sql_query('SELECT DISTINCT Membership_ID FROM Fine', engine)
    cs = mydb.cursor()
    ID = stringpaymentID.get()
    statement = 'DELETE FROM Fine WHERE Membership_ID=%s'
    insert = (f'{ID}',)
    statement2 = 'INSERT INTO FinePayment values (%s, %s, %s)'
    insert2 = (f'{ID}', f'{datetime.date.today()}', f'{amount.Fine_Amount[0]}',)
    cs.execute(statement, insert)
    cs.execute(statement2, insert2)
    mydb.commit()
    mydb.close()


#------------------------------update loan to sql-----------------------------------------
def update_borrow(): #3 adding data to sql
    ID = strID.get()
    ACCNO = stringAccID.get()
    LOAN_ID = ID + ACCNO
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    statement = 'INSERT INTO Loan(Loan_ID, Accession_No, Borrow_Date, Due_Date, Membership_ID) values (%s, %s, %s, %s, %s)'
    today = date.today()
    #today = today.strftime("%Y-%m-%d")
    due = today + datetime.timedelta(days = 14)
    #due = due.strftime("%Y-%m-%d")
    insert = (f'{LOAN_ID}', f'{ACCNO}', today, due, f'{ID}')
    cs.execute(statement, insert)
    mydb.commit()
    mydb.close()

#------------------------------confirm borrow-----------------------------------------
def cfm_borrow(): 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ID = strID.get()
    ACCNO = stringAccID.get()
    checkloan = pd.read_sql_query('SELECT DISTINCT(Accession_No) FROM Loan', engine)

    checkquota = "SELECT Membership_ID FROM Loan WHERE Membership_ID = %s"
    insert = (f'{ID}',)
    cs.execute(checkquota, insert)
    record = cs.fetchall()

    fines = pd.read_sql_query('SELECT DISTINCT(Membership_ID) FROM Fine', engine).to_numpy()
    thisAcc = f'"{ACCNO}"'

    if ACCNO in str(checkloan.Accession_No):
        getduedate = pd.read_sql_query('SELECT Due_Date FROM Loan WHERE Accession_No = {};'.format(thisAcc), engine)
        duedate = str(getduedate.Due_Date[0])
        error001(duedate)
    elif len(record) >= 2:
        error002()
    elif ID in fines:
        error003()
    else: 
        ultimate_borrow(cfm_pg)

    #---------------------------- success borrow-----------------------------------------

def ultimate_borrow(cfm_pg): #after success  
    cfm_pg.destroy()
    update_borrow()


#------------------------------return success ----------------------------------------
def ultimate_return(cfm_pg): #if success return
    cfm_pg.destroy()
    update_return()

#------------------------------return success but have fine ----------------------------------------

def lousy_return(cfm_pg):
    cfm_pg.destroy()
    update_return()
    error004()

#------------------------------confirm book ----------------------------------------
def cfm_return(): #check if got fine
    accNO = stringAccNum.get()

    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()

    getid = "SELECT Membership_ID FROM Loan WHERE Accession_No = %s"
    insert = (f'{accNO}',)
    cs.execute(getid, insert)
    thisID = cs.fetchall()[0]

    checkfines = pd.read_sql_query('SELECT DISTINCT(Membership_ID) FROM Fine', engine).to_numpy()

    if thisID in checkfines:
        lousy_return(cfm_pg)
    else:
        ultimate_return(cfm_pg)


#------------------------------update loan on sql ----------------------------------------

def update_return():
    ACCNO = stringAccNum.get()
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    statement = 'DELETE FROM Loan WHERE Accession_No=%s'
    insert = (f'{ACCNO}',)
    cs.execute(statement, insert)
    mydb.commit()
    mydb.close()



#----------------book reservation function-------------------------------------------

def reserve_book():
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ID = stringMemberID.get()
    
    checkreservations = 'SELECT Membership_ID FROM Reserve WHERE Membership_ID=%s'
    insert = (f'{ID}',)
    cs.execute(checkreservations, insert)
    record = cs.fetchall()

    checkfines = pd.read_sql_query('SELECT DISTINCT(Membership_ID) FROM Fine', engine)
    ID = stringMemberID.get()

    if len(record) >= 2:
        error36()
    elif ID in str(checkfines.Membership_ID):
        error37()
    else:
        cfm35()

def confirm_reservation():
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ID = stringMemberID.get()
    ACCNO = stringReservationAccNo.get()
    RESERVE_DATE = str(date.today())

    statement = 'INSERT INTO Reserve(Membership_ID, Accession_No, Reserve_Date, Cancel_Status) values (%s, %s, %s, %s)'
    insert = (f'{ID}', f'{ACCNO}', f'{RESERVE_DATE}', 'N') 
    cs.execute(statement, insert)
    mydb.commit()
    mydb.close()


#----------------cancel reservation function-------------------------------------------

def reserve_cancellation():
    ##checkAccNo = pd.read_sql_query('SELECT Accession_No FROM Reserve', engine)
    ##checkID = pd.read_sql_query('SELECT Membership_ID FROM Reserve', engine)
    checkall = pd.read_sql_query('SELECT * FROM Reserve', engine)
    ACCNO = stringAccNo2.get()
    ID = stringMemberID2.get()
    flag = True

    for row in checkall.to_numpy():
        if ACCNO in row and ID in row:
            cfm39()
            flag = False
            break
    if flag:
        error40()

def confirm_cancellation():
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ACCNO = stringAccNo2.get()
    statement = 'DELETE FROM Reserve WHERE Accession_No=%s'
    insert = (f'{ACCNO}',)
    cs.execute(statement, insert)
    mydb.commit()
    mydb.close()


#----------------books on loan function-------------------------------------------
def display_books_on_loan():
    global reports_label, reportsmenu_button
    reports_pg = Toplevel() 
    reports_pg.title("Books on Loan Report")
    reports_label = Label(reports_pg, text = "Books on Loan Report", fg = "white", bg = "#413F54", padx = 400, pady = 50)

    #PLUS ALL THE SQL STUFF HERE 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    checkBooksOnLoan = pd.read_sql_query('SELECT Accession_No FROM Loan', engine).to_numpy()

    cs = mydb.cursor()
      
    reports_cols = ('Accession Number', 'Title', 'Author', 'ISBN', 'Publisher', 'Year')
    reports_table = Treeview(reports_pg, columns=reports_cols, show='headings')
    for col in reports_cols:
        reports_table.heading(col, text=col)
        reports_table.column(col, minwidth=0, width=120, stretch=NO)
        reports_table.grid(row=1, column=0, columnspan=6)

    result = []
    for book in checkBooksOnLoan:
        statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Accession_No = %s"
        insert = (f'{book[0]}',)
        cs.execute(statement, insert)
        result.append(cs.fetchall())


    for i in range(len(result)):
        reports_table.insert(parent = '', index = i, iid = i, values = result[i][0])


    reportsmenu_button = Button(reports_pg, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = reports_pg.destroy)
    reports_label.grid(row = 0, column = 0, columnspan = 3)
    reportsmenu_button.grid(row = 5, column =1)

#----------------members with fines function-------------------------------------------
def members_with_fines():
    global reports_label, reportsmenu_button
    reports_pg = Toplevel() 
    reports_pg.title("Members with Outstanding Fines")
    reports_label = Label(reports_pg, text = "Members with Outstanding Fines", fg = "white", bg = "#413F54", padx = 400, pady = 50)

    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    checkmembers = pd.read_sql_query('SELECT DISTINCT(Membership_ID) FROM Fine', engine).to_numpy()
    cs = mydb.cursor()

    reports_cols = ('Membership_ID', 'Name', 'Faculty', 'Phone Number', 'Email')
    reports_table = Treeview(reports_pg, columns=reports_cols, show='headings')
    for col in reports_cols:
        reports_table.heading(col, text=col)
        reports_table.column(col, minwidth=0, width=180, stretch=NO)
        reports_table.grid(row=1, column=0, columnspan=5)

    result = []
    for member in checkmembers:
        statement = "SELECT Membership_ID, Name, Faculty, Phone, Email FROM Membership WHERE Membership_ID = %s"
        insert = (f'{member[0]}',)
        cs.execute(statement, insert)
        #result.append(cs.fetchall())
        result += cs.fetchall()

    for i in range(len(result)):
        reports_table.insert(parent = '', index = i, iid = i, values = result[i])

    reportsmenu_button = Button(reports_pg, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = reports_pg.destroy)
    reports_label.grid(row = 0, column = 0, columnspan = 3)
    reportsmenu_button.grid(row = 5, column =1)


#----------------books on loan by member function-------------------------------------------
def search2(): 
    global search2_label, backtoloans_button 
    search2_pg = Toplevel()  
    search2_pg.title("Search Member") 
    search2_label = Label(search2_pg, text = "Books on Loan to Member", fg = "white", bg = "#413F54", padx = 500, pady = 50) 
    #PLUS ALL THE SQL STUFF HERE  
    backtosearch_button = Button(search2_pg, text = "Back to Search Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = search2_pg.destroy) 
 
    search2_label.grid(row = 0, column = 0, columnspan = 3) 
    backtosearch_button.grid(row = 10, column = 1) 
 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW) 
    # checkMember = pd.read_sql_query('SELECT Membership_ID FROM LOAN', engine).to_numpy() 
 
    cs = mydb.cursor() 

    acc = e_memberid.get()
    accno = f'"{acc}"'

    checkbooks = pd.read_sql_query('SELECT DISTINCT(Accession_No) FROM Loan WHERE Membership_ID = {};'.format(accno), engine).to_numpy()
    cs = mydb.cursor()

    reports_cols = ('Accession Number', 'Title', 'Author', 'ISBN', 'Publisher', 'Year')
    reports_table = Treeview(search2_pg, columns=reports_cols, show='headings')
    for col in reports_cols:
        reports_table.heading(col, text=col)
        reports_table.column(col, minwidth=0, width=180, stretch=NO)
        reports_table.grid(row=1, column=0, columnspan=5)

    result = []
    for book in checkbooks:
        statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Accession_No = %s"
        insert = (f'{book[0]}',)
        cs.execute(statement, insert)
        #result.append(cs.fetchall())
        result += cs.fetchall()

    for i in range(len(result)):
        reports_table.insert(parent = '', index = i, iid = i, values = result[i])


def display_books_on_reservation():
    global reports_label, reportsmenu_button
    reports_pg = Toplevel() 
    reports_pg.title("Books on Reservation Report")
    reports_label = Label(reports_pg, text = "Books on Reservation Report", fg = "white", bg = "#413F54", padx = 400, pady = 50)

    #PLUS ALL THE SQL STUFF HERE 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    checkAccNo = pd.read_sql_query('SELECT Accession_No FROM Reserve', engine).to_numpy()
    checkID = pd.read_sql_query('SELECT Membership_ID FROM Reserve', engine).to_numpy()
    cs = mydb.cursor()
      
    reports_cols = ('Accession Number', 'Title', 'Membership ID', 'Name')
    reports_table = Treeview(reports_pg, columns=reports_cols, show='headings')
    for col in reports_cols:
        reports_table.heading(col, text=col)
        reports_table.column(col, minwidth=0, width=220, stretch=NO)
        reports_table.grid(row=1, column=0, columnspan=6)

    result = []
    for data in checkAccNo:
        statement = "SELECT Accession_No, Title FROM Book WHERE Accession_No = %s"
        insert = (f'{data[0]}',)
        cs.execute(statement, insert)
        result.append(cs.fetchall())

    for i in range(len(checkID)):
        statement = "SELECT Membership_ID, Name FROM Membership WHERE Membership_ID = %s"
        insert = (f'{checkID[i][0]}',)
        cs.execute(statement, insert)
        result[i].append(cs.fetchall()[0])

    final = []
    for entry in result:
        entry = entry[0] + entry[1]
        final.append(entry)


    for i in range(len(result)):
        reports_table.insert(parent = '', index = i, iid = i, values = final[i])


    reportsmenu_button = Button(reports_pg, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = reports_pg.destroy)
    reports_label.grid(row = 0, column = 0, columnspan = 3)
    reportsmenu_button.grid(row = 5, column =1)




#------------------------------------------------------------------TINKERTIME-------------------------------------------------------------------------------------

root = Tk()

#------------------- change frame function-------------------
def change_frame(new_frame, old_frame):
    old_frame.forget()
    new_frame.pack(fill = 'both', expand=1)

#------------------------------------------------------------

#frames
main_menu_frame = Frame(root)
borrow_return_frame = Frame(root)
borrow_frame = Frame(root)
return_frame = Frame(root)
reserve_cancel_frame = Frame(root)
reservation_frame = Frame(root)
cancel_reservation_frame = Frame(root)
fines_frame = Frame(root)
payment_frame = Frame(root)
member_creation_frame = Frame(root)
member_update_frame = Frame(root)
member_deletion_frame = Frame(root)
option_select_frame = Frame(root)
books_select_frame = Frame(root)
book_acquisition_frame = Frame(root)
book_withdrawal_frame = Frame(root)
member_update_details_frame = Frame(root)
reports_frame = Frame(root)
reports_search_frame = Frame(root)
reports_loans_frame = Frame(root)
reports_reservation_frame = Frame(root)
reports_fines_frame = Frame(root)
reports_loan_member_frame = Frame(root)


main_menu_frame.pack(fill = 'both', expand = 1)

#-------------------------------main menu frame--------------------------------------------

main_label = Label(main_menu_frame, text = "A Library System", fg = "white", bg = "#413F54", padx = 300, pady = 50)

#pics

membership_pic = ImageTk.PhotoImage(Image.open("membershippic.png"))
membership_label = Label(main_menu_frame, image = membership_pic, padx = 50, pady = 50)

books_pic = ImageTk.PhotoImage(Image.open("bookspic.png"))
books_label = Label(main_menu_frame, image = books_pic, padx = 50, pady = 50)

loans_pic = ImageTk.PhotoImage(Image.open("loanspic.png"))
loans_label = Label(main_menu_frame, image = loans_pic, padx = 50, pady = 50)

reservations_pic = ImageTk.PhotoImage(Image.open("reservationpic.png"))
reservations_label = Label(main_menu_frame, image = reservations_pic, padx = 50, pady = 50)

fines_pic = ImageTk.PhotoImage(Image.open("finespic.png"))
fines_label = Label(main_menu_frame, image = fines_pic, padx = 50, pady = 50)

reports_pic = ImageTk.PhotoImage(Image.open("reportspic.png"))
reports_label = Label(main_menu_frame, image = reports_pic, padx = 50, pady = 50)

#words

membership_word = Button(main_menu_frame, text = "Membership", fg = "black", bg = "#413F54", padx = 50, pady = 10,  command = lambda: change_frame(option_select_frame, main_menu_frame))
books_word = Button(main_menu_frame, text = "Books", fg = "black", bg = "#413F54", padx = 50, pady = 10, command = lambda: change_frame(books_select_frame, main_menu_frame))
loans_word = Button(main_menu_frame, text = "Loans", fg = "black", bg = "#413F54", padx = 50, pady = 10, command = lambda: change_frame(borrow_return_frame, main_menu_frame))
reservations_word = Button(main_menu_frame, text = "Reservations", fg = "black", bg = "#413F54", padx = 50, pady = 10, command = lambda: change_frame(reserve_cancel_frame, main_menu_frame))
fines_word = Button(main_menu_frame, text = "Fines", fg = "black", bg = "#413F54", padx = 50, pady = 10, command = lambda: change_frame(fines_frame, main_menu_frame))
reports_word = Button(main_menu_frame, text = "Reports", fg = "black", bg = "#413F54", padx = 50, pady = 10, command = lambda: change_frame(reports_frame, main_menu_frame))

main_label.grid(row = 0, column =0, columnspan = 3)
main_label.config(font=("Arial", 30, "bold"))

membership_label.grid(row = 1, column =0)
books_label.grid(row = 1, column = 1)
loans_label.grid(row = 1, column = 2)

membership_word.grid(row = 2, column =0)
books_word.grid(row = 2, column = 1)
loans_word.grid(row = 2, column = 2)

reservations_label.grid(row = 3, column =0)
fines_label.grid(row = 3, column =1)
reports_label.grid(row = 3, column =2)

reservations_word.grid(row = 4, column =0)
fines_word.grid(row = 4, column =1)
reports_word.grid(row = 4, column =2)


#----------------Borrow/return frame (slide 24)-----------------------------------------
myLabel = Label(borrow_return_frame, text = "Select one of the Options below:", fg = "white", bg = "#413F54", padx = 300, pady = 50)
myLabel.config(font=("Arial", 20, "bold"))

myButtonb = Button(borrow_return_frame, text = "Book Borrowing", fg = "black", bg = "#8789C0", padx = 200, pady = 50, command = lambda: change_frame(borrow_frame, borrow_return_frame))
myButtonr = Button(borrow_return_frame, text = "Book Returning", fg = "black", bg = "#8789C0", padx = 200, pady = 50, command = lambda: change_frame(return_frame, borrow_return_frame))

myButtonback = Button(borrow_return_frame, text = "Back To Main Menu", fg = "black", bg = "#E5D4C0", padx = 400, pady = 20, command = lambda: change_frame(main_menu_frame, borrow_return_frame))

loanspic = ImageTk.PhotoImage(Image.open("loanspic.png"))
myLabelloanspic = Label(borrow_return_frame, image = loanspic, padx = 200, pady = 100)

myLabel.grid(row = 0, column =0, columnspan = 2)
myButtonb.grid(row = 1, column = 1)
myButtonr.grid(row = 2, column = 1)
myLabelloanspic.grid(row = 1, column =0, rowspan = 2)
myButtonback.grid(row = 3, column =0, columnspan = 2)

#----------------borrow frame (slide 25-29)----------------------------------------------
myLabel = Label(borrow_frame, text = "To Borrow a Book, Please Enter Information Below:", fg = "white", bg = "#413F54", padx = 200, pady = 50)
#myLabel.pack()
myLabel.grid(row = 0, column =0, columnspan = 2)
myLabel.config(font=("Arial", 20, "bold"))

label_accno = Label(borrow_frame, text = "Accession Number:", padx = 60, pady = 20)
#label_accno.pack()
label_memid = Label(borrow_frame, text = "Membership ID:", padx = 60, pady = 20)
#label_memid.pack()

label_accno.grid(row = 1, column =0)
label_memid.grid(row = 2, column =0)

stringAccID = StringVar()
accno = Entry(borrow_frame, width = 50, textvariable = stringAccID)
#accno.pack() 
#accno.insert(0, "Accession Number")
strID = StringVar()
memid = Entry(borrow_frame, width = 50, textvariable = strID)
#memid.pack()
#memid.insert(0, "Membership ID")

accno.grid(row = 1, column =1)
memid.grid(row = 2, column =1)

def borrow_book(): #1 need to confirm details before checking conditions 
    global cfm_pg, cfm_label, cfm_button1, cfm_button2
    cfm_pg = Toplevel() 
    cfm_pg.title("Book Borrowing")
    confirm_label = Label(cfm_pg, text = "Confirm Loan Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)

    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ID = strID.get()
    ACCNO = stringAccID.get()

    today = date.today()
    #today = today.strftime("%Y-%m-%d")
    due = today + datetime.timedelta(days = 14)
    #due = due.strftime("%Y-%m-%d")

    data = ''

    statement = "SELECT Accession_No, Title FROM Book WHERE Accession_No = %s"
    insert = (f'{ACCNO}',)
    cs.execute(statement, insert)
    records1 = cs.fetchall()

    for record in records1:
        data += str(record[0]) + "\n" + " " + "\n" + str(record[1]) + "\n" + " " + "\n" + str(today) + "\n" + " " + "\n"

    statement = "SELECT Membership_ID, Name FROM Membership WHERE Membership_ID = %s"
    insert = (f'{ID}',)
    cs.execute(statement, insert)
    records2 = cs.fetchall()

    #data = str(records1[0]) + "\n" + " " + "\n" + str(records1[1]) + "\n" + " " + "\n" + today.strftime("%Y-%m-%d") + "\n" + " " + "\n"# + str(records2[0]) + "\n" + " " + "\n" + str(records2[1]) + "\n" + " " + "\n" + due.strftime("%Y-%m-%d") 

    for record in records2:
        data += str(record[0]) + "\n" + " " + "\n" + str(record[1]) + "\n" + " " + "\n" + str(due) #due.strftime("%Y-%m-%d")

    #for record in records2:
    #   data += str(records[0]) + "\n" + " " + "\n" + str(records[1]) + "\n" + " " + "\n" + str(records[2]) + "\n" + " " + "\n" + str(records[3]) + "\n" + " " + "\n" +str(records[4]) 
    label = Label(cfm_pg, text= data, height=12)

    accession_label = Label(cfm_pg, text="Accession Number")
    book_title_label = Label(cfm_pg, text="Book Title")
    borrow_date_label = Label(cfm_pg, text="Borrow Date")
    member_id_label = Label(cfm_pg, text="Membership ID")
    member_name_label = Label(cfm_pg, text="Member Name")
    due_date_label = Label(cfm_pg, text="Due Date")

    cfm_button1 = Button(cfm_pg, text = "Confirm Loan", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [cfm_borrow()])
    cfm_button2 = Button(cfm_pg, text = "Back To Borrow Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = cfm_pg.destroy)

    confirm_label.grid(row = 0, column = 0, columnspan = 2)
    label.grid(row = 1, column = 1, rowspan = 6)
    cfm_button1.grid(row = 7, column = 0)
    cfm_button2.grid(row = 7, column = 1)
    accession_label.grid(column = 0, row = 1)
    book_title_label.grid(column = 0, row = 2)
    borrow_date_label.grid(column = 0, row = 3)
    member_id_label.grid(column = 0, row = 4)
    member_name_label.grid(column = 0, row = 5)
    due_date_label.grid(column = 0, row = 6)

    mydb.commit()
    mydb.close()


def error001(duedate):
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Book currently on Loan until:\n" + duedate, fg = "red", bg = "white", padx = 400, pady = 50) #pack()
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Borrow Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy) #pack()

    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0)

def error002():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Member Loan Quota Exceeded", fg = "red", bg = "white", padx = 400, pady = 50) #pack()
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Borrow Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy) #pack()
    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0)


def error003():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Member has Oustanding Fines", fg = "red", bg = "white", padx = 400, pady = 50) #pack()
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Borrow Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy) #pack()
    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0)


borrowbutton = Button(borrow_frame, text = "Borrow Book", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [borrow_book()]) #how to put many commands
#borrowbutton.pack()
menubutton = Button(borrow_frame, text = "Back To Loans Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(borrow_return_frame, borrow_frame))
#menubutton.pack()

borrowbutton.grid(row = 3, column = 0)
menubutton.grid(row = 3, column =1)

#----------------------------return frame(slide 30-32)----------------------------------
myLabel = Label(return_frame, text = "To Return a Book, Please Enter Information Below:", fg = "white", bg = "#413F54", padx = 200, pady = 50)
#myLabel.pack()
myLabel.grid(row = 0, column =0, columnspan = 2)
myLabel.config(font=("Arial", 20, "bold"))

label_accno = Label(return_frame, text = "Accession Number:", padx = 60, pady = 20)
#label_accno.pack()
label_returndate = Label(return_frame, text = "Return Date:", padx = 60, pady = 20)
#label_memid.pack()

label_accno.grid(row = 1, column =0)
label_returndate.grid(row = 2, column =0)

stringAccNum = StringVar()
accno = Entry(return_frame, width = 50, textvariable = stringAccNum)
#accno.pack() 
#accno.insert(0, "Accession Number")
#returndate = Entry(return_frame, width = 50)
returndate = Label(return_frame, text = date.today(), padx = 60, pady = 20)
#memid.pack()
#memid.insert(0, "Membership ID")

accno.grid(row = 1, column =1)
returndate.grid(row = 2, column =1)


def return_book():
    global cfm_pg, cfm_label, cfm_button1, cfm_button2
    cfm_pg = Toplevel() 
    cfm_pg.title("Book Returning")
    cfm_label = Label(cfm_pg, text = "Confirm Return Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)
    
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    accNO = stringAccNum.get()

    getloanid = "SELECT Loan_ID FROM Loan WHERE Accession_No = %s"
    insert = (f'{accNO}',)
    cs.execute(getloanid, insert)
    loanid = cs.fetchall()[0]
    loanid = str(loanid[0])

    getfine = "SELECT Fine_Amount FROM Fine WHERE Loan_ID = %s"
    insert = (f'{loanid}',)
    cs.execute(getfine, insert)
    allfines = cs.fetchall()

    if allfines:
        fineamt = str(allfines[0][0])
    else:
        fineamt = "0"

    getid = "SELECT Membership_ID FROM Loan WHERE Accession_No = %s"
    insert = (f'{accNO}',)
    cs.execute(getid, insert)
    thisID = cs.fetchall()[0]

    #loanID = pd.read_sql_query('SELECT * FROM Loan WHERE Accession_No = {}'.format(acc1), engine).at[0, 'Loan_ID']
    #fineamt = pd.read_sql_query('SELECT * FROM Fine WHERE Loan_ID = {}'.format(loan1), engine).at[0, 'Fine_Amount']
    #ID = pd.read_sql_query('SELECT * FROM Loan WHERE Accession_No = {}'.format(acc1), engine).at[0, 'Membership_ID']

    statement = "SELECT Accession_No, Title FROM Book WHERE Accession_No = %s"
    insert = (f'{accNO}',)
    cs.execute(statement, insert)
    records1 = cs.fetchall()

    statement = "SELECT Membership_ID, Name FROM Membership WHERE Membership_ID = %s"
    thatID = str(thisID[0])
    insert = (f'{thatID}',)
    cs.execute(statement, insert)
    records2 = cs.fetchall()

    today = date.today()

    records = records1[0] + records2[0]

    data = str(records[0]) + "\n" + " " + "\n" + str(records[1]) + "\n" + " " + "\n" + str(records[2]) + "\n" + " " + "\n" + str(records[3]) + "\n" + " " + "\n" + today.strftime("%Y-%m-%d") + "\n" + " " + "\n" + "$" + fineamt
    
    label = Label(cfm_pg, text=data, height=12)

    accession_label = Label(cfm_pg, text="Accession Number")
    book_title_label = Label(cfm_pg, text="Book Title")
    member_id_label = Label(cfm_pg, text="Membership ID")
    member_name_label = Label(cfm_pg, text="Member Name")
    return_date_label = Label(cfm_pg, text="Return Date")
    fine_label = Label(cfm_pg, text="Fine")


    cfm_button1 = Button(cfm_pg, text = "Confirm Return", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda : [cfm_return()])
    cfm_button2 = Button(cfm_pg, text = "Back To Return Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = cfm_pg.destroy)

    cfm_label.grid(row = 0, column = 0, columnspan = 2)
    label.grid(row = 1, column = 1, rowspan = 6)
    cfm_button1.grid(row = 7, column = 0)
    cfm_button2.grid(row = 7, column = 1)
    accession_label.grid(column = 0, row = 1)
    book_title_label.grid(column = 0, row = 2)
    member_id_label.grid(column = 0, row = 3)
    member_name_label.grid(column = 0, row = 4)
    return_date_label.grid(column = 0, row = 5)
    fine_label.grid(column = 0, row = 6)

    mydb.commit()
    mydb.close()

def error004():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Book returned successfully but has fines", fg = "red", bg = "white", padx = 400, pady = 50) #.pack()
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Return Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = error_pg.destroy) #.pack()
    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0)

returnbutton = Button(return_frame, text = "Return Book", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [return_book()]) #how to put many commands
#borrowbutton.pack()
menubutton = Button(return_frame, text = "Back To Loans Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(borrow_return_frame, return_frame))
#menubutton.pack()

returnbutton.grid(row = 3, column = 0)
menubutton.grid(row = 3, column =1)



#----------------Reserve/cancel frame (slide 33)-----------------------------------------
myLabel = Label(reserve_cancel_frame, text = "Select one of the Options below:", fg = "white", bg = "#413F54", padx = 300, pady = 50)
myLabel.config(font=("Arial", 20, "bold"))

myButtonb = Button(reserve_cancel_frame, text = "Book Reservation", fg = "black", bg = "#8789C0", padx = 20, pady = 50, width = 50, command = lambda: change_frame(reservation_frame, reserve_cancel_frame))
myButtonr = Button(reserve_cancel_frame, text = "Reservation Cancellation", fg = "black", bg = "#8789C0", padx = 20, pady = 50, width = 50, command = lambda: change_frame(cancel_reservation_frame, reserve_cancel_frame))
#myButtonr.pack()

myButtonback = Button(reserve_cancel_frame, text = "Back To Main Menu", fg = "black", bg = "#E5D4C0", padx = 400, pady = 20, command = lambda: change_frame(main_menu_frame, reserve_cancel_frame))
#myButtonback.pack()

reservationpic = ImageTk.PhotoImage(Image.open("reservationpic.png"))
myLabelreservationpic = Label(reserve_cancel_frame, image = reservationpic, padx = 200, pady = 100)
#myLabelp1 .pack()

myLabel.grid(row = 0, column =0, columnspan = 2)
myButtonb.grid(row = 1, column = 1)
myButtonr.grid(row = 2, column = 1)
myLabelreservationpic.grid(row = 1, column = 0, rowspan = 2)
myButtonback.grid(row = 3, column =0, columnspan = 2)



#----------------reservation frame (slide 34-37)----------------------------------------------
myLabel = Label(reservation_frame, text = "To Reserve a Book, Please Enter Information Below:", fg = "white", bg = "#413F54", padx = 400, pady = 50)
#myLabel.pack()
myLabel.grid(row = 0, column =0, columnspan = 2)

label_accno = Label(reservation_frame, text = "Accession Number:", padx = 60, pady = 20)
#label_accno.pack()
label_memid = Label(reservation_frame, text = "Membership ID:", padx = 60, pady = 20)
#label_memid.pack()
label_reservedate = Label(reservation_frame, text = "Reserve Date:", padx = 60, pady = 20)
#label_accno.pack()

label_accno.grid(row = 1, column =0)
label_memid.grid(row = 2, column =0)
label_reservedate.grid(row = 3, column = 0)

stringReservationAccNo = StringVar()
accno = Entry(reservation_frame, width = 50, textvariable = stringReservationAccNo)
#accno.pack() 
#accno.insert(0, "Accession Number")
stringMemberID = StringVar()
memid = Entry(reservation_frame, width = 50, textvariable = stringMemberID)
#memid.pack()
#memid.insert(0, "Membership ID")

stringReserveDate = StringVar()
#reservedate = Entry(reservation_frame, width = 50, textvariable = stringReserveDate)

date = date.today()
reservedate = Label(reservation_frame, text = f"{date}", width = 50)

accno.grid(row = 1, column =1)
memid.grid(row = 2, column =1)
reservedate.grid(row = 3, column = 1)

def cfm35():
    global cfm_label, cfm_button1, cfm_button2
    cfm_pg = Toplevel() 
    cfm_pg.title("Book Reservation")
    cfm_label = Label(cfm_pg, text = "Confirm Reservation Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ACCNO = stringReservationAccNo.get()
    ID = stringMemberID.get()
    data = ''
    today = date.today()

    #PLUS ALL THE SQL STUFF HERE 
    statement = "SELECT Accession_No, Title FROM Book WHERE Accession_No = %s"
    insert = (f'{ACCNO}',)
    cs.execute(statement, insert)
    records1 = cs.fetchall()

    for record in records1:
        data += str(record[0]) + "\n" + " " + "\n" + str(record[1]) + "\n" + " " + "\n"

    statement = "SELECT Membership_ID, Name FROM Membership WHERE Membership_ID = %s"
    insert = (f'{ID}',)
    cs.execute(statement, insert)
    records2 = cs.fetchall()


    for record in records2:
        data += str(record[0]) + "\n" + " " + "\n" + str(record[1]) + "\n" + " " + "\n" + str(today)

    #for record in records2:
    # data += str(records[0]) + "\n" + " " + "\n" + str(records[1]) + "\n" + " " + "\n" + str(records[2]) + "\n" + " " + "\n" + str(records[3]) + "\n" + " " + "\n" +str(records[4]) 
    label = Label(cfm_pg, text= data, height=10)

    book_accno_label = Label(cfm_pg, text="Accession Number")
    book_title_label = Label(cfm_pg, text="Book Title")
    member_ID_label = Label(cfm_pg, text="Membership ID")
    member_name_label = Label(cfm_pg, text="Member Name")
    reserve_date_label = Label(cfm_pg, text="Reserve Date")

    cfm_button1 = Button(cfm_pg, text = "Confirm Reservation", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [destroyer2(cfm_pg)])
    cfm_button2 = Button(cfm_pg, text = "Back To Reservation Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = cfm_pg.destroy)

    cfm_label.grid(row = 0, column = 0, columnspan = 2)
    label.grid(row = 1, column = 1, rowspan = 5)
    cfm_button1.grid(row = 6, column = 0)
    cfm_button2.grid(row = 6, column = 1)
    book_accno_label.grid(column = 0, row = 1)
    book_title_label.grid(column = 0, row = 2)
    member_ID_label.grid(column = 0, row = 3)
    member_name_label.grid(column = 0, row = 4)
    reserve_date_label.grid(column = 0, row = 5)

    mydb.commit()
    mydb.close()



def destroyer2(confirm_page):
    confirm_page.destroy()
    confirm_reservation()


def error36():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Member currently has 2 Books on Reservation", fg = "red", bg = "white", padx = 400, pady = 50)
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Reserve Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy)

    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0, columnspan = 2)

def error37():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    ID = stringMemberID.get()

    memberID = f'"{ID}"'
    checkpaymentAmount = pd.read_sql_query('SELECT * FROM FinePayment WHERE Membership_ID = {}'.format(memberID), engine)
    paymentAmount = checkpaymentAmount.at[0, 'Payment_Amount']
    ##db = pd.read_sql_query('SELECT * FROM Fine', engine)
    ##fineAmt = db.at[, 'Fine_Amount']
    
    error_label = Label(error_pg, text = f"Member has Outstanding Fine of: ${paymentAmount}", fg = "red", bg = "white", padx = 400, pady = 50)
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Reserve Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy)

    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0, columnspan = 2)


reservebutton = Button(reservation_frame, text = "Reserve Book", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [reserve_book()]) #how to put many commands
reservemenubutton = Button(reservation_frame, text = "Back To Reservations Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reserve_cancel_frame, reservation_frame))

reservebutton.grid(row = 4, column = 0)
reservemenubutton.grid(row = 4, column =1)

#----------------cancel_reservation_frame (slide 37-)----------------------------------------------

myLabel = Label(cancel_reservation_frame, text = "To Cancel a Reservation, Please Enter Information Below:", fg = "white", bg = "#413F54", padx = 400, pady = 50)
#myLabel.pack()
myLabel.grid(row = 0, column =0, columnspan = 2)

label_accno = Label(cancel_reservation_frame, text = "Accession Number:", padx = 60, pady = 20)
#label_accno.pack()
label_memid = Label(cancel_reservation_frame, text = "Membership ID:", padx = 60, pady = 20)
#label_memid.pack()
label_canceldate = Label(cancel_reservation_frame, text = "Cancel Date:", padx = 60, pady = 20)
#label_canceldate.pack()

label_accno.grid(row = 1, column =0)
label_memid.grid(row = 2, column =0)
label_canceldate.grid(row = 3, column =0)

stringAccNo2 = StringVar()
accno = Entry(cancel_reservation_frame, width = 50, textvariable = stringAccNo2)
#accno.pack() 
stringMemberID2 = StringVar()
memid = Entry(cancel_reservation_frame, width = 50, textvariable = stringMemberID2)
#memid.pack()
date = date.today()
canceldate = Label(cancel_reservation_frame, text = f"{date}", width = 50)

accno.grid(row = 1, column =1)
memid.grid(row = 2, column =1)
canceldate.grid(row = 3, column =1)


def cfm39():
  global cfm_label, cfm_button1, cfm_button2
  cfm_pg = Toplevel() 
  cfm_pg.title("Cancel Reservation")
  cfm_label = Label(cfm_pg, text = "Confirm Cancellation Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)
  mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
  cs = mydb.cursor()
  ACCNO = stringAccNo2.get()
  ID = stringMemberID2.get()
  data = ''
  today = date.today()

  #PLUS ALL THE SQL STUFF HERE 
  statement = "SELECT Accession_No, Title FROM Book WHERE Accession_No = %s"
  insert = (f'{ACCNO}',)
  cs.execute(statement, insert)
  records1 = cs.fetchall()

  for record in records1:
    data += str(record[0]) + "\n" + " " + "\n" + str(record[1]) + "\n" + " " + "\n"

  statement = "SELECT Membership_ID, Name FROM Membership WHERE Membership_ID = %s"
  insert = (f'{ID}',)
  cs.execute(statement, insert)
  records2 = cs.fetchall()

  for record in records2:
    data += str(record[0]) + "\n" + " " + "\n" + str(record[1]) + "\n" + " " + "\n" + str(today)

#for record in records2:
# data += str(records[0]) + "\n" + " " + "\n" + str(records[1]) + "\n" + " " + "\n" + str(records[2]) + "\n" + " " + "\n" + str(records[3]) + "\n" + " " + "\n" +str(records[4]) 

  label = Label(cfm_pg, text=data, height=10)
  book_accno_label = Label(cfm_pg, text="Accession Number")
  book_title_label = Label(cfm_pg, text="Book Title")
  member_ID_label = Label(cfm_pg, text="Membership ID")
  member_name_label = Label(cfm_pg, text="Member Name")
  cancellation_date_label = Label(cfm_pg, text="Cancellation Date")

  cfm_button1 = Button(cfm_pg, text = "Confirm Cancellation", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [destroyer3(cfm_pg)])
  cfm_button2 = Button(cfm_pg, text = "Back To Cancellation Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = cfm_pg.destroy)

  cfm_label.grid(row = 0, column = 0, columnspan = 2)
  label.grid(row = 1, column = 1, rowspan = 5)
  cfm_button1.grid(row = 6, column = 0)
  cfm_button2.grid(row = 6, column = 1)
  book_accno_label.grid(column = 0, row = 1)
  book_title_label.grid(column = 0, row = 2)
  member_ID_label.grid(column = 0, row = 3)
  member_name_label.grid(column = 0, row = 4)
  cancellation_date_label.grid(column = 0, row = 5)

  mydb.commit()
  mydb.close()


def destroyer3(confirm_page):
    confirm_page.destroy()
    confirm_cancellation()

def error40():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error")
  error_label = Label(error_pg, text = "Member has no such reservation.", fg = "red", bg = "white", padx = 400, pady = 50) #pack()
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Cancellation Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy) #pack()

  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0, columnspan = 2)



cancelbutton = Button(cancel_reservation_frame, text = "Cancel Reservation", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [reserve_cancellation()]) #how to put many commands
#borrowbutton.pack()
menubutton = Button(cancel_reservation_frame, text = "Back To Reservations Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reserve_cancel_frame, cancel_reservation_frame))
#menubutton.pack()

cancelbutton.grid(row = 4, column = 0)
menubutton.grid(row = 4, column =1)



#---------------------fines frame ()---------------------------------------------------

myLabel = Label(fines_frame, text = "Select one of the Options below:", fg = "white", bg = "#413F54", padx = 300, pady = 50)
myLabel.config(font=("Arial", 20, "bold"))

myButtonp = Button(fines_frame, text = "Fine Payment", fg = "black", bg = "#8789C0", padx = 200, pady = 50, command = lambda: change_frame(payment_frame, fines_frame))

myButtonback = Button(fines_frame, text = "Back To Main Menu", fg = "black", bg = "#E5D4C0", padx = 400, pady = 20, command = lambda: change_frame(main_menu_frame, fines_frame))
#myButtonback.pack()


finespic = ImageTk.PhotoImage(Image.open("finespic.png"))
myLabelfinespic = Label(fines_frame, image = finespic, padx = 200, pady = 100)
#myLabelp1.pack()

myLabel.grid(row = 0, column =0, columnspan = 2)
myButtonp.grid(row = 1, column = 1)
myLabelfinespic.grid(row = 1, column = 0)
myButtonback.grid(row = 2, column =0, columnspan = 2)


#----------------payment frame (slide 43-45)----------------------------------------------
myLabel = Label(payment_frame, text = "To Pay a Fine, Please Enter Information Below:", fg = "white", bg = "#413F54", padx = 200, pady = 50)
#myLabel.pack()
myLabel.grid(row = 0, column =0, columnspan = 2)

label_memid = Label(payment_frame, text = "Membership ID:", padx = 60, pady = 20)
#label_memid.pack()
label_paymentdate = Label(payment_frame, text = "Payment Date:", padx = 60, pady = 20)
#label_paymentdate.pack()
label_paymentamt = Label(payment_frame, text = "Payment Amount:", padx = 60, pady = 20)
#label_paymentamt.pack()

label_memid.grid(row = 1, column =0)
label_paymentdate.grid(row = 2, column =0)
label_paymentamt.grid(row = 3, column = 0)

stringpaymentID = StringVar()
memid = Entry(payment_frame, width = 50, textvariable = stringpaymentID)
paymentdate = Label(payment_frame, text = datetime.date.today())
stringpaymentamt = StringVar()
paymentamt = Entry(payment_frame, width = 50, textvariable = stringpaymentamt)
#paymentamt.pack() 

memid.grid(row = 1, column =1)
paymentdate.grid(row = 2, column =1)
paymentamt.grid(row = 3, column = 1)

def combinepay(cfm_pg):
    confirm_payment()
    cfm_pg.destroy()

def cfrm():
    global cfm_label, cfm_button1, cfm_button2, amount
    cfm_pg = Toplevel() 
    cfm_pg.title("Fine Payment")
    cfm_label = Label(cfm_pg, text = "Please Confirm Details To Be Correct", fg = "white", bg = "#413F54", padx = 200, pady = 50)

    #PLUS ALL THE SQL STUFF HERE 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ID = stringpaymentID.get()
    paymentID = f'"{ID}"'
    amount = pd.read_sql_query('SELECT Fine_Amount FROM Fine WHERE Membership_ID = {};'.format(paymentID), engine)
    fine_amount_label = Label(cfm_pg, text="Payment Due: $" + str(amount.Fine_Amount[0]))
    statement = "SELECT Membership_ID FROM Fine WHERE Membership_ID = %s"
    insert = (f'{ID}',)
    cs.execute(statement, insert)

    fine_ID_label = Label(cfm_pg, text="Member ID: " + str(ID))
    fine_date_label = Label(cfm_pg, text="Payment Date: " + str(datetime.date.today()))
    fine_label = Label(cfm_pg, text="EXACT AMOUNT ONLY")

    fine_amount_label.grid(row = 1, column = 0)
    fine_ID_label.grid(row = 1, column = 1)
    fine_date_label.grid(row = 2, column = 1)
    fine_label.grid(row = 2, column = 0)

    cfm_button1 = Button(cfm_pg, text = "Confirm Payment", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [combinepay(cfm_pg)])
    cfm_button2 = Button(cfm_pg, text = "Back To Payment Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = cfm_pg.destroy)

    cfm_label.grid(row = 0, column = 0, columnspan = 2)
    cfm_button1.grid(row = 3, column = 0)
    cfm_button2.grid(row = 3, column = 1)
    mydb.commit()
    mydb.close()




def error44():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Member has no fine", fg = "red", bg = "white", padx = 400, pady = 50)
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Payment Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy)

    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0)

def error45():
    global error_label, error_button
    error_pg = Toplevel() 
    error_pg.title("Error")
    error_label = Label(error_pg, text = "Incorrect fine payment amount", fg = "red", bg = "white", padx = 400, pady = 50)
    #PLUS ALL THE SQL STUFF HERE 
    error_button = Button(error_pg, text = "Back to Payment Function", fg = "black", bg = "white", padx = 50, pady = 20, command = error_pg.destroy)

    error_label.grid(row = 0, column = 0, columnspan = 2)
    error_button.grid(row = 1, column = 0)


paybutton = Button(payment_frame, text = "Pay Fine", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [pay_fine()]) #how to put many commands
finesmenubutton = Button(payment_frame, text = "Back To Fines Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(fines_frame, payment_frame))

paybutton.grid(row = 4, column = 0)
finesmenubutton.grid(row = 4, column =1)

#---------------------------MEMBERSHIP: Membership Option selection frame------------------------------------------------- 
select_option_label = Label(option_select_frame, text="Select one of the options below:", fg="white", bg="#413F54", width=30, height=2, 
  borderwidth=1, relief=SOLID, padx=300, pady=30)
select_option_label.grid(column=0, row=0, columnspan=2)
select_option_label.config(font=("Arial", 20, "bold")) 


select_option_creation = Button(option_select_frame, text="1. Membership Creation", fg = "black", bg = "#8789C0", width=20, padx=200, pady=50, 
                command=lambda: change_frame(member_creation_frame, option_select_frame))
select_option_creation.grid(column=1, row=1)

select_option_update = Button(option_select_frame, text="2. Membership Update", fg = "black", bg = "#8789C0", width=20, padx=200, pady=50,
                command=lambda: change_frame(member_update_frame, option_select_frame))
select_option_update.grid(column=1, row=2)

select_option_delete = Button(option_select_frame, text="3. Membership Deletion", fg = "black", bg = "#8789C0", width=20, padx=200, pady=50,
                command=lambda: change_frame(member_deletion_frame, option_select_frame))
select_option_delete.grid(column=1, row=3)

return_to_main_menu = Button(option_select_frame, text="Back to Main Menu", fg="black", bg="#E5D4C0", padx=400, pady=20, command = lambda: change_frame(main_menu_frame, option_select_frame))
return_to_main_menu.grid(column=0, row=4, columnspan=2)


membershippic = ImageTk.PhotoImage(Image.open("membershippic.png"))
myLabelmembershippic = Label(option_select_frame, image = membershippic, padx = 200, pady = 100)
#myLabelp1.pack()
myLabelmembershippic.grid(row = 1, column = 0, rowspan=3)

# Membership Creation

#popup if can create member
def member_creation_success():
 success_pg = Toplevel()
 success_pg.title("Success")
 success_label = Label(success_pg, text = "ALS Membership created.",
    fg = "white", bg = "green", padx = 400, pady = 50)
 success_button = Button(success_pg, text = "Back to Create Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = success_pg.destroy)
 success_label.grid(row = 0, column = 0, columnspan = 2)
 success_button.grid(row = 1, column = 0, columnspan = 2)

#popup if cannot create member
def member_creation_error():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error!")
  error_label = Label(error_pg, text = "Member already exist; Missing or Incomplete fields.", 
      fg = "yellow", bg = "red", padx = 400, pady = 50) 
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Create Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = error_pg.destroy)
  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0, columnspan = 2)


member_creation_label = Label(member_creation_frame, text="To Create Member, Please Enter Requested Information Below:", fg="white", bg="#413F54", width=30, height=1, borderwidth=1, relief=SOLID, padx=250, pady=30)
member_creation_label.grid(column=0, row=0, columnspan=4, padx=(50,10), pady=(10,10))

member_ID_label = Label(member_creation_frame, text="Membership ID", height=2)
member_ID_label.grid(column=1, row=1, padx=(10,50), pady=(10,10))

stringcreateID = StringVar()
member_ID_input = Entry(member_creation_frame, width=20, textvariable=stringcreateID)
member_ID_input.grid(column=2, row=1, padx=(10,50), pady=(10,10))
member_ID_input.focus()

member_name_label = Label(member_creation_frame, text="Name", height=2)
member_name_label.grid(column=1, row=2, padx=(10,50), pady=(10,10))

stringcreateName = StringVar()
member_name_input = Entry(member_creation_frame, width=20, textvariable=stringcreateName)
member_name_input.grid(column=2, row=2, padx=(10,50), pady=(10,10))
member_name_input.focus()

member_faculty_label = Label(member_creation_frame, text="Faculty", height=2)
member_faculty_label.grid(column=1, row=3, padx=(10,50), pady=(10,10))

stringcreateFaculty = StringVar()
member_faculty_input = Entry(member_creation_frame, width=20, textvariable=stringcreateFaculty)
member_faculty_input.grid(column=2, row=3, padx=(10,50), pady=(10,10))
member_faculty_input.focus()

member_phone_label = Label(member_creation_frame, text="Phone Number", height=2)
member_phone_label.grid(column=1, row=4, padx=(10,50), pady=(10,10))

stringcreatePhone = StringVar()
member_phone_input = Entry(member_creation_frame, width=20, textvariable=stringcreatePhone)
member_phone_input.grid(column=2, row=4, padx=(10,50), pady=(10,10))
member_phone_input.focus()
member_faculty_label = Label(member_creation_frame, text="Email Address", height=2)
member_faculty_label.grid(column=1, row=5, padx=(10,50), pady=(10,10))

stringcreateEmail = StringVar()
member_email_input = Entry(member_creation_frame, width=20, textvariable=stringcreateEmail)
member_email_input.grid(column=2, row=5, padx=(10,50), pady=(10,10))
member_email_input.focus()

create_member_button = Button(member_creation_frame, text="Create Member", fg="black", bg="#E5D4C0", padx=40, pady=10, command = lambda: [create_member()])
create_member_button.grid(column=1, row=6, padx=(10,50), pady=(10,10))

return_to_main_menu = Button(member_creation_frame, text="Back to Main Menu", fg="black", bg="#E5D4C0", padx=40, pady=10, command = lambda: change_frame(main_menu_frame, member_creation_frame))
return_to_main_menu.grid(column=2, row=6, padx=(10,50), pady=(10,10))


# Membership Deletion]

def combinedelete(confirm_pg):
    confirm_delete()
    confirm_pg.destroy()

#popup if can delete member
def member_deletion_confirm(): 
    global confirm_label, confirm_button1, confirm_button2
    confirm_pg = Toplevel() 
    confirm_pg.title("Confirm Deletion")
    confirm_label = Label(confirm_pg, text = "Please Confirm Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)
    
    #PLUS ALL THE SQL STUFF HERE 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ID = stringID.get()
    statement = "SELECT Membership_ID, Name, Faculty, Phone, Email FROM Membership WHERE Membership_ID = %s"
    insert = (f'{ID}',)
    cs.execute(statement, insert)
    records = cs.fetchall()
    printrecords = ''
    for records in records:
        printrecords += str(records[0]) + "\n" + " " + "\n" + str(records[1]) + "\n" + " " + "\n" + str(records[2]) + "\n" + " " + "\n" + str(records[3]) + "\n" + " " + "\n" +str(records[4]) 
    label = Label(confirm_pg, text=printrecords, height=10)


    member_ID_label = Label(confirm_pg, text="Member ID")
    member_name_label = Label(confirm_pg, text="Name")
    member_faculty_label = Label(confirm_pg, text="Faculty")
    member_phone_label = Label(confirm_pg, text="Phone Number")
    member_email_label = Label(confirm_pg, text="Email Address")


    confirm_button1 = Button(confirm_pg, text = "Confirm Deletion", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [combinedelete(confirm_pg)])
    confirm_button2 = Button(confirm_pg, text = "Back To Delete Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = confirm_pg.destroy)  

    confirm_label.grid(row = 0, column = 0, columnspan = 2)
    label.grid(row = 1, column = 1, rowspan = 5)
    confirm_button1.grid(row = 6, column = 0)
    confirm_button2.grid(row = 6, column = 1)
    member_ID_label.grid(column = 0, row = 1)
    member_name_label.grid(column = 0, row = 2)
    member_faculty_label.grid(column = 0, row = 3)
    member_phone_label.grid(column = 0, row = 4)
    member_email_label.grid(column = 0, row = 5)

    mydb.commit()
    mydb.close()


#popup if cannot delete member
def member_deletion_error():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error!")
  error_label = Label(error_pg, text = "Member has loans, reservations or outstanding fines.", 
      fg = "yellow", bg = "red", padx = 400, pady = 50) 
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Delete Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = error_pg.destroy)
  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0, columnspan = 2)

member_deletion_label = Label(member_deletion_frame, text="To Delete Member, Please Enter Membership ID:", fg="white", bg="#413F54", width=30, height=1, borderwidth=1, relief=SOLID, padx=250, pady=30)
member_deletion_label.grid(column=0, row=0, columnspan=4)

member_ID_label = Label(member_deletion_frame, text="Membership ID", height=3)
member_ID_label.grid(column=1, row=3)

stringID = StringVar()
member_ID_input = Entry(member_deletion_frame, width=20, textvariable=stringID)
member_ID_input.grid(column=2, row=3)
member_ID_input.focus()

delete_member_button = Button(member_deletion_frame, text="Delete Member", fg="black", bg="#E5D4C0", padx=40, pady=10, command = lambda: [delete_member()])
delete_member_button.grid(column=1, row=6)

return_to_membership_menu = Button(member_deletion_frame, text="Back to Membership Menu", fg="black", bg="#E5D4C0", padx=40, pady=10, command=lambda: change_frame(option_select_frame, member_deletion_frame))
return_to_membership_menu.grid(column=2, row=6)

# Membership Update first frame 

member_deletion_label = Label(member_update_frame, text="To Update a Member, Please Enter Membership ID:", fg="white", bg="#413F54", width=30, height=1, borderwidth=1, relief=SOLID, padx=250, pady=30)
member_deletion_label.grid(column=0, row=0, columnspan=4)

member_ID_label = Label(member_update_frame, text="Membership ID", height=3)
member_ID_label.grid(column=1, row=3)

member_ID_input = Entry(member_update_frame, width=20)
member_ID_input.grid(column=2, row=3)
member_ID_input.focus()

update_member_button = Button(member_update_frame, text="Update Member", fg="black", bg="#E5D4C0", padx=40, pady=10, command=lambda: change_frame(member_update_details_frame, member_update_frame))
update_member_button.grid(column=1, row=6)

return_to_membership_menu = Button(member_update_frame, text="Back to Membership Menu", fg="black", bg="#E5D4C0", padx=40, pady=10, command=lambda: change_frame(option_select_frame, member_update_frame))
return_to_membership_menu.grid(column=2, row=6)

def devastator():
    confirm_pg.destroy()
    update_member()

# Membership Update second frame
def member_update_confirm(): 
  global confirm_pg, confirm_label, confirm_button1, confirm_button2
  confirm_pg = Toplevel() 
  confirm_pg.title("Confirm Deletion")
  confirm_label = Label(confirm_pg, text = "Please Confirm Update Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)

  #PLUS ALL THE SQL STUFF HERE 
  mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
  cs = mydb.cursor()
  ID = member_ID_input.get() #!!!
  NAME = member_name_input.get()
  FACULTY = member_faculty_input.get()
  PHONE = member_phone_input.get()
  EMAIL = member_email_input.get()
  statement = "SELECT Membership_ID, Name, Faculty, Phone, Email FROM Membership WHERE Membership_ID = %s"
  insert = (f'{ID}',)
  cs.execute(statement, insert)

  #records = cs.fetchall()
  printrecords = str(NAME + "" + "\n" + "" + FACULTY + "" + "\n" + "" + PHONE + "" + "\n" + "" + EMAIL)

  label = Label(confirm_pg, text = printrecords)

  member_ID_label = Label(confirm_pg, text="Member ID")
  member_name_label = Label(confirm_pg, text="Name")
  member_faculty_label = Label(confirm_pg, text="Faculty")
  member_phone_label = Label(confirm_pg, text="Phone Number")
  member_email_label = Label(confirm_pg, text="Email Address")

  confirm_button1 = Button(confirm_pg, text = "Confirm Update", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = devastator)
  confirm_button2 = Button(confirm_pg, text = "Back To Update Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = confirm_pg.destroy)

  confirm_label.grid(row = 0, column = 0, columnspan = 2)
  confirm_button1.grid(row = 6, column = 0)
  confirm_button2.grid(row = 6, column = 1)

  member_ID_label.grid(column = 0, row = 1)
  member_name_label.grid(column = 0, row = 2)
  member_faculty_label.grid(column = 0, row = 3)
  member_phone_label.grid(column = 0, row = 4)
  member_email_label.grid(column = 0, row = 5)
  label.grid(row = 2, column = 1, rowspan = 4)

  ID_input = Label(confirm_pg, text = ID) 
  ID_input.grid(row = 1, column = 1)

  mydb.commit()
  mydb.close()

def destroyer():
  confirm_pg.destroy()
  success_pg.destroy()
  

#popup if can update member
def member_update_success():
 global success_pg, success_label, success_button, create_another_member_button
 success_pg = Toplevel()
 success_pg.title("Success")
 success_label = Label(success_pg, text = "ALS Membership updated.",
    fg = "white", bg = "#413F54", padx = 400, pady = 50)
 create_another_member_button = Button(success_pg, text = "Create Another Member",
   fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = destroyer)
 success_button = Button(success_pg, text = "Back to Update Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = success_pg.destroy)
 success_label.grid(row = 0, column = 0, columnspan = 2)
 create_another_member_button.grid(row = 1, column = 0)
 success_button.grid(row = 1, column = 1)


#popup if cannot create member
def member_update_error():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error!")
  error_label = Label(error_pg, text = "Missing or incomplete fields.", 
      fg = "yellow", bg = "red", padx = 400, pady = 50) 
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Update Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = error_pg.destroy)
  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0)


member_update_label = Label(member_update_details_frame, text="Please Enter Requested Information Below", fg="white", bg="#413F54", width=30, height=1, borderwidth=1, relief=SOLID, padx=250, pady=30)
member_update_label.grid(column=0, row=0, columnspan=4)

member_ID_label = Label(member_update_details_frame, text="Membership ID", height=2)
member_ID_label.grid(column=1, row=1)

#member_ID_input = Entry(member_update_details_frame, width=20)
#member_ID_input.grid(column=2, row=1)
#member_ID_input.focus()

member_name_label = Label(member_update_details_frame, text="Name", height=2)
member_name_label.grid(column=1, row=2)

member_name_input = Entry(member_update_details_frame, width=20)
member_name_input.grid(column=2, row=2)
member_name_input.focus()

member_faculty_label = Label(member_update_details_frame, text="Faculty", height=2)
member_faculty_label.grid(column=1, row=3)

member_faculty_input = Entry(member_update_details_frame, width=20)
member_faculty_input.grid(column=2, row=3)
member_faculty_input.focus()

member_phone_label = Label(member_update_details_frame, text="Phone Number", height=2)
member_phone_label.grid(column=1, row=4)

member_phone_input = Entry(member_update_details_frame, width=20)
member_phone_input.grid(column=2, row=4)
member_phone_input.focus()

member_faculty_label = Label(member_update_details_frame, text="Email Address", height=2)
member_faculty_label.grid(column=1, row=5)

member_email_input = Entry(member_update_details_frame, width=20)
member_email_input.grid(column=2, row=5)
member_email_input.focus()

update_member_button = Button(member_update_details_frame, text="Update Member", fg="black", bg="#E5D4C0", padx=40, pady=10, command = member_update_confirm)
update_member_button.grid(column=1, row=6)
return_to_membership_menu = Button(member_update_details_frame, text="Back to Membership Menu", fg="black", bg="#E5D4C0", padx=40, pady=10, command=lambda: change_frame(option_select_frame, member_update_details_frame))
return_to_membership_menu.grid(column=2, row=6)

#--------------------------------books frame------------------------------------

#option selection 
select_book_action = Label(books_select_frame, text = "Select one of the Options below:", fg="white", bg="#413F54", width=30, height=2, borderwidth=1, relief=SOLID, padx=300, pady=30)
select_book_action.config(font=("Arial", 20, "bold"))
select_book_action.grid(column=0, row=0, columnspan=4)

select_book_acquisition = Button(books_select_frame, text = "Acquisition", fg = "black", bg = "#8789C0", padx = 200, pady = 50,
       command = lambda: change_frame(book_acquisition_frame, books_select_frame))
##select_book_acquisition.config(padx = 20)
##select_book_acquisition.grid(column=0, row=1, padx=(50,50))
select_book_acquisition.grid(column=1, row=1)

select_book_withdrawal = Button(books_select_frame, text = "Withdrawal", fg = "black", bg = "#8789C0", padx = 200, pady = 50,
       command = lambda: change_frame(book_withdrawal_frame, books_select_frame))
##select_book_withdrawal.config(padx = 20)
##select_book_withdrawal.grid(column=0, row=2, padx=(50,50)) 
select_book_withdrawal.grid(column=1, row=2) 

back_to_main_menu = Button(books_select_frame, text = "Back to Main Menu", fg="black", bg="#E5D4C0", padx=400, pady=20, command=lambda: change_frame(main_menu_frame, books_select_frame))
##back_to_main_menu.config(padx = 40)
##back_to_main_menu.grid(column=0, row=3, padx=(50,50))
back_to_main_menu.grid(column=0, row=3, columnspan=2)

bookspic = ImageTk.PhotoImage(Image.open("bookspic.png"))
myLabelbookspic = Label(books_select_frame, image = bookspic, padx = 200, pady = 100)
myLabelbookspic.grid(row = 1, column = 0, rowspan=2)

# --------------- Book Acquisition frame ----------------------- #
# if accessionNo not in books table:
# return book_success
#else:
# return add_book_error


#popup if can add book to library
def book_success():
 global success_label, success_button
 success_pg = Toplevel()
 success_pg.title("Success!")
 success_label = Label(success_pg, text = "New Book added in Library.",
    fg = "white", bg = "green", padx = 400, pady = 50)
 success_button = Button(success_pg, text = "Back to Acquisition Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = success_pg.destroy)
 success_label.grid(row = 0, column = 0, columnspan = 2)
 success_button.grid(row = 1, column = 0, columnspan = 2)

#popup if cannot add book
def add_book_error():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error!")
  error_label = Label(error_pg, text = "Book already added; Duplicate, Missing or Incomplete fields.", 
      fg = "yellow", bg = "red", padx = 400, pady = 50) 
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Acquisition Function", 
    fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = error_pg.destroy)
  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0, columnspan = 2)


book_acquisition_label = Label(book_acquisition_frame, 
   text="For New Book Acquisition, Please Enter Required Information Below:", fg = "white", bg = "#413F54", padx = 200, pady = 50, borderwidth=1)
book_acquisition_label.config(font=("Arial", 20, "bold"))
book_acquisition_label.grid(column=0, row=0, columnspan=4, padx=(50,10), pady=(10,10))

accession_no_label = Label(book_acquisition_frame, text="Accession Number")
accession_no_label.grid(column=1, row=1, padx=(50,10), pady=(10,10))
stringAccNo = StringVar()
accession_no_input = Entry(book_acquisition_frame, textvariable = stringAccNo)
accession_no_input.grid(column=2, row=1, padx=(10,50), pady=(10,10))
accession_no_input.focus()

title_label = Label(book_acquisition_frame, text="Title")
title_label.grid(column=1, row=2, padx=(50,10), pady=(10,10))
stringTitle = StringVar()
title_input = Entry(book_acquisition_frame, textvariable = stringTitle)
title_input.grid(column=2, row=2, padx=(10,50), pady=(10,10))

authors_label = Label(book_acquisition_frame, text="Authors")
authors_label.grid(column=1, row=3, padx=(50,10), pady=(10,10))
stringAuthors = StringVar()
authors_input = Entry(book_acquisition_frame, textvariable = stringAuthors)
authors_input.grid(column=2, row=3, padx=(10,50), pady=(10,10))

isbn_label = Label(book_acquisition_frame, text="ISBN")
isbn_label.grid(column=1, row=4, padx=(50,10), pady=(10,10))
stringISBN = StringVar()
isbn_input = Entry(book_acquisition_frame, textvariable = stringISBN)
isbn_input.grid(column=2, row=4, padx=(10,50), pady=(10,10))

publisher_label = Label(book_acquisition_frame, text="Publisher")
publisher_label.grid(column=1, row=5, padx=(50,10), pady=(10,10))
stringPublisher = StringVar()
publisher_input = Entry(book_acquisition_frame, textvariable = stringPublisher)
publisher_input.grid(column=2, row=5, padx=(10,50), pady=(10,10))

publication_year_label = Label(book_acquisition_frame, text="Publication Year")
publication_year_label.grid(column=1, row=6, padx=(50,10), pady=(10,10))
stringPubYear = StringVar()
publication_year_input = Entry(book_acquisition_frame, textvariable = stringPubYear)
publication_year_input.grid(column=2, row=6, padx=(10,50), pady=(10,10))

add_new_book = Button(book_acquisition_frame, text = "Add New Book", width = 20, fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [aquire_book()])
add_new_book.config(padx=40)
add_new_book.grid(column=1, row=7, padx=(50,50))
back_to_books_menu = Button(book_acquisition_frame, text = "Back to Books Menu", width = 20, fg = "black", bg = "#E5D4C0", padx = 50, pady = 20,
  command = lambda: change_frame(books_select_frame, book_acquisition_frame))
back_to_books_menu.config(padx=40)
back_to_books_menu.grid(column=2, row=7, padx=(50,50))

# --------------- Book Withdrawal frame ----------------------- #
#def withdrawal_book_result():
# if accessionNo in loan table:
#  return on_loan_error
# elif accessionNo in reserve table:
#  return reserved_error
# else:
#  return confirm


def combinewithdraw(confirm_pg):
    confirm_withdraw()
    confirm_pg.destroy()

#popup if can withdraw book
def confirm(): 
    global confirm_label, confirm_button1, confirm_button2
    confirm_pg = Toplevel() 
    confirm_pg.title("Confirm Withdrawal")
    confirm_label = Label(confirm_pg, text = "Please Confirm Details To Be Correct", fg = "white", bg = "#413F54", padx = 400, pady = 50)

    #PLUS ALL THE SQL STUFF HERE 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    cs = mydb.cursor()
    ACC = stringwithdrawAccNo.get()
    statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Accession_No = %s"
    insert = (f'{ACC}',)
    cs.execute(statement, insert)
    records = cs.fetchall()
    printrecords = ''
    for records in records:
        printrecords += str(records[0]) + "\n" + " " + "\n" + str(records[1]) + "\n" + " " + "\n" + str(records[2]) + "\n" + " " + "\n" + str(records[3]) + "\n" + " " + "\n" +str(records[4]) + "\n" + " " + "\n" +str(records[5]) 
    label = Label(confirm_pg, text=printrecords, height=12)


    book_AccNo_label = Label(confirm_pg, text="Accession Number")
    book_title_label = Label(confirm_pg, text="Title")
    book_authors_label = Label(confirm_pg, text="Authors")
    book_ISBN_label = Label(confirm_pg, text="ISBN")
    book_publisher_label = Label(confirm_pg, text="Publisher")
    book_pubyear_label = Label(confirm_pg, text="Publication Year")


    confirm_button1 = Button(confirm_pg, text = "Confirm Withdrawal", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [combinewithdraw(confirm_pg)])
    confirm_button2 = Button(confirm_pg, text = "Back To Withdrawal Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = confirm_pg.destroy)

    confirm_label.grid(row = 0, column = 0, columnspan = 2)
    label.grid(row = 1, column = 1, rowspan = 6)
    book_AccNo_label.grid(column = 0, row = 1)
    book_title_label.grid(column = 0, row = 2)
    book_authors_label.grid(column = 0, row = 3)
    book_ISBN_label.grid(column = 0, row = 4)
    book_publisher_label.grid(column = 0, row = 5)
    book_pubyear_label.grid(column = 0, row = 6)
    confirm_button1.grid(row = 7, column = 0)
    confirm_button2.grid(row = 7, column = 1)

    mydb.commit()
    mydb.close()

#popup if cannot withdraw book due to on loan
def on_loan_error():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error")
  error_label = Label(error_pg, text = "Book is currently on Loan", 
      fg = "yellow", bg = "red", padx = 400, pady = 50) 
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Withdrawal Function", 
    fg = "black", bg = "green", padx = 50, pady = 20, command = error_pg.destroy)
  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0, columnspan = 2)

#popup if cannot withdraw book due to reserved
def reserved_error():
  global error_label, error_button
  error_pg = Toplevel() 
  error_pg.title("Error")
  error_label = Label(error_pg, text = "Book is currently Reserved", 
      fg = "yellow", bg = "red", padx = 400, pady = 50) 
  #PLUS ALL THE SQL STUFF HERE 
  error_button = Button(error_pg, text = "Back to Withdrawal Function", 
    fg = "black", bg = "green", padx = 50, pady = 20, command = error_pg.destroy)
  error_label.grid(row = 0, column = 0, columnspan = 2)
  error_button.grid(row = 1, column = 0, columnspan = 2)
 
book_withdrawal_label = Label(book_withdrawal_frame, 
  text="To Remove Outdated Books From System, Please Enter Required Information Below:", fg = "white", bg = "#413F54", padx = 200, pady = 50, borderwidth=1)
book_withdrawal_label.grid(column=0, row=0, columnspan=2)
book_withdrawal_label.config(font=("Arial", 15, "bold"))

accession_no_label2 = Label(book_withdrawal_frame, text = "Accession Number")
accession_no_label2.grid(column=0, row=1, padx=(50,10), pady=(10,10))
stringwithdrawAccNo = StringVar()
accession_no_input2 = Entry(book_withdrawal_frame, textvariable = stringwithdrawAccNo)
accession_no_input2.grid(column=1, row=1, padx=(10,50), pady=(10,10))

withdraw_book = Button(book_withdrawal_frame, text = "Withdraw Book", width = 20, fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: [withdraw_book_func()])     
withdraw_book.config(padx=40)
withdraw_book.grid(column=0, row=3, padx=(50,50))
back_to_books_menu2 = Button(book_withdrawal_frame, text = "Back to Books Menu", width = 20, fg = "black", bg = "#E5D4C0", padx = 50, pady = 20,
  command = lambda: change_frame(books_select_frame, book_withdrawal_frame))
back_to_books_menu2.config(padx=40)
back_to_books_menu2.grid(column=1, row=3, padx=(50,50))

#-------------------------------------reports frame (slide 46)--------------------------
myLabel = Label(reports_frame, text = "Select one of the Options below:", fg = "white", bg = "#413F54", padx = 300, pady = 50)
myLabel.config(font=("Arial", 20, "bold"))

myButton1 = Button(reports_frame, text = "Book Search", fg = "black", bg = "#8789C0", padx = 20, pady = 20, width = 50, command = lambda: change_frame(reports_search_frame, reports_frame))
myButton2 = Button(reports_frame, text = "Books on Loan", fg = "black", bg = "#8789C0", padx = 20, pady = 20, width = 50, command = display_books_on_loan)
myButton3 = Button(reports_frame, text = "Books on Reservation", fg = "black", bg = "#8789C0", padx = 20, pady = 20, width = 50, command = display_books_on_reservation)
myButton4 = Button(reports_frame, text = "Outstanding Fines", fg = "black", bg = "#8789C0", padx = 20, pady = 20, width = 50, command = members_with_fines)
myButton5 = Button(reports_frame, text = "Books on Loan to Member", fg = "black", bg = "#8789C0", padx = 20, pady = 20, width = 50, command = lambda: change_frame(reports_loan_member_frame, reports_frame))

myButton6 = Button(reports_frame, text = "Back To Main Menu", fg = "black", bg = "#E5D4C0", padx = 400, pady = 20, command = lambda: change_frame(main_menu_frame, reports_frame))

reportspic = ImageTk.PhotoImage(Image.open("reportspic.png"))
myLabelreportspic = Label(reports_frame, image = reportspic, padx = 200, pady = 100)

myLabel.grid(row = 0, column =0, columnspan = 2)
myButton1.grid(row = 1, column = 1)
myButton2.grid(row = 2, column = 1)
myButton3.grid(row = 3, column = 1)
myButton4.grid(row = 4, column = 1)
myButton5.grid(row = 5, column = 1)
myLabelreportspic.grid(row = 1, column = 0, rowspan = 5)
myButton6.grid(row = 6, column =0, columnspan = 2)

#---------------------------------------------search frame (slide 47)--------------------------------------
myLabel = Label(reports_search_frame, text = "Search Based on One of the Categories Below:", fg = "white", bg = "#413F54", padx = 400, pady = 50)
myLabel.grid(row = 0, column =0, columnspan = 2)

label_title = Label(reports_search_frame, text = "Title", padx = 60, pady = 20)
label_authors = Label(reports_search_frame, text = "Authors", padx = 60, pady = 20)
label_isbn = Label(reports_search_frame, text = "ISBN", padx = 60, pady = 20)
label_pub = Label(reports_search_frame, text = "Publisher", padx = 60, pady = 20)
label_pubyear = Label(reports_search_frame, text = "Publication Year", padx = 60, pady = 20)

label_title.grid(row = 1, column =0)
label_authors.grid(row = 2, column =0)
label_isbn.grid(row = 3, column = 0)
label_pub.grid(row = 4, column =0)
label_pubyear.grid(row = 5, column = 0)

string_e_title= StringVar()
e_title = Entry(reports_search_frame, width = 50, textvariable = string_e_title)
string_e_author = StringVar()
e_author = Entry(reports_search_frame, width = 50, textvariable = string_e_author)
string_e_isbn = StringVar()
e_isbn = Entry(reports_search_frame, width = 50, textvariable = string_e_isbn)
string_e_pub = StringVar()
e_pub = Entry(reports_search_frame, width = 50, textvariable = string_e_pub)
string_e_pubyear = StringVar()
e_pubyear = Entry(reports_search_frame, width = 50, textvariable = string_e_pubyear)

e_title.grid(row = 1, column =1)
e_author.grid(row = 2, column =1)
e_isbn.grid(row = 3, column = 1)
e_pub.grid(row = 4, column =1)
e_pubyear.grid(row = 5, column = 1)

def inside(title, entry):
    flag = False
    test = ""
    title = title + " "
    for i in range(len(title)):
        if title[i] != " ":
            test += title[i]
        elif title[i] == " ": 
            if test.upper() == entry.upper():
                flag = True
                break
            else:
                test = ""
    return flag


def search():
    global search_label, backtosearch_button
    search_pg = Toplevel() 
    search_pg.title("Book Search")
    search_label = Label(search_pg, text = "Book Search Results", fg = "white", bg = "#413F54", padx = 400, pady = 50)

    #PLUS ALL THE SQL STUFF HERE 
    mydb = mysql.connector.connect(host='localhost', database='ALS', user='root', password=SQL_PW)
    checkTitle = pd.read_sql_query('SELECT Title FROM Book', engine).to_numpy()
    checkAuthor = pd.read_sql_query('SELECT DISTINCT(Author) FROM Book', engine).to_numpy()
    checkISBN = pd.read_sql_query('SELECT ISBN FROM Book', engine).to_numpy()
    checkPub = pd.read_sql_query('SELECT DISTINCT(Publisher) FROM Book', engine).to_numpy()
    checkPubYear = pd.read_sql_query('SELECT Publication_Year FROM Book', engine).to_numpy()    

    cs = mydb.cursor()
    TITLE2 = string_e_title.get()
    AUTHOR2 = string_e_author.get()
    ISBN2 = string_e_isbn.get()
    PUB2 = string_e_pub.get()
    PUBYEAR2 = string_e_pubyear.get()
      
    search_cols = ('Accession Number', 'Title', 'Author', 'ISBN', 'Publisher', 'Year')
    search_table = Treeview(search_pg, columns=search_cols, show='headings')
    for col in search_cols:
        search_table.heading(col, text=col)
        search_table.column(col, minwidth=0, width=120, stretch=NO)
        search_table.grid(row=1, column=0, columnspan=6)

    result = []
    record = []
    record2 = []
    if TITLE2 != "":
        for book in checkTitle:
            if inside(book[0], TITLE2):     
                statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Title = %s"
                insert = (f'{book[0]}',)
                cs.execute(statement, insert)
                record.append(cs.fetchall())

    if AUTHOR2 != "":
        for book in checkAuthor:
            if inside(book[0], AUTHOR2):
                statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Author = %s"
                insert = (f'{book[0]}',)
                cs.execute(statement, insert)
                result.append(cs.fetchall())

    if ISBN2 != "":
        for book in checkISBN:
            if inside(book[0], ISBN2):
                statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE ISBN = %s"
                insert = (f'{book[0]}',)
                cs.execute(statement, insert)
                record2.append(cs.fetchall())

    if PUB2 != "":
        for book in checkPub:
            if inside(book[0], PUB2):
                statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Publisher = %s"
                insert = (f'{book[0]}',)
                cs.execute(statement, insert)
                result.append(cs.fetchall())

    if PUBYEAR2 != "":
        for book in checkPubYear:
            if book[0] == int(PUBYEAR2):
                statement = "SELECT Accession_No, Title, Author, ISBN, Publisher, Publication_Year FROM Book WHERE Publication_Year = %s"
                insert = (f'{book[0]}',)
                cs.execute(statement, insert)
                record2.append(cs.fetchall())

    for i in range(len(result)):
        if len(result[i]) == 1:
            search_table.insert(parent = '', index = i, values = result[i][0])
        else:
            for j in range(len(result[i])):
                search_table.insert(parent = '', index = i, values = result[i][j])

    for i in range(len(record)):
        search_table.insert(parent = '', index = i, iid = i, values = record[i][0])

    for i in range(len(record2)):
        search_table.insert(parent = '', index = i, iid = i, values = record2[0][i])

    backtosearch_button = Button(search_pg, text = "Back to Search Function", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = search_pg.destroy)
    search_label.grid(row = 0, column = 0, columnspan = 3)
    backtosearch_button.grid(row = 5, column = 1)

search_button = Button(reports_search_frame, text = "Search Book", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = search) #how to put many commands
reportsmenu_button = Button(reports_search_frame, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reports_frame, reports_search_frame))

search_button.grid(row = 6, column = 0)
reportsmenu_button.grid(row = 6, column =1)

#--------------------------------------loans frame(slide 49)--------------------------------------------------------
myLabel = Label(reports_loans_frame, text = "Books on Loan to Member", fg = "white", bg = "#413F54", padx = 400, pady = 50)
myLabel.grid(row = 0, column =0, columnspan = 2)

#PLUS ALL THE SQL STUFF HERE

reportsmenu_button = Button(reports_loans_frame, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reports_frame, reports_loans_frame))
reportsmenu_button.grid(row = 3, column =1)

#--------------------------------------books on reservation frame(slide 50)--------------------------------------------------------
myLabel = Label(reports_reservation_frame, text = "Books on Reservation to Member", fg = "white", bg = "#413F54", padx = 400, pady = 50)
myLabel.grid(row = 0, column =0, columnspan = 2)

#PLUS ALL THE SQL STUFF HERE

reportsmenu_button = Button(reports_reservation_frame, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reports_frame, reports_reservation_frame))
reportsmenu_button.grid(row = 3, column =1)

#--------------------------------------members w fines report frame(slide 51)--------------------------------------------------------
myLabel = Label(reports_fines_frame, text = "Members With Outstanding Fines", fg = "white", bg = "#413F54", padx = 400, pady = 50)
myLabel.grid(row = 0, column =0, columnspan = 2)

#PLUS ALL THE SQL STUFF HERE

reportsmenu_button = Button(reports_fines_frame, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reports_frame, reports_fines_frame))
reportsmenu_button.grid(row = 3, column =1)

#---------------------------------------------search frame (slide 47)--------------------------------------
myLabel = Label(reports_loan_member_frame, text = "Books on Loan to Member", fg = "white", bg = "#413F54", padx = 400, pady = 50)
myLabel.grid(row = 0, column =0, columnspan = 2)

label_memberid = Label(reports_loan_member_frame, text = "Membership ID", padx = 60, pady = 20)
label_memberid.grid(row = 1, column = 0)
e_memberid = Entry(reports_loan_member_frame, width = 50)
e_memberid.grid(row = 1, column = 1)

###################################################################################

    
search2_button = Button(reports_loan_member_frame, text = "Search Member", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = search2) #how to put many commands 
reportsmenu2_button = Button(reports_loan_member_frame, text = "Back To Reports Menu", fg = "black", bg = "#E5D4C0", padx = 50, pady = 20, command = lambda: change_frame(reports_frame, reports_loan_member_frame)) 
search2_button.grid(row = 6, column = 0) 
reportsmenu2_button.grid(row = 6, column =1)

###################################################################################

root.mainloop()