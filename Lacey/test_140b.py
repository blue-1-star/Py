##import sqlite3
##
##def viewphonebook():
##    cursor.execute("SELECT * FROM Names")
##    for x in cursor.fetchall():
##        print(x)
##
##def addtophonebook():
##    newid = int(input("Enter ID: "))
##    newfname = int(input("Enter first name: "))
##    newsname = int(input("Enter surname: "))
##    newpnum = int(input("Enter phone number: "))
##    cursor.execute(""" INSERT INTO Names(id, firstname, surname, phonenumber)
##VALUES (?, ?, ?, ?)""", (newid, newfname, newsname, newpnum))
##    db.commit()
##
##def selectname():
##    selectsurname = input("Enter a surname: ")
##    cursor.execute(""" SELECT * FROM Names WHERE surname = ?""", [selectsurname])
##    for x in cursor.fetchall():
##        print(x)
##
##def deletedata():
##    selectid = int(input("Enter ID: "))
##    cursor.execute("DELETE FROM Names WHERE id = ?", [selectid])
##    cursor.execute("SELECT * FROM Names")
##    for x in cursor.fetchall():
##        print(x)
##    db.commit()
##with sqlite3.connect("PhoneBook.db") as db:
##    cursor = db.cursor()
                   

def main():
    again = "y"
    while again == "y":
        print()
        print("Main Menu")
        print()
        print("1) View phone book")
        print("2) Add to phone book")
        print("3) Search for surname")
        print("4) Delete person from phone book")
        print("5) Quit")
        print()
        
        selection = int(input("Enter your selection: "))               
        print("selection  = ", selection)
        if selection == 1:
            print("1")
        elif selection == 2:
            print("2")
        elif selection == 3:
            print("3")
        elif selection == 4:
            print("4")
        elif selection ==5:
            again = "n"
        else:
            print("Incorrect selection entered")

main()
#db.close()

