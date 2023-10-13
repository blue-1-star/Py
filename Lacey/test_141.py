import sqlite3

with sqlite3.connect("BookInfo.db") as db:
    cursor=db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Authors( 
Name text NOT NULL,
PlaceOfBirth text NOT NULL);""")

# with sqlite3.connect("BookInfo.db") as db:
#     cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Books(
id integer PRIMARY KEY,
Title text NOT NULL,
Author text NOT NULL,
DatePublished integer);""")

cursor.execute("""INSERT INTO Authors(Name, PlaceOfBirth)
VALUES("Agatha Christie", "Torquay")""")
cursor.execute("""INSERT INTO Authors(Name, PlaceOfBirth)
VALUES("Cecelia Ahern", "Dublin")""")
db.commit()

cursor.execute("""INSERT INTO Books(id, Title, Author, DatePublished )
VALUES("1", "De Profundis", "Oscar Wilde", "1905")""")
db.commit()
db.close()

