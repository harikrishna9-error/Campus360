import sqlite3

conn = sqlite3.connect("portal.db")
cursor = conn.cursor()

# -------------------------
# CLEAR TABLES
# -------------------------

cursor.execute("DELETE FROM admin")
cursor.execute("DELETE FROM faculty")
cursor.execute("DELETE FROM students")

# -------------------------
# ADMIN
# -------------------------

cursor.execute("""

INSERT INTO admin
(username,password)

VALUES

('admin','admin123')

""")

# -------------------------
# FACULTY
# -------------------------

faculty = [

('F001','faculty123','Dr. Srinivas','CSE','9876543210','srinivas@campus360.com'),

('F002','faculty123','Dr. Lakshmi','ECE','9876543211','lakshmi@campus360.com'),

('F003','faculty123','Dr. Kumar','EEE','9876543212','kumar@campus360.com'),

('F004','faculty123','Dr. Prasad','MECH','9876543213','prasad@campus360.com'),

('F005','faculty123','Dr. Raju','CIVIL','9876543214','raju@campus360.com')

]

cursor.executemany("""

INSERT INTO faculty

(facultyid,password,name,department,phone,email)

VALUES

(?,?,?,?,?,?)

""",faculty)

# -------------------------
# STUDENTS
# -------------------------

students = [

('24B11CS001','12345','Hari Krishna','CSE','3','A','9876543201','hari@gmail.com','Srikakulam','10-08-2005','O+'),

('24B11CS002','12345','Ramesh','CSE','3','A','9876543202','ramesh@gmail.com','Vizag','12-03-2005','A+'),

('24B11CS003','12345','Suresh','CSE','3','A','9876543203','suresh@gmail.com','Vizianagaram','21-04-2005','B+'),

('24B11CS004','12345','Mahesh','CSE','3','A','9876543204','mahesh@gmail.com','Tekkali','18-07-2005','AB+'),

('24B11CS005','12345','Kiran','CSE','3','A','9876543205','kiran@gmail.com','Palasa','14-09-2005','O-'),

('24B11CS006','12345','Ajay','CSE','3','A','9876543206','ajay@gmail.com','Sompeta','16-11-2005','B-'),

('24B11CS007','12345','Rahul','CSE','3','A','9876543207','rahul@gmail.com','Amadalavalasa','02-01-2005','A-'),

('24B11CS008','12345','Vamsi','CSE','3','A','9876543208','vamsi@gmail.com','Ichapuram','05-02-2005','O+'),

('24B11CS009','12345','Naresh','CSE','3','A','9876543209','naresh@gmail.com','Narasannapeta','09-06-2005','B+'),

('24B11CS010','12345','Karthik','CSE','3','A','9876543215','karthik@gmail.com','Rajam','22-12-2005','A+')

]

cursor.executemany("""

INSERT INTO students

(

rollno,
password,
name,
branch,
year,
section,
phone,
email,
address,
dob,
bloodgroup

)

VALUES

(

?,?,?,?,?,?,?,?,?,?,?

)

""",students)

# -------------------------
# CLEAR TABLES
# -------------------------

cursor.execute("DELETE FROM attendance")
cursor.execute("DELETE FROM marks")
cursor.execute("DELETE FROM fees")
cursor.execute("DELETE FROM results")
cursor.execute("DELETE FROM backlogs")

# -------------------------
# ATTENDANCE
# -------------------------

attendance = [

('24B11CS001',120,118,98.33),
('24B11CS002',120,115,95.83),
('24B11CS003',120,112,93.33),
('24B11CS004',120,110,91.67),
('24B11CS005',120,117,97.50),
('24B11CS006',120,111,92.50),
('24B11CS007',120,109,90.83),
('24B11CS008',120,116,96.67),
('24B11CS009',120,114,95.00),
('24B11CS010',120,118,98.33)

]

cursor.executemany("""

INSERT INTO attendance

(

rollno,
total_classes,
present_classes,
percentage

)

VALUES

(?,?,?,?)

""",attendance)

# -------------------------
# MARKS
# -------------------------

marks = [

('24B11CS001',95,92,96,94,377,9.42),
('24B11CS002',90,91,89,92,362,9.05),
('24B11CS003',88,86,90,87,351,8.77),
('24B11CS004',82,84,81,80,327,8.17),
('24B11CS005',96,95,94,97,382,9.55),
('24B11CS006',79,80,82,81,322,8.05),
('24B11CS007',75,78,79,77,309,7.72),
('24B11CS008',91,90,93,92,366,9.15),
('24B11CS009',87,88,86,89,350,8.75),
('24B11CS010',94,93,95,96,378,9.45)

]

cursor.executemany("""

INSERT INTO marks

(

rollno,
python,
java,
dbms,
os,
total,
cgpa

)

VALUES

(?,?,?,?,?,?,?)

""",marks)

# -------------------------
# FEES
# -------------------------

fees = [

('24B11CS001',50000,50000,0,'Paid'),
('24B11CS002',50000,30000,20000,'Pending'),
('24B11CS003',50000,50000,0,'Paid'),
('24B11CS004',50000,25000,25000,'Pending'),
('24B11CS005',50000,50000,0,'Paid'),
('24B11CS006',50000,40000,10000,'Pending'),
('24B11CS007',50000,50000,0,'Paid'),
('24B11CS008',50000,35000,15000,'Pending'),
('24B11CS009',50000,50000,0,'Paid'),
('24B11CS010',50000,50000,0,'Paid')

]

cursor.executemany("""

INSERT INTO fees

(

rollno,
total_fee,
paid,
balance,
status

)

VALUES

(?,?,?,?,?)

""",fees)

# -------------------------
# RESULTS
# -------------------------

results = [

('24B11CS001','III-I',9.42,9.30,'PASS'),
('24B11CS002','III-I',9.05,8.95,'PASS'),
('24B11CS003','III-I',8.77,8.60,'PASS'),
('24B11CS004','III-I',8.17,8.05,'PASS'),
('24B11CS005','III-I',9.55,9.40,'PASS'),
('24B11CS006','III-I',8.05,8.00,'PASS'),
('24B11CS007','III-I',7.72,7.80,'PASS'),
('24B11CS008','III-I',9.15,9.10,'PASS'),
('24B11CS009','III-I',8.75,8.70,'PASS'),
('24B11CS010','III-I',9.45,9.35,'PASS')

]

cursor.executemany("""

INSERT INTO results

(

rollno,
semester,
sgpa,
cgpa,
result

)

VALUES

(?,?,?,?,?)

""",results)

# -------------------------
# BACKLOGS
# -------------------------

backlogs = [

('24B11CS002','Computer Networks','Cleared'),
('24B11CS004','Java Programming','Pending'),
('24B11CS006','DBMS','Pending'),
('24B11CS007','Operating Systems','Cleared')

]

cursor.executemany("""

INSERT INTO backlogs

(

rollno,
subject,
status

)

VALUES

(?,?,?)

""",backlogs)

# -------------------------
# CLEAR TABLES
# -------------------------

cursor.execute("DELETE FROM library")
cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM exams")
cursor.execute("DELETE FROM timetable")
cursor.execute("DELETE FROM halltickets")

# -------------------------
# LIBRARY
# -------------------------

library = [

('24B11CS001','Python Programming','2026-06-01','2026-06-15','Returned'),
('24B11CS002','Database System Concepts','2026-06-03','2026-06-17','Issued'),
('24B11CS003','Operating System Concepts','2026-06-05','2026-06-19','Issued'),
('24B11CS004','Computer Networks','2026-06-07','2026-06-21','Returned'),
('24B11CS005','Java Programming','2026-06-09','2026-06-23','Issued'),
('24B11CS006','Data Structures','2026-06-11','2026-06-25','Issued'),
('24B11CS007','Software Engineering','2026-06-13','2026-06-27','Returned'),
('24B11CS008','Artificial Intelligence','2026-06-15','2026-06-29','Issued'),
('24B11CS009','Machine Learning','2026-06-17','2026-07-01','Issued'),
('24B11CS010','Cloud Computing','2026-06-19','2026-07-03','Returned')

]

cursor.executemany("""

INSERT INTO library

(

rollno,
book_name,
issue_date,
return_date,
status

)

VALUES

(?,?,?,?,?)

""", library)

# -------------------------
# BOOKS
# -------------------------

books = [

('Python Programming','Guido van Rossum',15),
('Database System Concepts','Korth',12),
('Operating System Concepts','Galvin',10),
('Computer Networks','Forouzan',8),
('Java Programming','Herbert Schildt',20),
('Data Structures','Seymour Lipschutz',14),
('Software Engineering','Pressman',9),
('Artificial Intelligence','Stuart Russell',6),
('Machine Learning','Tom Mitchell',5),
('Cloud Computing','Rajkumar Buyya',7)

]

cursor.executemany("""

INSERT INTO books

(

book_name,
author,
quantity

)

VALUES

(?,?,?)

""", books)

# -------------------------
# EXAMS
# -------------------------

exams = [

('Mid-1','2026-07-10','CSE','3'),
('Mid-2','2026-09-20','CSE','3'),
('Semester','2026-11-25','CSE','3'),
('Lab Internal','2026-08-05','CSE','3')

]

cursor.executemany("""

INSERT INTO exams

(

exam_name,
exam_date,
branch,
year

)

VALUES

(?,?,?,?)

""", exams)

# -------------------------
# TIMETABLE
# -------------------------

timetable = [

('CSE','3','Monday','Python','DBMS','OS','Java','CN','AI'),
('CSE','3','Tuesday','Java','Python','CN','DBMS','OS','ML'),
('CSE','3','Wednesday','OS','AI','Python','Java','DBMS','Library'),
('CSE','3','Thursday','CN','ML','OS','Python','Java','Sports'),
('CSE','3','Friday','DBMS','Python Lab','Java Lab','OS Lab','Project','Seminar'),
('CSE','3','Saturday','Aptitude','English','CRT','Mini Project','Library','Counselling')

]

cursor.executemany("""

INSERT INTO timetable

(

branch,
year,
day,
period1,
period2,
period3,
period4,
period5,
period6

)

VALUES

(?,?,?,?,?,?,?,?,?)

""", timetable)

# -------------------------
# HALLTICKETS
# -------------------------

halltickets = [

('24B11CS001','HT2026001','III-I'),
('24B11CS002','HT2026002','III-I'),
('24B11CS003','HT2026003','III-I'),
('24B11CS004','HT2026004','III-I'),
('24B11CS005','HT2026005','III-I'),
('24B11CS006','HT2026006','III-I'),
('24B11CS007','HT2026007','III-I'),
('24B11CS008','HT2026008','III-I'),
('24B11CS009','HT2026009','III-I'),
('24B11CS010','HT2026010','III-I')

]

cursor.executemany("""

INSERT INTO halltickets

(

rollno,
hallticket_no,
semester

)

VALUES

(?,?,?)

""", halltickets)

# -------------------------
# CLEAR TABLES
# -------------------------

cursor.execute("DELETE FROM payments")
cursor.execute("DELETE FROM receipts")
cursor.execute("DELETE FROM notifications")

# -------------------------
# PAYMENTS
# -------------------------

payments = [

('24B11CS001',50000,'2026-06-01','UPI'),
('24B11CS002',30000,'2026-06-02','Net Banking'),
('24B11CS003',50000,'2026-06-03','Debit Card'),
('24B11CS004',25000,'2026-06-04','Credit Card'),
('24B11CS005',50000,'2026-06-05','UPI'),
('24B11CS006',40000,'2026-06-06','Cash'),
('24B11CS007',50000,'2026-06-07','UPI'),
('24B11CS008',35000,'2026-06-08','Net Banking'),
('24B11CS009',50000,'2026-06-09','Debit Card'),
('24B11CS010',50000,'2026-06-10','Credit Card')

]

cursor.executemany("""

INSERT INTO payments

(

rollno,
amount,
payment_date,
payment_mode

)

VALUES

(?,?,?,?)

""", payments)

# -------------------------
# RECEIPTS
# -------------------------

receipts = [

('RCPT001','24B11CS001',50000,'2026-06-01'),
('RCPT002','24B11CS002',30000,'2026-06-02'),
('RCPT003','24B11CS003',50000,'2026-06-03'),
('RCPT004','24B11CS004',25000,'2026-06-04'),
('RCPT005','24B11CS005',50000,'2026-06-05'),
('RCPT006','24B11CS006',40000,'2026-06-06'),
('RCPT007','24B11CS007',50000,'2026-06-07'),
('RCPT008','24B11CS008',35000,'2026-06-08'),
('RCPT009','24B11CS009',50000,'2026-06-09'),
('RCPT010','24B11CS010',50000,'2026-06-10')

]

cursor.executemany("""

INSERT INTO receipts

(

receipt_no,
rollno,
amount,
receipt_date

)

VALUES

(?,?,?,?)

""", receipts)

# -------------------------
# NOTIFICATIONS
# -------------------------

notifications = [

('Semester Exams','Semester examinations start from 10 July 2026.','2026-07-01'),

('Fee Payment','Last date to pay fee is 05 July 2026.','2026-07-02'),

('Library Notice','Return library books before the due date.','2026-07-03'),

('Holiday','College holiday on 15 August.','2026-08-15'),

('Placement Drive','TCS Campus Drive on 20 August.','2026-08-20'),

('Workshop','AI Workshop on 25 August.','2026-08-25'),

('CRT Classes','CRT classes start from Monday.','2026-09-01'),

('Sports Meet','Annual sports meet registration is open.','2026-09-05'),

('Project Review','Mini project review on Friday.','2026-09-10'),

('Results','Mid-1 results are published.','2026-09-15')

]

cursor.executemany("""

INSERT INTO notifications

(

title,
message,
date

)

VALUES

(?,?,?)

""", notifications)

conn.commit()

conn.close()

print("=" * 50)
print("Data Inserted  Successfully")
print("=" * 50)
print("Admin Login")
print("Username : admin")
print("Password : admin123")
print()
print("Faculty Login")
print("Faculty ID : F001")
print("Password   : faculty123")
print()
print("Student Login")
print("Roll No : 24B11CS001")
print("Password: 12345")
print("=" * 50)

