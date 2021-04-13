import getpass
import time
import os
from tabulate import tabulate
import datetime
#size of console
os.system('mode con cols=100 lines=280')
#password function
n = 1
while n == 1:
    t = getpass.getpass(prompt='Please Enter your Password: ')
    if t.lower() == 'library':
        print('Password Accepted')
        time.sleep(1)
        n = 2
    else:
        print('The Password is incorrect. Please Try Again')
        time.sleep(2)
        os.system('CLS')
        n = 1
#Connecting to mysql
import mysql.connector
mydb = mysql.connector.connect(host='localhost',user='root',passwd='root')
mycursor = mydb.cursor()
if mydb.is_connected:
    print('Connection to database successful.')
    time.sleep(1)

#creating required database
mycursor.execute('Create database if not exists Library')
mycursor.execute('use Library')

#Creating tables
mycursor.execute("Create table if not exists bookdata(id char(10) primary key,bookname char(130),author char(100))")
mycursor.execute("Create table if not exists bookissue(name varchar(100) primary key,issuedate date,bookname1 char(100),bookid char(10))")


#inserting stuff
while(True):
    os.system('CLS')
    print('        ###         ###########   ########')
    print('        ###             ###       ##     ##')
    print('        ###             ###       ##     ##')
    print('        ###             ###       ########')
    print('        ###             ###       ##     ##')
    print('        #########       ###       ##     ##')
    print('        #########   ###########   ########    v(0.2)')

    print('Welcome to the Library Management System!!')
    print('1.Add Book Data')
    print('2.Display Book List')
    print('3.Display Issued Books')
    print('4.Issue Book')
    print('5.Return Book')
    print('6.Fine Details')
    print('7.Exit')
    ch = int(input('Enter your choice: '))

    if ch == 1:
        os.system('CLS')
        bid = str(input('Enter the book id (6 digits): '))
        bname = str(input('Enter the name of the book: '))
        bauthor = str(input('Enter the name of the author: '))
        mycursor.execute("insert into bookdata values(%s,%s,%s)",(bid,bname,bauthor))
        mydb.commit()#To permanently save data
        print('Book Data Successfully added!')
        q = input('Press Enter to continue')

    if ch == 2:
        os.system('CLS')
        mycursor.execute('Select * from bookdata')
        data = mycursor.fetchall()
        print(tabulate(data, headers=['Book ID','Book Name','Author'], tablefmt='psql'))
        z = input('Press Enter To Continue')
        
        
    if ch == 4:
        os.system('CLS')
        pname = str(input('Enter Name(First and Last): '))
        iid = str(input('Enter the id of the book issued: '))
        day = int(input('Enter the day of issue: '))
        month = int(input('Enter the month of issue: '))
        year = int(input('Enter the year of issue: '))
        idate = datetime.date(year,month,day)
        mycursor.execute("select bookname from bookdata where id ='"+iid+"'")
        iname = mycursor.fetchone()
        bb = iname[0]
        mycursor.execute('select * from bookissue')
        check = mycursor.fetchall()
        mycursor.execute("insert into bookissue (name,issuedate,bookname1,bookid) values (%s,%s,%s,%s)",(pname,idate,bb,iid))
        print('Book issued successfully!')
        mydb.commit()
        #my db.commit() not added, so data not saved permanently
        x = input('Press Enter to Continue')

    if ch == 3:
        os.system('CLS')
        mycursor.execute('Select * from bookissue')
        data = mycursor.fetchall()
        print(tabulate(data, headers=['Name of Borrower','Date of Issue','Book Name','Book Id'], tablefmt='psql'))
        l = input('Press Enter to Continue')

    if ch == 5:
        os.system('CLS')
        rname = str(input('Enter the name of the borrower: '))
        mycursor.execute("Select issuedate from bookissue where name ='"+rname+"'")
        dd = mycursor.fetchone()
        ddd = dd[0]
        pp = datetime.date.today()
        delta = (pp-ddd).days
        if delta >= 15:
            c = (delta//7)-1
            print('Date the book was issued: ',ddd)
            print("A fine of 1 dollar is applicable for each week the book hasn't been returned")
            print('Days the book was leased for: ',delta)
            print('Weeks:( ',delta,'modulo 7) - 1, which gives',c) 
            print('Fine = ',c,'* 1$ = ',c,'dollar(s)')
            print('The borrower has exceeded his lease time by',delta-14,'day(s).')
            print('So, a fine of',c,'$ is applicable. Please collect the fine.')
            time.sleep(0.5) 
            mycursor.execute("delete from bookissue where name ='"+rname+"'")
            mydb.commit()#to save changes
            print('Book Returned Successfully')
            g = input('Press Enter to continue')
        elif delta<15:
            cc = 15 - delta
            print('The borrower can keep the book for',cc,'more days.')
            w = str(input(" Would you still like to return the book? (Y/N): "))
            if w.lower()== 'y':
                mycursor.execute("delete from bookissue where name ='"+rname+"'")
                mydb.commit()
                ww = input('Since the book is still in issue period, no fine is to be collected. Book Returned Successfully. Press Enter to continue')
            elif w.lower()== 'n':
                print('Please ensure that the book is returned after',cc,'days')
                wwww = input('Press Enter to continue')

    if ch == 7:
        os.system('CLS')
        print('Thanks for using the library management system!')
        v = input('Press Enter to exit')
        break

    if ch == 6:
        print('A fine of 1 $ is applicable for each week the book is not returned')
        vv = input('Press enter to exit')
    
    
