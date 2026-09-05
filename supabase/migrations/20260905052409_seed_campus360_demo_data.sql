/*
# Campus360 — Seed Demo Data

## Overview
Inserts demo data into the Supabase tables, mirroring the original portal.db seed data.
Auth users must be created separately via Supabase Auth (sign-up). This migration
inserts profile rows only — the user_id columns are left NULL for now and will be
linked when users sign up with matching emails.

## Data Inserted
1. admin — 1 admin row (username: admin)
2. faculty — 5 faculty rows (F001–F005)
3. students — 10 student rows (24B11CS001–010)
4. fees — 10 fee records
5. library — 10 issued book records
6. books — 10 book catalog entries
7. exams — 4 exam entries
8. timetable — 6 days of schedule
9. results — 10 semester results
10. backlogs — 4 backlog entries
11. halltickets — 10 hall ticket entries
12. payments — 10 payment records
13. receipts — 10 receipt records
14. notifications — 10 notification entries

## Note
Attendance and marks are NOT seeded here because the original inserted_data.py
had column mismatches. Those tables will be populated through the app UI.
*/

-- ============================================================
-- ADMIN
-- ============================================================
INSERT INTO admin (username, password) VALUES ('admin', 'admin123')
ON CONFLICT (username) DO NOTHING;

-- ============================================================
-- FACULTY
-- ============================================================
INSERT INTO faculty (facultyid, password, name, department, phone, email)
VALUES
  ('F001', 'faculty123', 'Dr. Srinivas', 'CSE', '9876543210', 'srinivas@campus360.com'),
  ('F002', 'faculty123', 'Dr. Lakshmi', 'ECE', '9876543211', 'lakshmi@campus360.com'),
  ('F003', 'faculty123', 'Dr. Kumar', 'EEE', '9876543212', 'kumar@campus360.com'),
  ('F004', 'faculty123', 'Dr. Prasad', 'MECH', '9876543213', 'prasad@campus360.com'),
  ('F005', 'faculty123', 'Dr. Raju', 'CIVIL', '9876543214', 'raju@campus360.com')
ON CONFLICT (facultyid) DO NOTHING;

-- ============================================================
-- STUDENTS
-- ============================================================
INSERT INTO students (rollno, password, name, branch, year, section, phone, email, address, dob, bloodgroup)
VALUES
  ('24B11CS001', '12345', 'Hari Krishna', 'CSE', '3', 'A', '9876543201', 'hari@gmail.com', 'Srikakulam', '10-08-2005', 'O+'),
  ('24B11CS002', '12345', 'Ramesh', 'CSE', '3', 'A', '9876543202', 'ramesh@gmail.com', 'Vizag', '12-03-2005', 'A+'),
  ('24B11CS003', '12345', 'Suresh', 'CSE', '3', 'A', '9876543203', 'suresh@gmail.com', 'Vizianagaram', '21-04-2005', 'B+'),
  ('24B11CS004', '12345', 'Mahesh', 'CSE', '3', 'A', '9876543204', 'mahesh@gmail.com', 'Tekkali', '18-07-2005', 'AB+'),
  ('24B11CS005', '12345', 'Kiran', 'CSE', '3', 'A', '9876543205', 'kiran@gmail.com', 'Palasa', '14-09-2005', 'O-'),
  ('24B11CS006', '12345', 'Ajay', 'CSE', '3', 'A', '9876543206', 'ajay@gmail.com', 'Sompeta', '16-11-2005', 'B-'),
  ('24B11CS007', '12345', 'Rahul', 'CSE', '3', 'A', '9876543207', 'rahul@gmail.com', 'Amadalavalasa', '02-01-2005', 'A-'),
  ('24B11CS008', '12345', 'Vamsi', 'CSE', '3', 'A', '9876543208', 'vamsi@gmail.com', 'Ichapuram', '05-02-2005', 'O+'),
  ('24B11CS009', '12345', 'Naresh', 'CSE', '3', 'A', '9876543209', 'naresh@gmail.com', 'Narasannapeta', '09-06-2005', 'B+'),
  ('24B11CS010', '12345', 'Karthik', 'CSE', '3', 'A', '9876543215', 'karthik@gmail.com', 'Rajam', '22-12-2005', 'A+')
ON CONFLICT (rollno) DO NOTHING;

-- ============================================================
-- FEES
-- ============================================================
INSERT INTO fees (rollno, total_fee, paid, balance, status)
VALUES
  ('24B11CS001', 50000, 50000, 0, 'Paid'),
  ('24B11CS002', 50000, 30000, 20000, 'Pending'),
  ('24B11CS003', 50000, 50000, 0, 'Paid'),
  ('24B11CS004', 50000, 25000, 25000, 'Pending'),
  ('24B11CS005', 50000, 50000, 0, 'Paid'),
  ('24B11CS006', 50000, 40000, 10000, 'Pending'),
  ('24B11CS007', 50000, 50000, 0, 'Paid'),
  ('24B11CS008', 50000, 35000, 15000, 'Pending'),
  ('24B11CS009', 50000, 50000, 0, 'Paid'),
  ('24B11CS010', 50000, 50000, 0, 'Paid')
ON CONFLICT DO NOTHING;

-- ============================================================
-- LIBRARY
-- ============================================================
INSERT INTO library (rollno, book_name, issue_date, return_date, status)
VALUES
  ('24B11CS001', 'Python Programming', '2026-06-01', '2026-06-15', 'Returned'),
  ('24B11CS002', 'Database System Concepts', '2026-06-03', '2026-06-17', 'Issued'),
  ('24B11CS003', 'Operating System Concepts', '2026-06-05', '2026-06-19', 'Issued'),
  ('24B11CS004', 'Computer Networks', '2026-06-07', '2026-06-21', 'Returned'),
  ('24B11CS005', 'Java Programming', '2026-06-09', '2026-06-23', 'Issued'),
  ('24B11CS006', 'Data Structures', '2026-06-11', '2026-06-25', 'Issued'),
  ('24B11CS007', 'Software Engineering', '2026-06-13', '2026-06-27', 'Returned'),
  ('24B11CS008', 'Artificial Intelligence', '2026-06-15', '2026-06-29', 'Issued'),
  ('24B11CS009', 'Machine Learning', '2026-06-17', '2026-07-01', 'Issued'),
  ('24B11CS010', 'Cloud Computing', '2026-06-19', '2026-07-03', 'Returned')
ON CONFLICT DO NOTHING;

-- ============================================================
-- BOOKS
-- ============================================================
INSERT INTO books (book_name, author, quantity)
VALUES
  ('Python Programming', 'Guido van Rossum', 15),
  ('Database System Concepts', 'Korth', 12),
  ('Operating System Concepts', 'Galvin', 10),
  ('Computer Networks', 'Forouzan', 8),
  ('Java Programming', 'Herbert Schildt', 20),
  ('Data Structures', 'Seymour Lipschutz', 14),
  ('Software Engineering', 'Pressman', 9),
  ('Artificial Intelligence', 'Stuart Russell', 6),
  ('Machine Learning', 'Tom Mitchell', 5),
  ('Cloud Computing', 'Rajkumar Buyya', 7)
ON CONFLICT DO NOTHING;

-- ============================================================
-- EXAMS
-- ============================================================
INSERT INTO exams (exam_name, exam_date, branch, year)
VALUES
  ('Mid-1', '2026-07-10', 'CSE', '3'),
  ('Mid-2', '2026-09-20', 'CSE', '3'),
  ('Semester', '2026-11-25', 'CSE', '3'),
  ('Lab Internal', '2026-08-05', 'CSE', '3')
ON CONFLICT DO NOTHING;

-- ============================================================
-- TIMETABLE
-- ============================================================
INSERT INTO timetable (branch, year, day, period1, period2, period3, period4, period5, period6)
VALUES
  ('CSE', '3', 'Monday', 'Python', 'DBMS', 'OS', 'Java', 'CN', 'AI'),
  ('CSE', '3', 'Tuesday', 'Java', 'Python', 'CN', 'DBMS', 'OS', 'ML'),
  ('CSE', '3', 'Wednesday', 'OS', 'AI', 'Python', 'Java', 'DBMS', 'Library'),
  ('CSE', '3', 'Thursday', 'CN', 'ML', 'OS', 'Python', 'Java', 'Sports'),
  ('CSE', '3', 'Friday', 'DBMS', 'Python Lab', 'Java Lab', 'OS Lab', 'Project', 'Seminar'),
  ('CSE', '3', 'Saturday', 'Aptitude', 'English', 'CRT', 'Mini Project', 'Library', 'Counselling')
ON CONFLICT DO NOTHING;

-- ============================================================
-- RESULTS
-- ============================================================
INSERT INTO results (rollno, semester, sgpa, cgpa, result)
VALUES
  ('24B11CS001', 'III-I', 9.42, 9.30, 'PASS'),
  ('24B11CS002', 'III-I', 9.05, 8.95, 'PASS'),
  ('24B11CS003', 'III-I', 8.77, 8.60, 'PASS'),
  ('24B11CS004', 'III-I', 8.17, 8.05, 'PASS'),
  ('24B11CS005', 'III-I', 9.55, 9.40, 'PASS'),
  ('24B11CS006', 'III-I', 8.05, 8.00, 'PASS'),
  ('24B11CS007', 'III-I', 7.72, 7.80, 'PASS'),
  ('24B11CS008', 'III-I', 9.15, 9.10, 'PASS'),
  ('24B11CS009', 'III-I', 8.75, 8.70, 'PASS'),
  ('24B11CS010', 'III-I', 9.45, 9.35, 'PASS')
ON CONFLICT DO NOTHING;

-- ============================================================
-- BACKLOGS
-- ============================================================
INSERT INTO backlogs (rollno, subject, status)
VALUES
  ('24B11CS002', 'Computer Networks', 'Cleared'),
  ('24B11CS004', 'Java Programming', 'Pending'),
  ('24B11CS006', 'DBMS', 'Pending'),
  ('24B11CS007', 'Operating Systems', 'Cleared')
ON CONFLICT DO NOTHING;

-- ============================================================
-- HALLTICKETS
-- ============================================================
INSERT INTO halltickets (rollno, hallticket_no, semester)
VALUES
  ('24B11CS001', 'HT2026001', 'III-I'),
  ('24B11CS002', 'HT2026002', 'III-I'),
  ('24B11CS003', 'HT2026003', 'III-I'),
  ('24B11CS004', 'HT2026004', 'III-I'),
  ('24B11CS005', 'HT2026005', 'III-I'),
  ('24B11CS006', 'HT2026006', 'III-I'),
  ('24B11CS007', 'HT2026007', 'III-I'),
  ('24B11CS008', 'HT2026008', 'III-I'),
  ('24B11CS009', 'HT2026009', 'III-I'),
  ('24B11CS010', 'HT2026010', 'III-I')
ON CONFLICT DO NOTHING;

-- ============================================================
-- PAYMENTS
-- ============================================================
INSERT INTO payments (rollno, amount, payment_date, payment_mode)
VALUES
  ('24B11CS001', 50000, '2026-06-01', 'UPI'),
  ('24B11CS002', 30000, '2026-06-02', 'Net Banking'),
  ('24B11CS003', 50000, '2026-06-03', 'Debit Card'),
  ('24B11CS004', 25000, '2026-06-04', 'Credit Card'),
  ('24B11CS005', 50000, '2026-06-05', 'UPI'),
  ('24B11CS006', 40000, '2026-06-06', 'Cash'),
  ('24B11CS007', 50000, '2026-06-07', 'UPI'),
  ('24B11CS008', 35000, '2026-06-08', 'Net Banking'),
  ('24B11CS009', 50000, '2026-06-09', 'Debit Card'),
  ('24B11CS010', 50000, '2026-06-10', 'Credit Card')
ON CONFLICT DO NOTHING;

-- ============================================================
-- RECEIPTS
-- ============================================================
INSERT INTO receipts (receipt_no, rollno, amount, receipt_date)
VALUES
  ('RCPT001', '24B11CS001', 50000, '2026-06-01'),
  ('RCPT002', '24B11CS002', 30000, '2026-06-02'),
  ('RCPT003', '24B11CS003', 50000, '2026-06-03'),
  ('RCPT004', '24B11CS004', 25000, '2026-06-04'),
  ('RCPT005', '24B11CS005', 50000, '2026-06-05'),
  ('RCPT006', '24B11CS006', 40000, '2026-06-06'),
  ('RCPT007', '24B11CS007', 50000, '2026-06-07'),
  ('RCPT008', '24B11CS008', 35000, '2026-06-08'),
  ('RCPT009', '24B11CS009', 50000, '2026-06-09'),
  ('RCPT010', '24B11CS010', 50000, '2026-06-10')
ON CONFLICT DO NOTHING;

-- ============================================================
-- NOTIFICATIONS
-- ============================================================
INSERT INTO notifications (title, message, date)
VALUES
  ('Semester Exams', 'Semester examinations start from 10 July 2026.', '2026-07-01'),
  ('Fee Payment', 'Last date to pay fee is 05 July 2026.', '2026-07-02'),
  ('Library Notice', 'Return library books before the due date.', '2026-07-03'),
  ('Holiday', 'College holiday on 15 August.', '2026-08-15'),
  ('Placement Drive', 'TCS Campus Drive on 20 August.', '2026-08-20'),
  ('Workshop', 'AI Workshop on 25 August.', '2026-08-25'),
  ('CRT Classes', 'CRT classes start from Monday.', '2026-09-01'),
  ('Sports Meet', 'Annual sports meet registration is open.', '2026-09-05'),
  ('Project Review', 'Mini project review on Friday.', '2026-09-10'),
  ('Results', 'Mid-1 results are published.', '2026-09-15')
ON CONFLICT DO NOTHING;
