import sqlite3

conn  = sqlite3.connect("student.db") #it creates db if already doesnt exist

cursor  = conn.cursor() #create a cursor object
print("database created successfully")


cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT
        
    )
    '''
)
conn.commit()
print("table created successfully")

cursor.execute(
    '''
    INSERT INTO students (name,age,course) VALUES(?,?,?)
    ''',('Harman',22,'MCA')
)

conn.commit()
print("Data added")

cursor.execute(
    '''
    SELECT * FROM students
    '''
)

data = cursor.fetchall()

for row in data:
    print(row)

cursor.execute("""
            UPDATE students SET course=? WHERE id =?
            """,("mca",1))


conn.commit()
print("data updated")


cursor.execute('''
                SELECT * FROM students
                ''')

data = cursor.fetchall()


print(data)



cursor.execute("""
            DELETE FROM students WHERE id= ?""",(3,))

conn.commit()


cursor.execute('''
                SELECT * FROM students
                ''')

data = cursor.fetchall()


print(data)


cursor.execute("""DELETE FROM students""")
conn.commit()
print("All data deleted")


cursor.execute('''
                SELECT * FROM students
                ''')

data = cursor.fetchall()


print(data)



