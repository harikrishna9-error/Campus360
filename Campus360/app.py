from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "campus360_secret_key"


# ==============================
# DATABASE CONNECTION
# ==============================

def get_connection():

    conn = sqlite3.connect("portal.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# HOME
# ==============================

@app.route("/")
def home():

    return render_template("login.html")


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["POST"])
def login():

    usertype = request.form["usertype"]
    username = request.form["username"]
    password = request.form["password"]

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- STUDENT ----------------

    if usertype == "student":

        cursor.execute("""

        SELECT *

        FROM students

        WHERE rollno=?

        AND password=?

        """,

        (

        username,
        password

        ))

        student = cursor.fetchone()

        conn.close()

        if student:

            session.clear()

            session["student"] = student["rollno"]
            session["student_name"] = student["name"]

            return redirect("/student_dashboard")

        flash("Invalid Student Login")
        return redirect("/")


    # ---------------- FACULTY ----------------

    elif usertype == "faculty":

        cursor.execute("""

        SELECT *

        FROM faculty

        WHERE facultyid=?

        AND password=?

        """,

        (

        username,
        password

        ))

        faculty = cursor.fetchone()

        conn.close()

        if faculty:

            session.clear()

            session["faculty"] = faculty["facultyid"]
            session["faculty_name"] = faculty["name"]

            return redirect("/faculty_dashboard")

        flash("Invalid Faculty Login")
        return redirect("/")


    # ---------------- ADMIN ----------------

    elif usertype == "admin":

        cursor.execute("""

        SELECT *

        FROM admin

        WHERE username=?

        AND password=?

        """,

        (

        username,
        password

        ))

        admin = cursor.fetchone()

        conn.close()

        if admin:

            session.clear()

            session["admin"] = admin["username"]

            return redirect("/admin_dashboard")

        flash("Invalid Admin Login")
        return redirect("/")

    conn.close()

    return redirect("/")

# ==============================
# REGISTER
# ==============================

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method=="POST":

        try:

            conn=get_connection()
            cursor=conn.cursor()

            cursor.execute("""
            INSERT INTO students
            (
            rollno,
            password,
            name,
            branch,
            year,
            section,
            phone,
            email
            )

            VALUES
            (?,?,?,?,?,?,?,?)
            """,
            (
            request.form["rollno"],
            request.form["password"],
            request.form["name"],
            request.form["branch"],
            request.form["year"],
            request.form["section"],
            request.form["phone"],
            request.form["email"]
            ))

            conn.commit()
            conn.close()

            flash("✅ Registration Successful! Please Login.")

            return redirect("/")

        except:

            flash("❌ Roll Number already exists.")

            return redirect("/register")

    return render_template("register.html")

# ==============================
# LOGOUT
# ==============================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==============================
# STUDENT DASHBOARD
# ==============================

@app.route("/student_dashboard")
def student_dashboard():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    rollno = session["student"]

    # ---------------- Student Details ----------------

    cursor.execute(
        "SELECT * FROM students WHERE rollno=?",
        (rollno,)
    )

    student = cursor.fetchone()

    # ---------------- Attendance ----------------

    cursor.execute("""

    SELECT *

    FROM attendance

    WHERE rollno=?

    """,(rollno,))

    attendance_rows = cursor.fetchall()

    total_periods = 0
    present_periods = 0

    for row in attendance_rows:

        for p in range(1,7):

            total_periods += 1

            if row[f"P{p}"] == "Present":

                present_periods += 1

    if total_periods:

        attendance_percentage = round(

            (present_periods/total_periods)*100,

            2

        )

    else:

        attendance_percentage = 0

    attendance = {

        "total_periods": total_periods,

        "present_periods": present_periods,

        "percentage": attendance_percentage

    }

    # ---------------- Marks ----------------

    cursor.execute("""

    SELECT

    COUNT(*) AS exams,

    IFNULL(AVG(percentage),0) AS average

    FROM marks

    WHERE rollno=?

    """,(rollno,))

    marks = cursor.fetchone()

    # ---------------- Fees ----------------

    cursor.execute("""

    SELECT

    balance,

    status

    FROM fees

    WHERE rollno=?

    """,(rollno,))

    fee = cursor.fetchone()

    # ---------------- Notifications ----------------

    cursor.execute("""

    SELECT COUNT(*)

    FROM notifications

    """)

    notifications = cursor.fetchone()[0]

    conn.close()

    return render_template(

        "student_dashboard.html",

        student=student,

        attendance=attendance,

        marks=marks,

        fee=fee,

        notifications=notifications

    )

# ==============================
# STUDENT PROFILE
# ==============================

@app.route("/profile")
def profile():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE rollno=?",
        (session["student"],)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "profile.html",
        student=student
    )


# ==============================
# ATTENDANCE
# ==============================

@app.route("/attendance", methods=["GET"])
def attendance():

    # ----------------------------------------
    # Login Check
    # ----------------------------------------

    if ("admin" not in session and
        "faculty" not in session and
        "student" not in session):

        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    # ==================================================
    # STUDENT
    # ==================================================

    if "student" in session:

        rollno = session["student"]

        date = request.args.get("date", "")

        cursor.execute("""
            SELECT *
            FROM students
            WHERE rollno=?
        """, (rollno,))

        student = cursor.fetchone()

        cursor.execute("""
            SELECT
                date,

                MAX(CASE WHEN period=1 THEN status END) AS P1,
                MAX(CASE WHEN period=2 THEN status END) AS P2,
                MAX(CASE WHEN period=3 THEN status END) AS P3,
                MAX(CASE WHEN period=4 THEN status END) AS P4,
                MAX(CASE WHEN period=5 THEN status END) AS P5,
                MAX(CASE WHEN period=6 THEN status END) AS P6

            FROM attendance

            WHERE rollno=?
        """, (rollno,))

        if date:

            cursor.execute("""
                SELECT
                    date,

                    MAX(CASE WHEN period=1 THEN status END) AS P1,
                    MAX(CASE WHEN period=2 THEN status END) AS P2,
                    MAX(CASE WHEN period=3 THEN status END) AS P3,
                    MAX(CASE WHEN period=4 THEN status END) AS P4,
                    MAX(CASE WHEN period=5 THEN status END) AS P5,
                    MAX(CASE WHEN period=6 THEN status END) AS P6

                FROM attendance

                WHERE
                rollno=?
                AND date=?

                GROUP BY date

                ORDER BY date DESC
            """, (rollno, date))

        else:

            cursor.execute("""
                SELECT
                    date,

                    MAX(CASE WHEN period=1 THEN status END) AS P1,
                    MAX(CASE WHEN period=2 THEN status END) AS P2,
                    MAX(CASE WHEN period=3 THEN status END) AS P3,
                    MAX(CASE WHEN period=4 THEN status END) AS P4,
                    MAX(CASE WHEN period=5 THEN status END) AS P5,
                    MAX(CASE WHEN period=6 THEN status END) AS P6

                FROM attendance

                WHERE rollno=?

                GROUP BY date

                ORDER BY date DESC
            """, (rollno,))

        attendance = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE rollno=?
        """, (rollno,))

        total_periods = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE
            rollno=?
            AND status='Present'
        """, (rollno,))

        present_periods = cursor.fetchone()[0]

        percentage = 0

        if total_periods > 0:

            percentage = round(
                present_periods * 100 / total_periods,
                2
            )

        conn.close()

        return render_template(

            "attendance.html",

            role="student",

            student=student,

            attendance=attendance,

            date=date,

            percentage=percentage,

            total_periods=total_periods,

            present_periods=present_periods

        )

    # ==================================================
    # ADMIN / FACULTY
    # ==================================================

    branch = request.args.get("branch", "")
    year = request.args.get("year", "")
    date = request.args.get("date", "")

    students = []
    stats = None
    if branch and year and date:

        # -------------------------
        # Statistics
        # -------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM students
            WHERE branch=? AND year=?
        """, (branch, year))

        total_students = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE
            branch=?
            AND year=?
            AND date=?
        """, (branch, year, date))

        total_attendance = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE
            branch=?
            AND year=?
            AND date=?
            AND status='Present'
        """, (branch, year, date))

        present = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance
            WHERE
            branch=?
            AND year=?
            AND date=?
            AND status='Absent'
        """, (branch, year, date))

        period_absent = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM students
            WHERE
            branch=?
            AND year=?
            AND rollno NOT IN
            (
                SELECT DISTINCT rollno
                FROM attendance
                WHERE
                branch=?
                AND year=?
                AND date=?
                AND status='Present'
            )
        """, (
            branch,
            year,
            branch,
            year,
            date
        ))

        fullday_absent = cursor.fetchone()[0]
        full_day_present = present // 6

        stats = {

            "total_students": total_students,

            "total_periods": total_students * 6,

            "full_day_present": full_day_present,

            "period_absent": period_absent,

            "absent_students": fullday_absent

        }

        # -------------------------
        # Student Attendance Table
        # -------------------------

        cursor.execute("""

            SELECT

            s.rollno,
            s.name,

            MAX(CASE WHEN a.period=1 THEN a.status END) AS P1,
            MAX(CASE WHEN a.period=2 THEN a.status END) AS P2,
            MAX(CASE WHEN a.period=3 THEN a.status END) AS P3,
            MAX(CASE WHEN a.period=4 THEN a.status END) AS P4,
            MAX(CASE WHEN a.period=5 THEN a.status END) AS P5,
            MAX(CASE WHEN a.period=6 THEN a.status END) AS P6

            FROM students s

            LEFT JOIN attendance a

            ON s.rollno = a.rollno
            AND a.date=?

            WHERE

            s.branch=?
            AND s.year=?

            GROUP BY

            s.rollno,
            s.name

            ORDER BY s.rollno

        """, (

            date,
            branch,
            year

        ))

        students = cursor.fetchall()

    conn.close()

    return render_template(

        "attendance.html",

        role="staff",

        students=students,

        stats=stats,

        branch=branch,

        year=year,

        date=date

    )

@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():

    if "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # SAVE ATTENDANCE
    # -----------------------------
    if request.method == "POST" and request.form.get("action") == "save":

        branch = request.form["branch"]
        year = request.form["year"]
        date = request.form["date"]

        cursor.execute("""
        DELETE FROM attendance
        WHERE branch=? AND year=? AND date=?
        """,(branch,year,date))

        rollnos = request.form.getlist("rollno")

        for i,rollno in enumerate(rollnos):

            for period in range(1,7):

                field=f"status_{i}_{period}"

                status="Present" if field in request.form else "Absent"

                cursor.execute("""
                INSERT INTO attendance
                (rollno,branch,year,date,period,status)
                VALUES(?,?,?,?,?,?)
                """,(rollno,branch,year,date,period,status))

        conn.commit()
        conn.close()

        flash("Attendance Saved Successfully","success")

        return redirect(
            f"/attendance?branch={branch}&year={year}&date={date}"
        )

    # -----------------------------
    # LOAD STUDENTS
    # -----------------------------

    branch=request.values.get("branch","")
    year=request.values.get("year","")
    date=request.values.get("date","")

    students=[]

    if branch and year and date:

        cursor.execute("""

        SELECT
        rollno,
        name

        FROM students

        WHERE
        branch=?
        AND year=?

        ORDER BY rollno

        """,(branch,year))

        students=cursor.fetchall()

    conn.close()

    return render_template(

        "mark_attendance.html",

        students=students,

        branch=branch,

        year=year,

        date=date

    )

@app.route("/view_attendance")
def view_attendance():

    if "faculty" not in session and "admin" not in session:
        return redirect("/")

    branch = request.args.get("branch")
    year = request.args.get("year")
    date = request.args.get("date")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

    s.rollno,
    s.name,

    MAX(CASE WHEN a.period=1 THEN a.status END) AS P1,
    MAX(CASE WHEN a.period=2 THEN a.status END) AS P2,
    MAX(CASE WHEN a.period=3 THEN a.status END) AS P3,
    MAX(CASE WHEN a.period=4 THEN a.status END) AS P4,
    MAX(CASE WHEN a.period=5 THEN a.status END) AS P5,
    MAX(CASE WHEN a.period=6 THEN a.status END) AS P6

    FROM students s

    LEFT JOIN attendance a

    ON s.rollno=a.rollno
    AND a.date=?

    WHERE

    s.branch=?
    AND s.year=?

    GROUP BY

    s.rollno,
    s.name

    ORDER BY s.rollno

    """,(

    date,
    branch,
    year

    ))

    students = cursor.fetchall()

    conn.close()

    return render_template(

        "view_attendance.html",

        students=students,

        branch=branch,

        year=year,

        date=date

    )

@app.route("/edit_attendance", methods=["GET", "POST"])
def edit_attendance():

    if "faculty" not in session and "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    branch = request.values.get("branch")
    year = request.values.get("year")
    date = request.values.get("date")

    if request.method == "POST":

        cursor.execute("""

        DELETE FROM attendance

        WHERE
        branch=?
        AND year=?
        AND date=?

        """,(branch,year,date))

        rollnos = request.form.getlist("rollno")

        for i,rollno in enumerate(rollnos):

            for period in range(1,7):

                field=f"status_{i}_{period}"

                status="Present" if field in request.form else "Absent"

                cursor.execute("""

                INSERT INTO attendance
                (

                rollno,
                branch,
                year,
                date,
                period,
                status

                )

                VALUES(?,?,?,?,?,?)

                """,(

                rollno,
                branch,
                year,
                date,
                period,
                status

                ))

        conn.commit()

        flash("Attendance Updated Successfully","success")

        conn.close()

        return redirect(
            f"/attendance?branch={branch}&year={year}&date={date}"

        )


    cursor.execute("""

    SELECT

    s.rollno,
    s.name,

    MAX(CASE WHEN a.period=1 THEN a.status END) AS P1,
    MAX(CASE WHEN a.period=2 THEN a.status END) AS P2,
    MAX(CASE WHEN a.period=3 THEN a.status END) AS P3,
    MAX(CASE WHEN a.period=4 THEN a.status END) AS P4,
    MAX(CASE WHEN a.period=5 THEN a.status END) AS P5,
    MAX(CASE WHEN a.period=6 THEN a.status END) AS P6

    FROM students s

    LEFT JOIN attendance a

    ON s.rollno=a.rollno
    AND a.date=?

    WHERE

    s.branch=?
    AND s.year=?

    GROUP BY

    s.rollno,
    s.name

    ORDER BY s.rollno

    """,(

    date,
    branch,
    year

    ))

    students = cursor.fetchall()

    conn.close()

    return render_template(

        "edit_attendance.html",

        students=students,

        branch=branch,

        year=year,

        date=date

    )

@app.route("/delete_attendance")
def delete_attendance():

    if "faculty" not in session and "admin" not in session:
        return redirect("/")

    branch = request.args.get("branch")
    year = request.args.get("year")
    date = request.args.get("date")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM attendance

    WHERE

    branch=?
    AND year=?
    AND date=?

    """,(

    branch,
    year,
    date

    ))

    conn.commit()

    conn.close()

    session["delete_success"] = "Attendance Deleted Successfully"

    return redirect(

       f"/attendance?branch={branch}&year={year}&date={date}"

    )

# ==============================
# MARKS
# ==============================

# =====================================
# MARKS
# =====================================

# =====================================================
# MARKS MODULE
# =====================================================

@app.route("/marks")
def marks():

    # ----------------------------------------
    # LOGIN CHECK
    # ----------------------------------------

    if ("admin" not in session and
        "faculty" not in session and
        "student" not in session):

        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # STUDENT
    # =====================================================

    if "student" in session:

        rollno = session["student"]

        cursor.execute("""

        SELECT *

        FROM marks

        WHERE rollno=?

        ORDER BY semester,exam

        """,(rollno,))

        marks = cursor.fetchall()

        conn.close()

        return render_template(

            "marks.html",

            role="student",

            marks=marks

        )

    # =====================================================
    # ADMIN / FACULTY
    # =====================================================

    branch = request.args.get("branch","")
    year = request.args.get("year","")
    semester = request.args.get("semester","")
    exam = request.args.get("exam","")

    students = []

    if branch and year and semester and exam:

        cursor.execute("""

        SELECT

        marks.*,
        students.name

        FROM marks

        JOIN students

        ON marks.rollno = students.rollno

        WHERE

        marks.branch=?
        AND marks.year=?
        AND marks.semester=?
        AND marks.exam=?

        ORDER BY marks.rollno

        """,(

            branch,
            year,
            semester,
            exam

        ))

        students = cursor.fetchall()

    conn.close()

    return render_template(

        "marks.html",

        role="staff",

        students=students,

        branch=branch,

        year=year,

        semester=semester,

        exam=exam

    )

# =====================================================
# MARK MARKS
# =====================================================

@app.route("/mark_marks", methods=["GET", "POST"])
def mark_marks():

    if "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    # -------------------------------------------------
    # POST
    # -------------------------------------------------

    if request.method == "POST":

        branch = request.form["branch"]
        year = request.form["year"]
        semester = request.form["semester"]
        exam = request.form["exam"]

        rollnos = request.form.getlist("rollno")

        for i, rollno in enumerate(rollnos):

            python = int(request.form.get(f"python_{i}", 0))
            java = int(request.form.get(f"java_{i}", 0))
            dbms = int(request.form.get(f"dbms_{i}", 0))
            os = int(request.form.get(f"os_{i}", 0))
            cn = int(request.form.get(f"cn_{i}", 0))

            total = python + java + dbms + os + cn
            percentage = round(total / 5, 2)

            if percentage >= 90:
                grade = "O"
            elif percentage >= 80:
                grade = "A+"
            elif percentage >= 70:
                grade = "A"
            elif percentage >= 60:
                grade = "B"
            elif percentage >= 50:
                grade = "C"
            elif percentage >= 40:
                grade = "D"
            else:
                grade = "F"

            if (
                python >= 40 and
                java >= 40 and
                dbms >= 40 and
                os >= 40 and
                cn >= 40
            ):
                result = "PASS"
            else:
                result = "FAIL"

            cursor.execute("""
            SELECT id
            FROM marks
            WHERE
            rollno=?
            AND semester=?
            AND exam=?
            """, (
                rollno,
                semester,
                exam
            ))

            exists = cursor.fetchone()

            if exists:

                cursor.execute("""

                UPDATE marks

                SET

                branch=?,
                year=?,
                python=?,
                java=?,
                dbms=?,
                os=?,
                cn=?,
                total=?,
                percentage=?,
                grade=?,
                result=?

                WHERE

                rollno=?
                AND semester=?
                AND exam=?

                """, (

                    branch,
                    year,

                    python,
                    java,
                    dbms,
                    os,
                    cn,

                    total,
                    percentage,
                    grade,
                    result,

                    rollno,
                    semester,
                    exam

                ))

            else:

                cursor.execute("""

                INSERT INTO marks(

                rollno,
                branch,
                year,
                semester,
                exam,

                python,
                java,
                dbms,
                os,
                cn,

                total,
                percentage,
                grade,
                result

                )

                VALUES(

                ?,?,?,?,?,
                ?,?,?,?,?,
                ?,?,?,?

                )

                """, (

                    rollno,
                    branch,
                    year,
                    semester,
                    exam,

                    python,
                    java,
                    dbms,
                    os,
                    cn,

                    total,
                    percentage,
                    grade,
                    result

                ))

        conn.commit()

        flash("Marks added successfully.", "success")

        conn.close()

        return redirect(url_for(
            "view_marks",
            branch=branch,
            year=year,
            semester=semester,
            exam=exam
        ))

    # -------------------------------------------------
    # GET
    # -------------------------------------------------

    branch = request.args.get("branch", "")
    year = request.args.get("year", "")
    semester = request.args.get("semester", "")
    exam = request.args.get("exam", "")

    students = []

    if branch and year:

        cursor.execute("""

        SELECT

        rollno,
        name

        FROM students

        WHERE

        branch=?
        AND year=?

        ORDER BY rollno

        """, (

            branch,
            year

        ))

        students = cursor.fetchall()

    conn.close()

    return render_template(

        "mark_marks.html",

        students=students,

        branch=branch,
        year=year,
        semester=semester,
        exam=exam

    )

# =====================================================
# VIEW MARKS
# =====================================================

@app.route("/view_marks")
def view_marks():

    if ("faculty" not in session and
        "admin" not in session):
        return redirect("/")

    branch = request.args.get("branch", "")
    year = request.args.get("year", "")
    semester = request.args.get("semester", "")
    exam = request.args.get("exam", "")

    conn = get_connection()
    cursor = conn.cursor()

    students = []

    if branch and year and semester and exam:

        cursor.execute("""

        SELECT

        marks.*,
        students.name

        FROM marks

        JOIN students

        ON marks.rollno=students.rollno

        WHERE

        marks.branch=?
        AND marks.year=?
        AND marks.semester=?
        AND marks.exam=?

        ORDER BY marks.rollno

        """,(

            branch,
            year,
            semester,
            exam

        ))

        students = cursor.fetchall()

    conn.close()

    return render_template(

        "view_marks.html",

        students=students,

        branch=branch,

        year=year,

        semester=semester,

        exam=exam

    )

# =====================================================
# EDIT MARKS
# =====================================================

@app.route("/edit_marks/<int:id>", methods=["GET", "POST"])
def edit_marks(id):

    if ("faculty" not in session and
        "admin" not in session):
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        python = int(request.form["python"])
        java = int(request.form["java"])
        dbms = int(request.form["dbms"])
        os = int(request.form["os"])
        cn = int(request.form["cn"])

        total = python + java + dbms + os + cn
        percentage = round(total / 5, 2)

        if percentage >= 90:
            grade = "O"
        elif percentage >= 80:
            grade = "A+"
        elif percentage >= 70:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"

        if (
            python >= 40 and
            java >= 40 and
            dbms >= 40 and
            os >= 40 and
            cn >= 40
        ):
            result = "PASS"
        else:
            result = "FAIL"

        cursor.execute("""

        UPDATE marks

        SET

        python=?,
        java=?,
        dbms=?,
        os=?,
        cn=?,
        total=?,
        percentage=?,
        grade=?,
        result=?

        WHERE id=?

        """,(

            python,
            java,
            dbms,
            os,
            cn,
            total,
            percentage,
            grade,
            result,
            id

        ))

        conn.commit()

        cursor.execute("""

        SELECT

        branch,
        year,
        semester,
        exam

        FROM marks

        WHERE id=?

        """,(id,))

        row = cursor.fetchone()

        conn.close()

        flash("Marks updated successfully.","success")

        return redirect(url_for(

            "view_marks",

            branch=row["branch"],
            year=row["year"],
            semester=row["semester"],
            exam=row["exam"]

        ))

    cursor.execute(

        "SELECT * FROM marks WHERE id=?",

        (id,)

    )

    marks = cursor.fetchone()

    conn.close()

    return render_template(

        "edit_marks.html",

        marks=marks

    )

# =====================================================
# DELETE MARKS
# =====================================================

@app.route("/delete_marks/<int:id>")
def delete_marks(id):

    if ("faculty" not in session and
        "admin" not in session):
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    # Get details before deleting
    cursor.execute("""

    SELECT

    branch,
    year,
    semester,
    exam

    FROM marks

    WHERE id=?

    """,(id,))

    row = cursor.fetchone()

    if row is None:

        conn.close()

        flash("Marks record not found.","danger")

        return redirect("/marks")

    # Delete record
    cursor.execute(

        "DELETE FROM marks WHERE id=?",

        (id,)

    )

    conn.commit()

    conn.close()

    flash("Marks deleted successfully.","success")

    return redirect(url_for(

        "view_marks",

        branch=row["branch"],
        year=row["year"],
        semester=row["semester"],
        exam=row["exam"]

    ))
    
# ==============================
# RESULTS
# ==============================

@app.route("/results")
def results():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM results WHERE rollno=?",
        (session["student"],)
    )

    results = cursor.fetchall()

    conn.close()

    return render_template(
        "results.html",
        results=results
    )


# ==============================
# BACKLOGS
# ==============================

@app.route("/backlogs")
def backlogs():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM backlogs WHERE rollno=?",
        (session["student"],)
    )

    backlogs = cursor.fetchall()

    conn.close()

    return render_template(
        "backlogs.html",
        backlogs=backlogs
    )


# ==============================
# HALL TICKET
# ==============================

@app.route("/hallticket")
def hallticket():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM halltickets WHERE rollno=?",
        (session["student"],)
    )

    hallticket = cursor.fetchone()

    conn.close()

    return render_template(
        "hallticket.html",
        hallticket=hallticket
    )


# ==============================
# CHANGE PASSWORD
# ==============================

@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    if "student" not in session:
        return redirect("/")

    if request.method == "POST":

        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM students WHERE rollno=?",
            (session["student"],)
        )

        student = cursor.fetchone()

        if student and student["password"] == old_password:

            cursor.execute(
                "UPDATE students SET password=? WHERE rollno=?",
                (new_password, session["student"])
            )

            conn.commit()

            flash("Password Changed Successfully")

        else:

            flash("Old Password Incorrect")

        conn.close()

        return redirect("/change_password")

    return render_template("change_password.html")

# ==============================
# FEES
# ==============================

@app.route("/fees")
def fees():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM fees WHERE rollno=?",
        (session["student"],)
    )

    fee = cursor.fetchone()

    conn.close()

    return render_template(
        "fees.html",
        fee=fee
    )


# ==============================
# LIBRARY
# ==============================

@app.route("/library")
def library():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM library WHERE rollno=?",
        (session["student"],)
    )

    books = cursor.fetchall()

    conn.close()

    return render_template(
        "library.html",
        books=books
    )


# ==============================
# BOOK SEARCH
# ==============================

@app.route("/book_search", methods=["GET","POST"])
def book_search():

    if "student" not in session:
        return redirect("/")

    books = []

    if request.method == "POST":

        keyword = "%" + request.form["book"] + "%"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM books WHERE book_name LIKE ?",
            (keyword,)
        )

        books = cursor.fetchall()

        conn.close()

    return render_template(
        "book_search.html",
        books=books
    )


# ==============================
# PAYMENTS
# ==============================

@app.route("/payments")
def payments():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM payments WHERE rollno=?",
        (session["student"],)
    )

    payments = cursor.fetchall()

    conn.close()

    return render_template(
        "payments.html",
        payments=payments
    )


# ==============================
# RECEIPTS
# ==============================

@app.route("/receipts")
def receipts():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM receipts WHERE rollno=?",
        (session["student"],)
    )

    receipts = cursor.fetchall()

    conn.close()

    return render_template(
        "receipts.html",
        receipts=receipts
    )


# ==============================
# TIMETABLE
# ==============================

@app.route("/timetable")
def timetable():

    if "student" not in session and "faculty" not in session and "admin" not in session:
        return redirect("/")

    return render_template("timetable.html")

@app.route("/view_timetable")
def view_timetable():

    if "student" not in session and "faculty" not in session and "admin" not in session:
        return redirect("/")

    if "student" in session:

        branch=session["student"]["branch"]
        year=session["student"]["year"]

    else:

        branch=request.args.get("branch")
        year=request.args.get("year")

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""

    SELECT *

    FROM timetable

    WHERE branch=? AND year=?

    ORDER BY id

    """,(branch,year))

    timetable=cursor.fetchall()

    conn.close()

    return render_template(

        "view_timetable.html",

        timetable=timetable,

        branch=branch,

        year=year

    )

@app.route("/delete_timetable")
def delete_timetable():

    if "admin" not in session:
        return redirect("/")

    branch = request.args.get("branch")
    year = request.args.get("year")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM timetable WHERE branch=? AND year=?",

        (branch, year)

    )

    conn.commit()
    conn.close()

    flash("Timetable Deleted Successfully!", "success")

    return redirect("/timetable")

@app.route("/create_timetable", methods=["GET","POST"])
def create_timetable():

    if "admin" not in session:
        return redirect("/")

    if request.method=="POST":

        branch=request.form["branch"]
        year=request.form["year"]

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""

        SELECT *

        FROM timetable

        WHERE branch=? AND year=?

        """,(branch,year))

        if cursor.fetchone():

            conn.close()

            flash("Timetable already exists!","danger")

            return redirect("/create_timetable")

        days=request.form.getlist("day")

        p1=request.form.getlist("period1")
        p2=request.form.getlist("period2")
        p3=request.form.getlist("period3")
        p4=request.form.getlist("period4")
        p5=request.form.getlist("period5")
        p6=request.form.getlist("period6")

        for i in range(6):

            cursor.execute("""

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

            """,(

            branch,
            year,
            days[i],
            p1[i],
            p2[i],
            p3[i],
            p4[i],
            p5[i],
            p6[i]

            ))

        conn.commit()

        conn.close()

        flash("Weekly Timetable Created Successfully!","success")

        return redirect("/timetable")

    return render_template("create_timetable.html")

@app.route("/edit_timetable", methods=["GET", "POST"])
def edit_timetable():

    if "admin" not in session:
        return redirect("/")

    branch = request.args.get("branch")
    year = request.args.get("year")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        ids = request.form.getlist("id")
        days = request.form.getlist("day")
        p1 = request.form.getlist("period1")
        p2 = request.form.getlist("period2")
        p3 = request.form.getlist("period3")
        p4 = request.form.getlist("period4")
        p5 = request.form.getlist("period5")
        p6 = request.form.getlist("period6")

        for i in range(len(ids)):

            cursor.execute("""

            UPDATE timetable

            SET

            day=?,
            period1=?,
            period2=?,
            period3=?,
            period4=?,
            period5=?,
            period6=?

            WHERE id=?

            """,

            (

            days[i],
            p1[i],
            p2[i],
            p3[i],
            p4[i],
            p5[i],
            p6[i],
            ids[i]

            ))

        conn.commit()

        conn.close()

        flash("Timetable Updated Successfully!", "success")

        return redirect(f"/view_timetable?branch={branch}&year={year}")

    cursor.execute("""

    SELECT *

    FROM timetable

    WHERE branch=? AND year=?

    ORDER BY id

    """,

    (

    branch,
    year

    ))

    timetable = cursor.fetchall()

    conn.close()

    return render_template(

    "edit_timetable.html",

    timetable=timetable,

    branch=branch,

    year=year

    )

# ==============================
# EXAM DETAILS
# ==============================

@app.route("/exam_details")
def exam_details():

    if "student" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM exams
        WHERE branch=? AND year=?
        """,
        (
            "CSE",
            "3"
        )
    )

    exams = cursor.fetchall()

    conn.close()

    return render_template(
        "exam_details.html",
        exams=exams
    )

# ==============================
# FACULTY DASHBOARD
# ==============================

@app.route("/faculty_dashboard")
def faculty_dashboard():

    if "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    attendance_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marks")
    marks_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notifications")
    notifications = cursor.fetchone()[0]

    conn.close()

    return render_template(

        "faculty_dashboard.html",

        total_students=total_students,

        attendance_count=attendance_count,

        marks_count=marks_count,

        notifications=notifications

    )


# ==============================
# FACULTY PROFILE
# ==============================

@app.route("/faculty_profile")
def faculty_profile():

    if "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM faculty WHERE facultyid=?",

        (session["faculty"],)

    )

    faculty = cursor.fetchone()

    conn.close()

    return render_template(

        "faculty_profile.html",

        faculty=faculty

    )


# ==============================
# VIEW STUDENTS
# ==============================

@app.route("/view_students")
def view_students():

    if "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM students ORDER BY rollno"

    )

    students = cursor.fetchall()

    conn.close()

    return render_template(

        "view_students.html",

        students=students

    )

@app.route("/view_student/<rollno>")
def view_student(rollno):

    # Allow both Admin and Faculty
    if "admin" not in session and "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE rollno=?",
        (rollno,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "view_student.html",
        student=student
    )

@app.route("/update_student/<rollno>", methods=["POST"])
def update_student(rollno):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    UPDATE students

    SET

    name=?,
    branch=?,
    year=?,
    section=?,
    phone=?,
    email=?

    WHERE rollno=?

    """,

    (

    request.form["name"],
    request.form["branch"],
    request.form["year"],
    request.form["section"],
    request.form["phone"],
    request.form["email"],
    rollno

    ))

    conn.commit()
    conn.close()

    return redirect("/view_students")

# ==============================
# SEARCH STUDENT
# ==============================

@app.route("/search_student", methods=["GET","POST"])
def search_student():

    if "faculty" not in session:
        return redirect("/")

    student = None

    if request.method == "POST":

        rollno = request.form["rollno"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(

            "SELECT * FROM students WHERE rollno=?",

            (rollno,)

        )

        student = cursor.fetchone()

        conn.close()

    return render_template(

        "search_student.html",

        student=student

    )


# ==============================
# ADMIN DASHBOARD
# ==============================

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM faculty")
    faculty = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books")
    books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notifications")
    notifications = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM marks")
    total_marks = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        students=students,
        faculty=faculty,
        books=books,
        notifications=notifications,
        total_marks=total_marks
    )


# ==============================
# VIEW STUDENTS
# ==============================

@app.route("/students")
def students():

    if "admin" not in session and "faculty" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    search = request.args.get("search")

    if search:

        cursor.execute("""

        SELECT *

        FROM students

        WHERE

        rollno LIKE ?

        OR name LIKE ?

        ORDER BY rollno

        """,

        (

        "%" + search + "%",
        "%" + search + "%"

        ))

    else:

        cursor.execute(

            "SELECT * FROM students ORDER BY rollno"

        )

    students = cursor.fetchall()

    conn.close()

    return render_template(

        "students.html",

        students=students

    )


# ==============================
# ADD STUDENT
# ==============================

@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        # Check if Roll Number already exists
        cursor.execute(
            "SELECT * FROM students WHERE rollno=?",
            (request.form["rollno"],)
        )

        student = cursor.fetchone()

        if student:

            conn.close()

            flash("Roll Number already exists!", "danger")

            return redirect("/add_student")

        # Insert New Student
        cursor.execute("""
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
        (?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            request.form["rollno"],
            request.form["password"],
            request.form["name"],
            request.form["branch"],
            request.form["year"],
            request.form["section"],
            request.form["phone"],
            request.form["email"],
            request.form["address"],
            request.form["dob"],
            request.form["bloodgroup"]
        ))

        conn.commit()
        conn.close()

        flash("Student Added Successfully!", "success")

        return redirect("/students")

    return render_template("add_student.html")

# ==============================
# EDIT STUDENT
# ==============================

@app.route("/edit_student/<rollno>", methods=["GET", "POST"])
def edit_student(rollno):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
        UPDATE students
        SET
            name=?,
            branch=?,
            year=?,
            section=?,
            phone=?,
            email=?,
            address=?,
            dob=?,
            bloodgroup=?
        WHERE rollno=?
        """,
        (
            request.form["name"],
            request.form["branch"],
            request.form["year"],
            request.form["section"],
            request.form["phone"],
            request.form["email"],
            request.form["address"],
            request.form["dob"],
            request.form["bloodgroup"],
            rollno
        ))

        conn.commit()
        conn.close()

        flash("Student Updated Successfully!", "success")

        return redirect(f"/view_student/{rollno}")

    cursor.execute(
        "SELECT * FROM students WHERE rollno=?",
        (rollno,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )


# ==============================
# DELETE STUDENT
# ==============================

@app.route("/delete_student/<rollno>")
def delete_student(rollno):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE rollno=?",
        (rollno,)
    )

    conn.commit()
    conn.close()

    flash("Student Deleted Successfully!", "success")

    return redirect("/students")


# ==============================
# SEARCH STUDENT
# ==============================

@app.route("/student_search", methods=["GET","POST"])
def student_search():

    if "admin" not in session:
        return redirect("/")

    students = []

    if request.method == "POST":

        keyword = "%" + request.form["search"] + "%"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM students

        WHERE

        rollno LIKE ?

        OR name LIKE ?

        """,

        (

        keyword,
        keyword

        ))

        students = cursor.fetchall()

        conn.close()

    return render_template(

        "student_search.html",

        students=students

    )

# ==============================
# FACULTY LIST
# ==============================

@app.route("/faculty")
def faculty():

    if "admin" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT *
        FROM faculty
        WHERE facultyid LIKE ?
        OR name LIKE ?
        OR department LIKE ?
        ORDER BY facultyid
        """,
        (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

    else:

        cursor.execute("""
        SELECT *
        FROM faculty
        ORDER BY facultyid
        """)

    faculty = cursor.fetchall()

    conn.close()

    return render_template(
        "faculty.html",
        faculty=faculty
    )

@app.route("/view_faculty/<facultyid>")
def view_faculty(facultyid):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM faculty WHERE facultyid=?",
        (facultyid,)
    )

    faculty = cursor.fetchone()

    conn.close()

    return render_template(
        "view_faculty.html",
        faculty=faculty
    )

@app.route("/update_faculty/<facultyid>", methods=["POST"])
def update_faculty(facultyid):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE faculty

        SET

        name=?,
        department=?,
        phone=?,
        email=?

        WHERE facultyid=?

    """,

    (

        request.form["name"],
        request.form["department"],
        request.form["phone"],
        request.form["email"],
        facultyid

    ))

    conn.commit()
    conn.close()

    return redirect("/faculty")

# ==============================
# ADD FACULTY
# ==============================

@app.route("/add_faculty", methods=["GET","POST"])
def add_faculty():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        # Check Duplicate Faculty ID
        cursor.execute(
            "SELECT * FROM faculty WHERE facultyid=?",
            (request.form["facultyid"],)
        )

        faculty = cursor.fetchone()

        if faculty:

            conn.close()

            flash("Faculty ID already exists!", "danger")

            return redirect("/add_faculty")

        # Insert Faculty
        cursor.execute("""

        INSERT INTO faculty
        (
            facultyid,
            password,
            name,
            department,
            phone,
            email
        )

        VALUES
        (?,?,?,?,?,?)

        """,
        (
            request.form["facultyid"],
            request.form["password"],
            request.form["name"],
            request.form["department"],
            request.form["phone"],
            request.form["email"]
        ))

        conn.commit()
        conn.close()

        flash("Faculty Added Successfully!", "success")

        return redirect("/faculty")

    return render_template("add_faculty.html")


# ==============================
# EDIT FACULTY
# ==============================

@app.route("/edit_faculty/<facultyid>", methods=["GET", "POST"])
def edit_faculty(facultyid):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
        UPDATE faculty
        SET
            name=?,
            department=?,
            phone=?,
            email=?
        WHERE facultyid=?
        """,
        (
            request.form["name"],
            request.form["department"],
            request.form["phone"],
            request.form["email"],
            facultyid
        ))

        conn.commit()
        conn.close()

        flash("Faculty Updated Successfully!", "success")

        return redirect(f"/view_faculty/{facultyid}")

    cursor.execute(
        "SELECT * FROM faculty WHERE facultyid=?",
        (facultyid,)
    )

    faculty = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_faculty.html",
        faculty=faculty
    )


# ==============================
# DELETE FACULTY
# ==============================

@app.route("/delete_faculty/<facultyid>")
def delete_faculty(facultyid):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM faculty WHERE facultyid=?",
        (facultyid,)
    )

    conn.commit()
    conn.close()

    flash("Faculty Deleted Successfully!", "success")

    return redirect("/faculty")


# ==============================
# BOOKS
# ==============================

@app.route("/books")
def books():

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books ORDER BY id DESC")

    books = cursor.fetchall()

    conn.close()

    return render_template(

        "books.html",

        books=books

    )


# ==============================
# ADD BOOK
# ==============================

@app.route("/add_book", methods=["GET", "POST"])
def add_book():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO books
        (
            book_name,
            author,
            quantity
        )

        VALUES
        (?,?,?)
        """,
        (
            request.form["book_name"],
            request.form["author"],
            request.form["quantity"]
        ))

        conn.commit()
        conn.close()

        flash("Book Added Successfully!", "success")

        return redirect("/books")

    return render_template("add_book.html")


# ==============================
# DELETE BOOK
# ==============================

@app.route("/delete_book/<int:id>")
def delete_book(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Book Deleted Successfully!", "success")

    return redirect("/books")

@app.route("/view_book/<int:id>")
def view_book(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    )

    book = cursor.fetchone()

    conn.close()

    return render_template(
        "view_book.html",
        book=book
    )

@app.route("/edit_book/<int:id>", methods=["GET", "POST"])
def edit_book(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
        UPDATE books
        SET
            book_name=?,
            author=?,
            quantity=?
        WHERE id=?
        """,
        (
            request.form["book_name"],
            request.form["author"],
            request.form["quantity"],
            id
        ))

        conn.commit()
        conn.close()

        flash("Book Updated Successfully!", "success")

        return redirect(f"/view_book/{id}")

    cursor.execute(
        "SELECT * FROM books WHERE id=?",
        (id,)
    )

    book = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_book.html",
        book=book
    )


# ==============================
# NOTIFICATIONS
# ==============================

@app.route("/notifications")
def notifications():

    if "student" not in session and "faculty" not in session and "admin" not in session:
       return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notifications ORDER BY id DESC"
    )

    notifications = cursor.fetchall()

    conn.close()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@app.route("/add_notification", methods=["GET", "POST"])
def add_notification():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO notifications
        (
            title,
            message,
            date
        )
        VALUES
        (?,?,?)
        """,
        (
            request.form["title"],
            request.form["message"],
            request.form["date"]
        ))

        conn.commit()
        conn.close()

        flash("Notification Added Successfully!", "success")

        return redirect("/notifications")

    return render_template("add_notification.html")


@app.route("/delete_notification/<int:id>")
def delete_notification(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notifications WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Notification Deleted Successfully!", "success")

    return redirect("/notifications")

@app.route("/view_notification/<int:id>")
def view_notification(id):

    if "student" not in session and "faculty" not in session and "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM notifications WHERE id=?",
        (id,)
    )

    notification = cursor.fetchone()

    conn.close()

    return render_template(
        "view_notification.html",
        notification=notification
    )

@app.route("/edit_notification/<int:id>", methods=["GET","POST"])
def edit_notification(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
        UPDATE notifications
        SET
            title=?,
            message=?,
            date=?
        WHERE id=?
        """,
        (
            request.form["title"],
            request.form["message"],
            request.form["date"],
            id
        ))

        conn.commit()
        conn.close()

        flash("Notification Updated Successfully!", "success")

        return redirect(f"/view_notification/{id}")

    cursor.execute(
        "SELECT * FROM notifications WHERE id=?",
        (id,)
    )

    notification = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_notification.html",
        notification=notification
    )

# ==============================
# EXAMS
# ==============================

@app.route("/admin_exams")
def admin_exams():

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM exams ORDER BY exam_date")

    exams = cursor.fetchall()

    conn.close()

    return render_template(
        "admin_exams.html",
        exams=exams
    )


@app.route("/add_exam", methods=["GET","POST"])
def add_exam():

    if "admin" not in session:
        return redirect("/")

    if request.method == "POST":

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO exams

        (

        exam_name,
        exam_date,
        branch,
        year

        )

        VALUES

        (?,?,?,?)

        """,

        (

        request.form["exam_name"],
        request.form["exam_date"],
        request.form["branch"],
        request.form["year"]

        ))

        conn.commit()
        conn.close()

        return redirect("/admin_exams")

    return render_template("add_exam.html")


@app.route("/delete_exam/<int:id>")
def delete_exam(id):

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM exams WHERE id=?",

        (id,)

    )

    conn.commit()
    conn.close()

    return redirect("/admin_exams")



# ==============================
# PAYMENT REPORT
# ==============================

@app.route("/payment_report")
def payment_report():

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM payments

    ORDER BY payment_date DESC

    """)

    payments = cursor.fetchall()

    conn.close()

    return render_template(
        "payment_report.html",
        payments=payments
    )


# ==============================
# RECEIPT REPORT
# ==============================

@app.route("/receipt_report")
def receipt_report():

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM receipts

    ORDER BY receipt_date DESC

    """)

    receipts = cursor.fetchall()

    conn.close()

    return render_template(
        "receipt_report.html",
        receipts=receipts
    )


# ==============================
# ADMIN STATISTICS
# ==============================

@app.route("/statistics")
def statistics():

    if "admin" not in session:
        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM faculty")
    total_faculty = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notifications")
    total_notifications = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM payments")
    total_payments = cursor.fetchone()[0]

    conn.close()

    return render_template(

        "statistics.html",

        total_students=total_students,
        total_faculty=total_faculty,
        total_books=total_books,
        total_notifications=total_notifications,
        total_payments=total_payments

    )

# ==============================
# SESSION CHECK HELPERS
# ==============================

def student_login_required():

    return "student" in session


def faculty_login_required():

    return "faculty" in session


def admin_login_required():

    return "admin" in session


# ==============================
# ABOUT
# ==============================

@app.route("/about")
def about():

    return render_template("about.html")


# ==============================
# CONTACT
# ==============================

@app.route("/contact")
def contact():

    return render_template("contact.html")


# ==============================
# HELP
# ==============================

@app.route("/help")
def help_page():

    return render_template("help.html")


# ==============================
# ERROR HANDLERS
# ==============================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"),404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template("500.html"),500


# ==============================
# CONTEXT PROCESSOR
# ==============================

@app.context_processor
def inject_user():

    return dict(

        student=session.get("student"),

        faculty=session.get("faculty"),

        admin=session.get("admin")

    )


# ==============================
# BEFORE REQUEST
# ==============================

@app.before_request
def before_request():

    pass


# ==============================
# AFTER REQUEST
# ==============================

@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-store"

    return response


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )