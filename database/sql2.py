import sqlite3 

conn  = sqlite3.connect("student.db")

cursor = conn.cursor()

print(" database created successfully")

cursor.execute('''
                SELECT * FROM students
                ''')

data = cursor.fetchall()

print(data)



students = [
    ('ram','22','mca'),
    ('raman','20','bca'),
    ('mohit','23','bba')
]

# executemany - for multiple values
cursor.executemany('''
                    INSERT INTO students (name,age,course)
                    values(?,?,?)
                    ''',students)

conn.commit()
print(" Data added successfully")


cursor.execute('''
                SELECT * FROM students
                ''')

data = cursor.fetchall()

print(data)




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

