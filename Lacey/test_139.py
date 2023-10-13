#import random
import sqlite3

with sqlite3.connect("PhoneBook1.db") as db:
    cursor=db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Names(
id integer PRIMARY KEY,
Firstname text NOT NULL,
Surname text NOT NULL,
PhoneNumber integer);""")

cursor.execute("""INSERT INTO Names(id, Firstname, Surname, PhoneNumber )
VALUES("1", "Simon", "Howeis", "0122334972")""")
db.commit()

cursor.execute("""INSERT INTO Names(id, Firstname, Surname, PhoneNumber )
VALUES("2", "Karen", "Phillips", "01954295773")""")
db.commit()

cursor.execute("""INSERT INTO Names(id, Firstname, Surname, PhoneNumber )
VALUES("3", "Darren", "Smith", "01583749012")""")
db.commit()

cursor.execute("""INSERT INTO Names(id, Firstname, Surname, PhoneNumber )
VALUES("4", "Anne", "Jones", "01323567322")""")
db.commit()

cursor.execute("""INSERT INTO Names(id, Firstname, Surname, PhoneNumber )
VALUES("5", "Mark", "Smith", "01223855534")""")
db.commit()
db.close()
