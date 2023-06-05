import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM events")

rows = cursor.fetchall()
print(rows)

new_rows =[('cat', 'Lion city', '2088.10.28'),
           ('Monkeys', 'Monkey City', '2088.10.19')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()
print(rows)