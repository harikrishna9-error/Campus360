/*
# Campus360 ERP — Create All Tables

## Overview
Creates all 16 tables from the portal.db schema in Supabase.
Tables are created WITHOUT RLS policies first — policies come in a separate migration
to avoid circular dependency issues (students policies reference admin table, etc.).

## New Tables (16)
1. students — student profiles (rollno, name, branch, year, section, etc.)
2. admin — admin profiles (username)
3. faculty — faculty profiles (facultyid, name, department, etc.)
4. attendance — per-period attendance (rollno, branch, year, date, period, status)
5. marks — exam marks (python, java, dbms, os, cn, total, percentage, grade, result)
6. fees — fee records (total_fee, paid, balance, status)
7. library — issued books (book_name, issue_date, return_date, status)
8. timetable — weekly schedule (branch, year, day, period1–period6)
9. results — semester results (sgpa, cgpa, result)
10. backlogs — backlog subjects (subject, status)
11. exams — exam schedule (exam_name, exam_date, branch, year)
12. halltickets — hall tickets (hallticket_no, semester)
13. payments — payment history (amount, payment_date, payment_mode)
14. receipts — fee receipts (receipt_no, amount, receipt_date)
15. notifications — announcements (title, message, date)
16. books — library catalog (book_name, author, quantity)

## Notes
- All tables use IDENTITY columns for integer PKs (Supabase best practice).
- user_id columns link students/faculty/admin to auth.users.
- RLS is enabled on every table but policies are added in the next migration.
*/

-- ============================================================
-- 1. ADMIN
-- ============================================================
CREATE TABLE IF NOT EXISTS admin (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  username text UNIQUE,
  password text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE admin ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 2. FACULTY
-- ============================================================
CREATE TABLE IF NOT EXISTS faculty (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  facultyid text UNIQUE,
  password text,
  name text NOT NULL,
  department text,
  phone text,
  email text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE faculty ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 3. STUDENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS students (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  rollno text UNIQUE NOT NULL,
  password text,
  name text NOT NULL,
  branch text,
  year text,
  section text,
  phone text,
  email text,
  address text,
  dob text,
  bloodgroup text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE students ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 4. ATTENDANCE
-- ============================================================
CREATE TABLE IF NOT EXISTS attendance (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text NOT NULL,
  branch text NOT NULL,
  year text NOT NULL,
  date text NOT NULL,
  period integer NOT NULL,
  status text NOT NULL CHECK (status IN ('Present', 'Absent')),
  created_at timestamptz DEFAULT now()
);
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 5. MARKS
-- ============================================================
CREATE TABLE IF NOT EXISTS marks (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text NOT NULL,
  branch text NOT NULL,
  year text NOT NULL,
  semester text NOT NULL,
  exam text NOT NULL,
  python integer DEFAULT 0,
  java integer DEFAULT 0,
  dbms integer DEFAULT 0,
  os integer DEFAULT 0,
  cn integer DEFAULT 0,
  total integer DEFAULT 0,
  percentage real DEFAULT 0,
  grade text,
  result text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE marks ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 6. FEES
-- ============================================================
CREATE TABLE IF NOT EXISTS fees (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text,
  total_fee integer,
  paid integer,
  balance integer,
  status text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE fees ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 7. LIBRARY
-- ============================================================
CREATE TABLE IF NOT EXISTS library (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text,
  book_name text,
  issue_date text,
  return_date text,
  status text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE library ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 8. TIMETABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS timetable (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  branch text,
  year text,
  day text,
  period1 text,
  period2 text,
  period3 text,
  period4 text,
  period5 text,
  period6 text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE timetable ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 9. RESULTS
-- ============================================================
CREATE TABLE IF NOT EXISTS results (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text,
  semester text,
  sgpa real,
  cgpa real,
  result text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE results ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 10. BACKLOGS
-- ============================================================
CREATE TABLE IF NOT EXISTS backlogs (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text,
  subject text,
  status text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE backlogs ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 11. EXAMS
-- ============================================================
CREATE TABLE IF NOT EXISTS exams (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  exam_name text,
  exam_date text,
  branch text,
  year text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE exams ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 12. HALLTICKETS
-- ============================================================
CREATE TABLE IF NOT EXISTS halltickets (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text,
  hallticket_no text,
  semester text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE halltickets ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 13. PAYMENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS payments (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  rollno text,
  amount integer,
  payment_date text,
  payment_mode text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 14. RECEIPTS
-- ============================================================
CREATE TABLE IF NOT EXISTS receipts (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  receipt_no text,
  rollno text,
  amount integer,
  receipt_date text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE receipts ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 15. NOTIFICATIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS notifications (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title text,
  message text,
  date text,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- 16. BOOKS
-- ============================================================
CREATE TABLE IF NOT EXISTS books (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  book_name text,
  author text,
  quantity integer,
  created_at timestamptz DEFAULT now()
);
ALTER TABLE books ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_attendance_rollno ON attendance(rollno);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);
CREATE INDEX IF NOT EXISTS idx_attendance_branch_year ON attendance(branch, year);
CREATE INDEX IF NOT EXISTS idx_marks_rollno ON marks(rollno);
CREATE INDEX IF NOT EXISTS idx_marks_branch_year ON marks(branch, year);
CREATE INDEX IF NOT EXISTS idx_fees_rollno ON fees(rollno);
CREATE INDEX IF NOT EXISTS idx_library_rollno ON library(rollno);
CREATE INDEX IF NOT EXISTS idx_timetable_branch_year ON timetable(branch, year);
CREATE INDEX IF NOT EXISTS idx_results_rollno ON results(rollno);
CREATE INDEX IF NOT EXISTS idx_backlogs_rollno ON backlogs(rollno);
CREATE INDEX IF NOT EXISTS idx_exams_branch_year ON exams(branch, year);
CREATE INDEX IF NOT EXISTS idx_halltickets_rollno ON halltickets(rollno);
CREATE INDEX IF NOT EXISTS idx_payments_rollno ON payments(rollno);
CREATE INDEX IF NOT EXISTS idx_receipts_rollno ON receipts(rollno);
CREATE INDEX IF NOT EXISTS idx_students_rollno ON students(rollno);
CREATE INDEX IF NOT EXISTS idx_students_branch_year ON students(branch, year);
