import sqlite3

conn = sqlite3.connect("portal.db")
cursor = conn.cursor()

# =========================
# STUDENTS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
name TEXT NOT NULL,
branch TEXT,
year TEXT,
section TEXT,
phone TEXT,
email TEXT,
address TEXT,
dob TEXT,
bloodgroup TEXT
)
""")

# =========================
# ADMIN TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
""")

# =========================
# FACULTY TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty(
id INTEGER PRIMARY KEY AUTOINCREMENT,
facultyid TEXT UNIQUE,
password TEXT,
name TEXT,
department TEXT,
phone TEXT,
email TEXT
)
""")

# =========================
# ATTENDANCE TABLE
# =========================
cursor.execute("""
CREATE TABLE attendance(

id INTEGER PRIMARY KEY AUTOINCREMENT,

rollno TEXT NOT NULL,

branch TEXT NOT NULL,

year TEXT NOT NULL,

date TEXT NOT NULL,

period INTEGER NOT NULL,

status TEXT NOT NULL CHECK(status IN ('Present','Absent')),

FOREIGN KEY(rollno) REFERENCES students(rollno)

)
""")


# =========================
# MARKS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks(

id INTEGER PRIMARY KEY AUTOINCREMENT,

rollno TEXT NOT NULL,

branch TEXT NOT NULL,

year TEXT NOT NULL,

semester TEXT NOT NULL,

exam TEXT NOT NULL,

python INTEGER DEFAULT 0,

java INTEGER DEFAULT 0,

dbms INTEGER DEFAULT 0,

os INTEGER DEFAULT 0,

cn INTEGER DEFAULT 0,

total INTEGER DEFAULT 0,

percentage REAL DEFAULT 0,

grade TEXT,

result TEXT,

FOREIGN KEY(rollno) REFERENCES students(rollno)

)
""")

# =========================
# FEES TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS fees(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT,
total_fee INTEGER,
paid INTEGER,
balance INTEGER,
status TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# LIBRARY TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS library(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT,
book_name TEXT,
issue_date TEXT,
return_date TEXT,
status TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# TIMETABLE TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable(
id INTEGER PRIMARY KEY AUTOINCREMENT,
branch TEXT,
year TEXT,
day TEXT,
period1 TEXT,
period2 TEXT,
period3 TEXT,
period4 TEXT,
period5 TEXT,
period6 TEXT
)
""")

# =========================
# RESULTS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS results(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT,
semester TEXT,
sgpa REAL,
cgpa REAL,
result TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# BACKLOGS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS backlogs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT,
subject TEXT,
status TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# EXAMS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS exams(
id INTEGER PRIMARY KEY AUTOINCREMENT,
exam_name TEXT,
exam_date TEXT,
branch TEXT,
year TEXT
)
""")

# =========================
# HALLTICKETS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS halltickets(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT,
hallticket_no TEXT,
semester TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# PAYMENTS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS payments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
rollno TEXT,
amount INTEGER,
payment_date TEXT,
payment_mode TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# RECEIPTS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS receipts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
receipt_no TEXT,
rollno TEXT,
amount INTEGER,
receipt_date TEXT,
FOREIGN KEY(rollno) REFERENCES students(rollno)
)
""")

# =========================
# NOTIFICATIONS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
message TEXT,
date TEXT
)
""")

# =========================
# BOOKS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
id INTEGER PRIMARY KEY AUTOINCREMENT,
book_name TEXT,
author TEXT,
quantity INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")