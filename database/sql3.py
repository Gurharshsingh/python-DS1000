import sqlite3


conn = sqlite3.connect("student_advanced.db")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


print("database connected")


# cursor.execute("""
#             CREATE TABLE IF NOT EXISTS courses(
#                 course_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 course_name TEXT NOT NULL,
#                 course_code TEXT NOT NULL UNIQUE,
#                 fee REAL NOT NULL
                
#             )
#             """)


# cursor.execute("""
#             CREATE TABLE IF NOT EXISTS students(
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             age INTEGER,
#             course_id INTEGER,
#             FOREIGN KEY (course_id) references courses (course_id))
#             """)


# conn.commit()



# courses_data = [ 
#         ("Python","Py101",10000),
#         ("Java","Ja101",12000),
#         ("Data Science","DS101",15000),
#         ("Machine Learning","ML101",18000),
#         ("Deep Learning","DL101",20000),
#         ("Web Development","WD101",14000),
#         ("Mobile Development","MD101",16000),
#         ("Data Analytics","DA101",13000),
#         ("Business Analytics","BA101",11000),
#         ("AI","AI101",17000)
# ]


# cursor.executemany("""
#             INSERT INTO courses(course_name,course_code,fee)
#             VALUES(?,?,?)
#             """, courses_data)

# conn.commit()
# print("Courses inserted successfully")


# students_data = [
#     ("John",20,1),
#     ("Jane",22,2),
#     ("Doe",23,3),
#     ("Peter",24,4),
#     ("Mary",25,5),
#     ("Rahul",21,6),
#     ("Priya",26,7),
#     ("Amit",27,8),
#     ("Sunita",28,9),
#     ("Vikram",29,10)
# ]

# cursor.executemany("""
#                 INSERT INTO students(name,age,course_id)
#                 VALUES(?,?,?)
#                 """, students_data)
# conn.commit()
# print("Students inserted successfully")




# join

cursor.execute("""
            SELECT students.id, students.name, students.age, courses.course_name, courses.course_code, courses.fee
            FROM students 
            INNER JOIN courses  ON students.course_id = courses.course_id""")

result = cursor.fetchall()

print("\nInner join result:")
for row in result:
    print(row)



# aggregate functions

cursor.execute("""
            SELECT
                COUNT(id) AS total_students,
                AVG(age) AS avg_age,
                MIN(age) AS min_age,
                MAX(age) AS max_age
            FROM students
                """
            )


summary = cursor.fetchone()
print(f"Total students: {summary[0]} Average age: {summary[1]:.2f} Minimum age: {summary[2]} Maximum age: {summary[3]}")
    