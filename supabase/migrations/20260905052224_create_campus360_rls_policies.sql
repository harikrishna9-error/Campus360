/*
# Campus360 ERP — RLS Policies

## Overview
Adds row-level security policies to all 16 tables.

## Security Model
- **students**: students see own row; admin+faculty see all; admin can insert/update/delete.
- **admin**: admins see own row + all admin rows (for role checks).
- **faculty**: faculty see own row; admin sees all; admin can insert/update/delete.
- **attendance, marks**: all authenticated can SELECT; admin+faculty can INSERT/UPDATE/DELETE.
- **fees, library, timetable, results, backlogs, exams, halltickets, payments, receipts, books, notifications**: all authenticated can SELECT; admin can INSERT/UPDATE/DELETE.
- Role checks use EXISTS subqueries against admin/faculty tables (which exist now).

## Policy Pattern
- 4 policies per table (SELECT, INSERT, UPDATE, DELETE) — no FOR ALL shortcuts.
- Role verification: EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid()).
*/

-- ============================================================
-- ADMIN POLICIES
-- ============================================================
DROP POLICY IF EXISTS "admin_select_own" ON admin;
CREATE POLICY "admin_select_own" ON admin FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "admin_select_all_admin" ON admin;
CREATE POLICY "admin_select_all_admin" ON admin FOR SELECT
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- FACULTY POLICIES
-- ============================================================
DROP POLICY IF EXISTS "faculty_select_own" ON faculty;
CREATE POLICY "faculty_select_own" ON faculty FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "faculty_select_staff" ON faculty;
CREATE POLICY "faculty_select_staff" ON faculty FOR SELECT
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "faculty_insert_admin" ON faculty;
CREATE POLICY "faculty_insert_admin" ON faculty FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "faculty_update_admin" ON faculty;
CREATE POLICY "faculty_update_admin" ON faculty FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "faculty_delete_admin" ON faculty;
CREATE POLICY "faculty_delete_admin" ON faculty FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- STUDENTS POLICIES
-- ============================================================
DROP POLICY IF EXISTS "students_select_own" ON students;
CREATE POLICY "students_select_own" ON students FOR SELECT
  TO authenticated USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "students_select_staff" ON students;
CREATE POLICY "students_select_staff" ON students FOR SELECT
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "students_insert_admin" ON students;
CREATE POLICY "students_insert_admin" ON students FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "students_update_admin" ON students;
CREATE POLICY "students_update_admin" ON students FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "students_delete_admin" ON students;
CREATE POLICY "students_delete_admin" ON students FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- ATTENDANCE POLICIES
-- ============================================================
DROP POLICY IF EXISTS "attendance_select_all" ON attendance;
CREATE POLICY "attendance_select_all" ON attendance FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "attendance_insert_staff" ON attendance;
CREATE POLICY "attendance_insert_staff" ON attendance FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "attendance_update_staff" ON attendance;
CREATE POLICY "attendance_update_staff" ON attendance FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "attendance_delete_staff" ON attendance;
CREATE POLICY "attendance_delete_staff" ON attendance FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

-- ============================================================
-- MARKS POLICIES
-- ============================================================
DROP POLICY IF EXISTS "marks_select_all" ON marks;
CREATE POLICY "marks_select_all" ON marks FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "marks_insert_staff" ON marks;
CREATE POLICY "marks_insert_staff" ON marks FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "marks_update_staff" ON marks;
CREATE POLICY "marks_update_staff" ON marks FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "marks_delete_staff" ON marks;
CREATE POLICY "marks_delete_staff" ON marks FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
    OR EXISTS (SELECT 1 FROM faculty f WHERE f.user_id = auth.uid())
  );

-- ============================================================
-- FEES POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "fees_select_all" ON fees;
CREATE POLICY "fees_select_all" ON fees FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "fees_insert_admin" ON fees;
CREATE POLICY "fees_insert_admin" ON fees FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "fees_update_admin" ON fees;
CREATE POLICY "fees_update_admin" ON fees FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "fees_delete_admin" ON fees;
CREATE POLICY "fees_delete_admin" ON fees FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- LIBRARY POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "library_select_all" ON library;
CREATE POLICY "library_select_all" ON library FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "library_insert_admin" ON library;
CREATE POLICY "library_insert_admin" ON library FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "library_update_admin" ON library;
CREATE POLICY "library_update_admin" ON library FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "library_delete_admin" ON library;
CREATE POLICY "library_delete_admin" ON library FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- TIMETABLE POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "timetable_select_all" ON timetable;
CREATE POLICY "timetable_select_all" ON timetable FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "timetable_insert_admin" ON timetable;
CREATE POLICY "timetable_insert_admin" ON timetable FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "timetable_update_admin" ON timetable;
CREATE POLICY "timetable_update_admin" ON timetable FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "timetable_delete_admin" ON timetable;
CREATE POLICY "timetable_delete_admin" ON timetable FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- RESULTS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "results_select_all" ON results;
CREATE POLICY "results_select_all" ON results FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "results_insert_admin" ON results;
CREATE POLICY "results_insert_admin" ON results FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "results_update_admin" ON results;
CREATE POLICY "results_update_admin" ON results FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "results_delete_admin" ON results;
CREATE POLICY "results_delete_admin" ON results FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- BACKLOGS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "backlogs_select_all" ON backlogs;
CREATE POLICY "backlogs_select_all" ON backlogs FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "backlogs_insert_admin" ON backlogs;
CREATE POLICY "backlogs_insert_admin" ON backlogs FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "backlogs_update_admin" ON backlogs;
CREATE POLICY "backlogs_update_admin" ON backlogs FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "backlogs_delete_admin" ON backlogs;
CREATE POLICY "backlogs_delete_admin" ON backlogs FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- EXAMS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "exams_select_all" ON exams;
CREATE POLICY "exams_select_all" ON exams FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "exams_insert_admin" ON exams;
CREATE POLICY "exams_insert_admin" ON exams FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "exams_update_admin" ON exams;
CREATE POLICY "exams_update_admin" ON exams FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "exams_delete_admin" ON exams;
CREATE POLICY "exams_delete_admin" ON exams FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- HALLTICKETS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "halltickets_select_all" ON halltickets;
CREATE POLICY "halltickets_select_all" ON halltickets FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "halltickets_insert_admin" ON halltickets;
CREATE POLICY "halltickets_insert_admin" ON halltickets FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "halltickets_update_admin" ON halltickets;
CREATE POLICY "halltickets_update_admin" ON halltickets FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "halltickets_delete_admin" ON halltickets;
CREATE POLICY "halltickets_delete_admin" ON halltickets FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- PAYMENTS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "payments_select_all" ON payments;
CREATE POLICY "payments_select_all" ON payments FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "payments_insert_admin" ON payments;
CREATE POLICY "payments_insert_admin" ON payments FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "payments_update_admin" ON payments;
CREATE POLICY "payments_update_admin" ON payments FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "payments_delete_admin" ON payments;
CREATE POLICY "payments_delete_admin" ON payments FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- RECEIPTS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "receipts_select_all" ON receipts;
CREATE POLICY "receipts_select_all" ON receipts FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "receipts_insert_admin" ON receipts;
CREATE POLICY "receipts_insert_admin" ON receipts FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "receipts_update_admin" ON receipts;
CREATE POLICY "receipts_update_admin" ON receipts FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "receipts_delete_admin" ON receipts;
CREATE POLICY "receipts_delete_admin" ON receipts FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- NOTIFICATIONS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "notifications_select_all" ON notifications;
CREATE POLICY "notifications_select_all" ON notifications FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "notifications_insert_admin" ON notifications;
CREATE POLICY "notifications_insert_admin" ON notifications FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "notifications_update_admin" ON notifications;
CREATE POLICY "notifications_update_admin" ON notifications FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "notifications_delete_admin" ON notifications;
CREATE POLICY "notifications_delete_admin" ON notifications FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

-- ============================================================
-- BOOKS POLICIES (admin-only writes)
-- ============================================================
DROP POLICY IF EXISTS "books_select_all" ON books;
CREATE POLICY "books_select_all" ON books FOR SELECT
  TO authenticated USING (true);

DROP POLICY IF EXISTS "books_insert_admin" ON books;
CREATE POLICY "books_insert_admin" ON books FOR INSERT
  TO authenticated WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "books_update_admin" ON books;
CREATE POLICY "books_update_admin" ON books FOR UPDATE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  ) WITH CHECK (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );

DROP POLICY IF EXISTS "books_delete_admin" ON books;
CREATE POLICY "books_delete_admin" ON books FOR DELETE
  TO authenticated USING (
    EXISTS (SELECT 1 FROM admin a WHERE a.user_id = auth.uid())
  );
