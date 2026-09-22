# 📘 Advanced SQLite & SQL Guide: Keys, Joins, Aggregations & Filtering

A comprehensive, beginner-friendly guide covering relational database concepts: Primary & Foreign Keys, Table Joins, Aggregate Functions, and Advanced Filtering Techniques.

---

## 📑 Table of Contents
1. [Primary Key vs. Foreign Key](#1-primary-key-vs-foreign-key)
   - [What is a Primary Key (PK)?](#what-is-a-primary-key-pk)
   - [What is a Foreign Key (FK)?](#what-is-a-foreign-key-fk)
   - [Comparison Summary](#comparison-summary)
   - [Enabling Foreign Keys in SQLite](#enabling-foreign-keys-in-sqlite)
2. [Database Normalization & Relationships](#2-database-normalization--relationships)
3. [SQL JOIN Operations](#3-sql-join-operations)
   - [INNER JOIN](#a-inner-join)
   - [LEFT JOIN (LEFT OUTER JOIN)](#b-left-join)
   - [RIGHT & FULL OUTER JOIN (Overview)](#c-right--full-outer-join-in-sqlite)
4. [Aggregate Functions & Grouping](#4-aggregate-functions--grouping)
   - [Basic Aggregates: COUNT, AVG, SUM, MIN, MAX](#basic-aggregates)
   - [GROUP BY](#group-by)
   - [HAVING vs WHERE](#having-vs-where)
5. [Advanced Filtering & Sorting](#5-advanced-filtering--sorting)
   - [BETWEEN ... AND ...](#between--and-)
   - [IN (...) and NOT IN (...)](#in--and-not-in-)
   - [LIKE & Wildcards (% and _)](#like--wildcards)
   - [IS NULL / IS NOT NULL](#is-null--is-not-null)
   - [ORDER BY (ASC / DESC)](#order-by)
   - [LIMIT & OFFSET](#limit--offset)
6. [Complete Code Reference Cheat Sheet](#6-complete-code-reference-cheat-sheet)

---

## 1. Primary Key vs. Foreign Key

In a real-world relational database, data is split across multiple tables to avoid data repetition (redundancy). Keys are the bridges that connect and protect these tables.

```
       TABLE: courses (Parent)
       +-----------+-------------+-------+
       | course_id | course_name | fee   |  <-- PRIMARY KEY: course_id
       +-----------+-------------+-------+
       | 101       | Python      | 5000  |
       | 102       | Web Dev     | 4500  |
       +-----------+-------------+-------+
                         ▲
                         │  (Relates student to their course)
                         │
       TABLE: students (Child)
       +----+--------+-----+-----------+
       | id | name   | age | course_id |  <-- FOREIGN KEY: course_id
       +----+--------+-----+-----------+
       | 1  | Harman | 22  | 101       |
       | 2  | Raman  | 20  | 102       |
       +----+--------+-----+-----------+
```

---

### What is a Primary Key (PK)?

- **Definition**: A column (or combination of columns) that **uniquely identifies** every single row in a table.
- **Rules**:
  1. Must be **UNIQUE** (no duplicate values).
  2. Cannot be **NULL** (must always have a value).
  3. A table can have **only one Primary Key**.

#### SQL Example:
```sql
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    fee REAL
);
```

---

### What is a Foreign Key (FK)?

- **Definition**: A column in one table (Child) that **references the Primary Key** of another table (Parent).
- **Purpose**: Establishes a link between tables and maintains **Referential Integrity** (prevents orphaned records).
- **Rules**:
  1. Can have **duplicate values** (many students can enroll in the same course).
  2. Can be **NULL** (unless marked `NOT NULL`, e.g., a student hasn't picked a course yet).
  3. You **cannot insert** a foreign key value that does not exist in the parent table!
  4. You **cannot delete** a parent row if child rows reference it (unless configured with `CASCADE`).

#### SQL Example:
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course_id INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

---

### Comparison Summary

| Feature | Primary Key (PK) | Foreign Key (FK) |
| :--- | :--- | :--- |
| **Role** | Uniquely identifies a record in its own table. | Links a record to another table's Primary Key. |
| **Duplicates** | ❌ Never allowed. | ✅ Allowed (many records can share one FK). |
| **NULL values** | ❌ Never allowed. | ✅ Allowed (optional relationship). |
| **Count per table** | Exactly 1 per table. | Can have multiple Foreign Keys per table. |
| **Table Type** | Parent or standalone table. | Child table. |

---

### ⚠️ Enabling Foreign Keys in SQLite

> **IMPORTANT**: By default, SQLite has foreign key constraints **disabled** for backward compatibility!  
> In every Python script or database session, you **must enable foreign key enforcement** immediately after connecting:

```python
import sqlite3

conn = sqlite3.connect("student_advanced.db")
cursor = conn.cursor()

# MUST RUN THIS TO ENFORCE FOREIGN KEY CHECKS:
cursor.execute("PRAGMA foreign_keys = ON;")
```

---

## 2. Database Normalization & Relationships

Instead of putting all information into one massive table:
- ❌ **Bad (Repeated data):**
  `| Harman | 22 | Python | 5000 | 6 Months | John (Instructor) |`
  *(If Python course fee changes, you have to update 100 student rows!)*
- ✅ **Good (Normalized):**
  `students` table stores student details + `course_id`.  
  `courses` table stores course name, fee, duration, instructor once.

---

## 3. SQL JOIN Operations

A **`JOIN`** clause combines rows from two or more tables based on a related column between them.

```
       TABLE: courses                   TABLE: students
     +----+-------------+             +----+--------+-----------+
     | id | course_name |             | id | name   | course_id |
     +----+-------------+             +----+--------+-----------+
     | 1  | Python      |             | 10 | Harman | 1         |
     | 2  | Web Dev     |             | 20 | Raman  | 2         |
     | 3  | Data Science|             | 30 | Amit   | NULL      |
     +----+-------------+             +----+--------+-----------+
```

---

### A. INNER JOIN
Returns only records that have **matching values in both tables**.

```
    [ Table A ] ─── ( MATCH ONLY ) ─── [ Table B ]
```

```sql
SELECT students.id, students.name, students.age, courses.course_name, courses.fee
FROM students
INNER JOIN courses ON students.course_id = courses.course_id;
```

*Output:*
| id | name | age | course_name | fee |
| :--- | :--- | :--- | :--- | :--- |
| 10 | Harman | 22 | Python | 5000 |
| 20 | Raman | 20 | Web Dev | 4500 |
*(Amit is excluded because `course_id` is NULL; Data Science is excluded because no student enrolled in it).*

---

### B. LEFT JOIN (or LEFT OUTER JOIN)
Returns **all records from the left table**, and the matched records from the right table. If no match is found, NULL is returned for right-table columns.

```
    [ ALL of Table A ] ─── ( Match if exists, else NULL ) ─── [ Table B ]
```

```sql
SELECT students.name, courses.course_name
FROM students
LEFT JOIN courses ON students.course_id = courses.course_id;
```

*Output:*
| name | course_name |
| :--- | :--- |
| Harman | Python |
| Raman | Web Dev |
| Amit | `NULL` *(Still appears, even without a course)* |

---

### C. RIGHT & FULL OUTER JOIN in SQLite
- **RIGHT JOIN**: Returns all records from the Right table (SQLite added support in version 3.39.0+; you can also achieve this by swapping table order in `LEFT JOIN`).
- **FULL OUTER JOIN**: Returns all records when there is a match in either table.

---

## 4. Aggregate Functions & Grouping

Aggregate functions perform calculations on multiple rows and return a single summary value.

### Basic Aggregates

| Function | What it does | SQL Example |
| :--- | :--- | :--- |
| **`COUNT()`** | Counts number of rows | `SELECT COUNT(*) FROM students;` |
| **`AVG()`** | Calculates average | `SELECT AVG(age) FROM students;` |
| **`SUM()`** | Calculates total sum | `SELECT SUM(fee) FROM courses;` |
| **`MIN()`** | Finds lowest value | `SELECT MIN(age) FROM students;` |
| **`MAX()`** | Finds highest value | `SELECT MAX(age) FROM students;` |

---

### GROUP BY
Groups rows that have the same values into summary rows (e.g., "Find total students in each course").

```sql
SELECT courses.course_name, COUNT(students.id) AS total_students
FROM courses
LEFT JOIN students ON courses.course_id = students.course_id
GROUP BY courses.course_name;
```

---

### HAVING vs WHERE

> **Key Difference**:
> - `WHERE` filters rows **before** aggregation happens.
> - `HAVING` filters groups **after** aggregation (`GROUP BY`) happens.

```sql
-- Find courses that have MORE THAN 1 student enrolled:
SELECT courses.course_name, COUNT(students.id) AS student_count
FROM courses
JOIN students ON courses.course_id = students.course_id
GROUP BY courses.course_name
HAVING student_count > 1;
```

---

## 5. Advanced Filtering & Sorting

### 1. `BETWEEN ... AND ...`
Filters within an inclusive range (numbers, dates, text).

```sql
-- Select students aged between 20 and 23 (inclusive: 20, 21, 22, 23)
SELECT * FROM students WHERE age BETWEEN 20 AND 23;
```

---

### 2. `IN (...)` and `NOT IN (...)`
Matches any value in a specified list.

```sql
-- Select students whose course_id is 1 or 3
SELECT * FROM students WHERE course_id IN (1, 3);

-- Select students NOT enrolled in courses 1 or 2
SELECT * FROM students WHERE course_id NOT IN (1, 2);
```

---

### 3. `LIKE` & Wildcards (Pattern Matching)
Used in text search:
- **`%`** represents zero, one, or multiple characters.
- **`_`** represents exactly one single character.

| Pattern | Meaning | Example Matches |
| :--- | :--- | :--- |
| `'H%'` | Starts with 'H' | 'Harman', 'Harry', 'Henry' |
| `'%man'` | Ends with 'man' | 'Harman', 'Raman', 'Salman' |
| `'%ar%'` | Contains 'ar' anywhere | 'Harman', 'Tara', 'Mark' |
| `'_a%'` | Second letter is 'a' | 'Harman', 'Raman' |

```sql
SELECT * FROM students WHERE name LIKE 'H%';
```

---

### 4. `IS NULL` and `IS NOT NULL`
To check for empty / missing values:

```sql
-- Find students who have not chosen a course yet
SELECT * FROM students WHERE course_id IS NULL;

-- Find students who have an assigned course
SELECT * FROM students WHERE course_id IS NOT NULL;
```

---

### 5. `ORDER BY` (Sorting)
Sorts results in Ascending (`ASC`, default) or Descending (`DESC`) order:

```sql
-- Sort students by age descending (oldest first), then by name ascending
SELECT * FROM students ORDER BY age DESC, name ASC;
```

---

### 6. `LIMIT` and `OFFSET` (Pagination)
Used to fetch a subset of rows (e.g. Page 1, Page 2):

```sql
-- Fetch only top 3 oldest students
SELECT * FROM students ORDER BY age DESC LIMIT 3;

-- Skip first 2 students, and fetch the next 2 (Pagination)
SELECT * FROM students ORDER BY id ASC LIMIT 2 OFFSET 2;
```

---

## 6. Complete Code Reference Cheat Sheet

```python
import sqlite3

# 1. Connect & Enable Foreign Keys
conn = sqlite3.connect("student_advanced.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# 2. Joins
cursor.execute("""
    SELECT s.name, c.course_name, c.fee
    FROM students s
    INNER JOIN courses c ON s.course_id = c.course_id
""")

# 3. Aggregations + Group By + Having
cursor.execute("""
    SELECT c.course_name, COUNT(s.id) AS total_enrolled, AVG(s.age) AS avg_age
    FROM courses c
    LEFT JOIN students s ON c.course_id = s.course_id
    GROUP BY c.course_name
    HAVING total_enrolled > 0
""")

# 4. Filtering: BETWEEN, LIKE, ORDER BY, LIMIT
cursor.execute("""
    SELECT * FROM students
    WHERE age BETWEEN 20 AND 25
      AND name LIKE '%man%'
    ORDER BY age DESC
    LIMIT 5
""")

# 5. Commit and Close
conn.commit()
conn.close()
```
