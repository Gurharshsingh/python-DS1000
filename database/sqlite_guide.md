# 📘 SQLite & Python: Complete Beginner's Guide

A friendly, step-by-step guide to understanding databases, SQL commands, and how Python interacts with SQLite.

---

## 📑 Table of Contents
1. [What is a Database?](#1-what-is-a-database)
2. [What makes SQLite Special?](#2-what-makes-sqlite-special)
3. [The Core Mental Model (Analogy)](#3-the-core-mental-model-analogy)
4. [SQLite Data Types & Constraints](#4-sqlite-data-types--constraints)
5. [The 4 Core Operations: CRUD](#5-the-4-core-operations-crud)
   - [Create (Table & Data)](#1-create)
   - [Read (Querying Data)](#2-read)
   - [Update (Modifying Data)](#3-update)
   - [Delete (Removing Data)](#4-delete)
6. [Crucial Python + SQLite Concepts](#6-crucial-python--sqlite-concepts)
7. [Quick Reference Cheat Sheet](#7-quick-reference-cheat-sheet)

---

## 1. What is a Database?

Think of a database as an **organized, electronic filing cabinet** or an **Excel workbook**.

* **Database (`.db` file)**: The entire Excel file / notebook.
* **Table**: A single sheet inside that notebook (e.g., `students`, `courses`, `teachers`).
* **Column (Field)**: The headers at the top (e.g., `id`, `name`, `age`, `course`).
* **Row (Record)**: A single student's entry (e.g., `1 | Harman | 22 | MCA`).

```
+----+--------+-----+--------+  <-- Columns (Headers)
| id | name   | age | course |
+----+--------+-----+--------+
| 1  | Harman | 22  | MCA    |  <-- Row 1 (Record)
| 2  | Ram    | 22  | BTech  |  <-- Row 2 (Record)
+----+--------+-----+--------+
```

---

## 2. What makes SQLite Special?

Most traditional databases (like MySQL, PostgreSQL, Oracle) require you to install a separate server program that runs in the background.

**SQLite is different:**
- **Serverless & Self-Contained**: The entire database lives in a single simple file (like `student.db`) on your disk.
- **Zero Configuration**: Built directly into Python (`import sqlite3`). No installations or setup needed.
- **Lightweight & Fast**: Perfect for desktop apps, mobile apps, learning, and testing.

---

## 3. The Core Mental Model (Analogy)

When writing Python code to talk to SQLite, remember these 5 roles:

| Concept in Code | Real-World Analogy | What it actually does |
| :--- | :--- | :--- |
| **`sqlite3.connect("student.db")`** | **Opening the notebook** | Establishes a link (`conn`) to the database file. Creates the file if it doesn't exist. |
| **`conn.cursor()`** | **Your Pen / Assistant** | Creates a `cursor` object. The cursor is the worker that travels through rows and runs commands. |
| **`cursor.execute("SQL...")`** | **Giving an instruction** | Passes a command written in SQL language to the cursor to run. |
| **`conn.commit()`** | **Pressing Ctrl + S (Save)** | Permanently writes and saves your changes to the `.db` file on disk. |
| **`cursor.fetchall()`** | **Reading notes back** | Pulls the queried records from the database into a Python list of tuples. |
| **`conn.close()`** | **Closing the notebook** | Safely disconnects and releases file locks. |

---

## 4. SQLite Data Types & Constraints

### Common Data Types
| Data Type | Description | Python Equivalent | Example |
| :--- | :--- | :--- | :--- |
| `INTEGER` | Whole numbers | `int` | `1`, `22`, `100` |
| `TEXT` | Strings/Words | `str` | `'Harman'`, `'MCA'` |
| `REAL` | Decimal numbers | `float` | `95.5`, `3.14` |
| `BLOB` | Binary data (images, files) | `bytes` | `b'raw_bytes'` |
| `NULL` | Empty / No value | `None` | `NULL` |

### Common Constraints (Rules for Columns)
- **`PRIMARY KEY`**: Unique identifier for every row. No two rows can have the same primary key.
- **`AUTOINCREMENT`**: Automatically gives `1, 2, 3, ...` as new rows are added.
- **`NOT NULL`**: Column cannot be left empty.
- **`UNIQUE`**: Every value in this column must be distinct (e.g., email addresses).
- **`DEFAULT <val>`**: Gives a fallback value if none is provided.

---

## 5. The 4 Core Operations: CRUD

CRUD stands for **Create, Read, Update, Delete** — the four essential actions you do with data.

```
      ┌───────────┐
      │   CRUD    │
      └─────┬─────┘
   ┌────────┼────────┬────────┐
   ▼        ▼        ▼        ▼
Create    Read    Update   Delete
(INSERT) (SELECT) (UPDATE) (DELETE)
```

---

### 1. CREATE

#### A. Creating a Table
```sql
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
);
```

#### B. Inserting a Single Row
```sql
INSERT INTO students (name, age, course) VALUES ('Harman', 22, 'MCA');
```
*In Python (Parameterized):*
```python
cursor.execute("""
    INSERT INTO students (name, age, course) VALUES (?, ?, ?)
""", ("Harman", 22, "MCA"))
conn.commit()  # <-- Always commit write operations!
```

#### C. Inserting Multiple Rows (`executemany`)
```python
students_list = [
    ("Ram", 22, "BTech"),
    ("Raman", 20, "BCA"),
    ("Mohit", 23, "BBA")
]

cursor.executemany("""
    INSERT INTO students (name, age, course) VALUES (?, ?, ?)
""", students_list)
conn.commit()
```

---

### 2. READ

#### A. Fetching All Rows
```sql
SELECT * FROM students;
```
*In Python:*
```python
cursor.execute("SELECT * FROM students")
data = cursor.fetchall()  # Returns: [(1, 'Harman', 22, 'MCA'), (2, 'Ram', 22, 'BTech'), ...]

for row in data:
    print(row)
```

#### B. Fetching Specific Columns
```sql
SELECT name, course FROM students;
```

#### C. Filtering with `WHERE`
```sql
SELECT * FROM students WHERE age > 21;
SELECT * FROM students WHERE course = 'MCA';
```
*In Python with parameter:*
```python
cursor.execute("SELECT * FROM students WHERE course = ?", ("MCA",))
records = cursor.fetchall()
```

#### D. `fetchall()` vs `fetchone()`
- **`cursor.fetchall()`**: Returns a list of all matching rows: `[(...), (...)]`
- **`cursor.fetchone()`**: Returns just the first matching row: `(...)` or `None` if not found.

---

### 3. UPDATE

Modifies existing data in a table.

```sql
UPDATE students SET course = 'MBA' WHERE id = 1;
```

*In Python:*
```python
cursor.execute("""
    UPDATE students SET course = ? WHERE id = ?
""", ("MBA", 1))
conn.commit()  # <-- Don't forget to commit!
```

> ⚠️ **WARNING**: If you omit the `WHERE` clause (`UPDATE students SET course = 'MBA'`), **every single row** in your table will be updated!

---

### 4. DELETE

Removes rows from a table.

```sql
DELETE FROM students WHERE id = 5;
```

*In Python:*
```python
cursor.execute("""
    DELETE FROM students WHERE id = ?
""", (5,))
conn.commit()  # <-- Don't forget to commit!
```

> ⚠️ **WARNING**: If you omit the `WHERE` clause (`DELETE FROM students`), **all rows will be wiped out**!

---

## 6. Crucial Python + SQLite Concepts

### 1. Why do we use `?` (Placeholders) instead of f-strings?
❌ **DON'T DO THIS (Vulnerable to SQL Injection & Syntax Errors):**
```python
user_input = "Harman"
cursor.execute(f"INSERT INTO students (name) VALUES ('{user_input}')")
```

✅ **DO THIS (Safe parameterized query):**
```python
user_input = "Harman"
cursor.execute("INSERT INTO students (name) VALUES (?)", (user_input,))
```
SQLite automatically escapes special characters and prevents malicious inputs.

---

### 2. Single-element Tuple Trailing Comma `(val,)`
In Python:
- `(5)` is just the integer `5` in parentheses.
- `(5,)` with a comma is a **1-element tuple**.

Since `cursor.execute()` expects parameters to be inside a tuple or list, always include the comma for single values:
```python
cursor.execute("DELETE FROM students WHERE id = ?", (5,))  # Notice the comma after 5
```

---

### 3. Forgetting `conn.commit()`
Read queries (`SELECT`) do not change data, so they do **not** need `conn.commit()`.
Write queries (`INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE`, `DROP TABLE`) **will NOT be saved permanently to disk** unless you call `conn.commit()`.

---

## 7. Quick Reference Cheat Sheet

```python
import sqlite3

# 1. Connect and create cursor
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# 2. Create Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        course TEXT
    )
""")
conn.commit()

# 3. Insert One
cursor.execute("INSERT INTO students (name, age, course) VALUES (?,?,?)", ("Alice", 21, "CS"))
conn.commit()

# 4. Insert Many
rows = [("Bob", 22, "IT"), ("Charlie", 20, "CS")]
cursor.executemany("INSERT INTO students (name, age, course) VALUES (?,?,?)", rows)
conn.commit()

# 5. Read / Select
cursor.execute("SELECT * FROM students WHERE course = ?", ("CS",))
for student in cursor.fetchall():
    print(student)

# 6. Update
cursor.execute("UPDATE students SET age = ? WHERE name = ?", (23, "Alice"))
conn.commit()

# 7. Delete
cursor.execute("DELETE FROM students WHERE name = ?", ("Bob",))
conn.commit()

# 8. Close Connection
conn.close()
```
