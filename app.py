from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_stem_key_123"

# Home page (Role Selector)
@app.route("/")
def home():
    return render_template("login.html")

# Student Login/Signup Page
@app.route("/login/student")
def student_login_page():
    return render_template("student_login.html")

# Teacher Login/Signup Page
@app.route("/login/teacher")
def teacher_login_page():
    return render_template("teacher_login.html")

# Process Login (handles both student and teacher via role form field)
@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    role = request.form.get("role", "student")

    if not username or not password:
        return render_template(f"{role}_login.html", error="Please enter both your username and password.")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", 
                   (username, password, role))

    user = cursor.fetchone()
    conn.close()

    if user:
        session["name"] = user[4]  # name is at index 4
        session["username"] = user[1] # username is index 1
        session["role"] = user[3] # role is index 3
        session["subject"] = user[5] # subject is index 5
        if role == "student":
            return redirect("/student")
        if role == "teacher":
            return redirect("/teacher")

    return render_template(f"{role}_login.html", error="Invalid username or password. Please try again.")

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.context_processor
def inject_unread_counts():
    if "name" in session:
        role = session.get("role")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        unread_msgs = 0
        unread_doubts = 0
        if role == "student":
            student_name = session.get("name")
            cursor.execute("SELECT COUNT(*) FROM messages WHERE is_read = 0 AND (target_student = 'ALL' OR target_student = ?)", (student_name,))
            unread_msgs = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM doubts WHERE is_read_by_student = 0 AND student_name = ? AND reply IS NOT NULL", (student_name,))
            unread_doubts = cursor.fetchone()[0]
        elif role == "teacher":
            teacher_name = session.get("name")
            cursor.execute("SELECT COUNT(*) FROM doubts WHERE is_read_by_teacher = 0 AND teacher_name = ?", (teacher_name,))
            unread_doubts = cursor.fetchone()[0]
        conn.close()
        return dict(unread_msgs=unread_msgs, unread_doubts=unread_doubts, total_unread=(unread_msgs + unread_doubts))
    return dict(unread_msgs=0, unread_doubts=0, total_unread=0)

@app.route("/mark_read/message/<int:msg_id>", methods=["POST"])
def mark_message_read(msg_id):
    if session.get("role") == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET is_read = 1 WHERE id = ?", (msg_id,))
        conn.commit()
        conn.close()
    return redirect("/student/messages")

@app.route("/mark_read/message/all", methods=["POST"])
def mark_all_messages_read():
    if session.get("role") == "student":
        student_name = session.get("name")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET is_read = 1 WHERE target_student = 'ALL' OR target_student = ?", (student_name,))
        conn.commit()
        conn.close()
    return redirect("/student/messages")

@app.route("/mark_read/doubt_student/<int:doubt_id>", methods=["POST"])
def mark_doubt_read_student(doubt_id):
    if session.get("role") == "student":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE doubts SET is_read_by_student = 1 WHERE id = ?", (doubt_id,))
        conn.commit()
        conn.close()
    return redirect("/student/doubts")

@app.route("/mark_read/doubt_teacher/<int:doubt_id>", methods=["POST"])
def mark_doubt_read_teacher(doubt_id):
    if session.get("role") == "teacher":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE doubts SET is_read_by_teacher = 1 WHERE id = ?", (doubt_id,))
        conn.commit()
        conn.close()
    return redirect("/teacher/messages")

@app.route("/mark_read/all_doubts_student", methods=["POST"])
def mark_all_doubts_student_read():
    if session.get("role") == "student":
        student_name = session.get("name")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE doubts SET is_read_by_student = 1 WHERE student_name = ? AND reply IS NOT NULL", (student_name,))
        conn.commit()
        conn.close()
    return redirect("/student/doubts")

@app.route("/mark_read/all_doubts_teacher", methods=["POST"])
def mark_all_doubts_teacher_read():
    if session.get("role") == "teacher":
        teacher_name = session.get("name")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE doubts SET is_read_by_teacher = 1 WHERE teacher_name = ?", (teacher_name,))
        conn.commit()
        conn.close()
    return redirect("/teacher/messages")

# Student Routes
@app.route("/student")
def student():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    username = session.get("username", "")
    grade = username.split('-')[0] if '-' in username else "Student"
    return render_template("student_dashboard.html", active_tab="dashboard", grade=grade)

@app.route("/student/learn")
def student_learn():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    username = session.get("username", "")
    grade = username.split('-')[0] if '-' in username else "Student"
    subject = request.args.get("subject")
    chapter = request.args.get("chapter")
    return render_template("student_dashboard.html", active_tab="learn", grade=grade, subject=subject, chapter=chapter)

@app.route("/student/play")
def student_play():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    subject = request.args.get("subject")
    sub_subject = request.args.get("sub_subject")
    username = session.get("username", "")
    grade = username.split('-')[0] if '-' in username else "Student"
    
    return render_template("student_dashboard.html", active_tab="play", subject=subject, sub_subject=sub_subject, grade=grade)

@app.route("/student/messages")
def student_messages():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch messages addressed to ALL or this specific student
    cursor.execute("SELECT id, teacher_name, message, date, is_read FROM messages WHERE target_student = 'ALL' OR target_student = ? ORDER BY id DESC", (session.get("name"),))
    messages = cursor.fetchall()
    conn.close()
    
    return render_template("student_dashboard.html", active_tab="messages", messages=messages)

@app.route("/student/doubts", methods=["GET", "POST"])
def student_doubts():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    student_name = session.get("name")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch teachers assigned to this student
    cursor.execute("SELECT teacher_name, subject FROM student_teacher_assignments WHERE student_name = ?", (student_name,))
    teachers = [(row[0], f"{row[0]} ({row[1]})") for row in cursor.fetchall()]
    
    if request.method == "POST":
        question = request.form.get("question")
        teacher_name = request.form.get("teacher_name")
        if question and teacher_name:
            current_date = datetime.now().strftime("%b %d, %Y, %I:%M %p")
            cursor.execute("INSERT INTO doubts (student_name, teacher_name, question, date) VALUES (?, ?, ?, ?)", (student_name, teacher_name, question, current_date))
            conn.commit()
            return redirect("/student/doubts")
            
    cursor.execute("SELECT id, question, reply, teacher_name, date, reply_date, is_read_by_student FROM doubts WHERE student_name = ? ORDER BY id DESC", (student_name,))
    doubts = cursor.fetchall()
    conn.close()
    
    return render_template("student_dashboard.html", active_tab="doubts", doubts=doubts, teachers=teachers)

@app.route("/student/progress")
def student_progress():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    username = session.get("username")
    student_name = session.get("name")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.subject, SUM(s.score) as total_score, MIN(a.teacher_name) as teacher_name 
        FROM scores s
        LEFT JOIN student_teacher_assignments a ON s.subject = a.subject AND a.student_name = ?
        WHERE s.username = ?
        GROUP BY s.subject
    """, (student_name, username))
    scores = cursor.fetchall()
    
    conn.close()
    
    return render_template("student_dashboard.html", active_tab="progress", scores=scores)

# Student Leaderboard
@app.route("/leaderboard")
def leaderboard():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    username = session.get("username", "")
    grade_prefix = username.split('-')[0] + "-%"
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT u.name, COALESCE(SUM(s.score), 0) as total_score
        FROM users u
        LEFT JOIN scores s ON u.username = s.username
        WHERE u.role = 'student' AND u.username LIKE ?
        GROUP BY u.id, u.name
        ORDER BY total_score DESC
    """, (grade_prefix,))
    
    leaderboard_data = cursor.fetchall()
    conn.close()
    
    return render_template("leaderboard.html", leaderboard=leaderboard_data)


# Teacher dashboard
@app.route("/teacher")
def teacher():
    if "name" not in session or session.get("role") != "teacher":
        return redirect("/")
        
    subject = session.get("subject", "Stem")
    grade = request.args.get("grade")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    if not grade:
        # Get distinct grades from usernames (e.g. G6, G7)
        cursor.execute("SELECT DISTINCT SUBSTR(username, 1, INSTR(username, '-') - 1) FROM users WHERE role = 'student'")
        grades = [row[0] for row in cursor.fetchall() if row[0]]
        # Sort grades numerically
        grades.sort(key=lambda g: int(g[1:]) if len(g) > 1 and g[1:].isdigit() else 0)
        
        conn.close()
        return render_template("teacher_dashboard.html", grades=grades, selected_grade=None)
    
    # If grade is selected
    grade_prefix = f"{grade}-%"
    
    # Get students and their scores for the teacher's subject in this grade
    cursor.execute("""
        SELECT u.name, COALESCE(SUM(s.score), 0) as score
        FROM users u
        LEFT JOIN scores s ON u.username = s.username AND s.subject = ?
        WHERE u.role = 'student' AND u.username LIKE ?
        GROUP BY u.id, u.name
        ORDER BY score DESC
    """, (subject, grade_prefix))
    
    students_data = cursor.fetchall()
    
    # Calculate stats
    active_students = len(students_data)
    avg_score = 0
    if active_students > 0:
        avg_score = sum(student[1] for student in students_data) // active_students
    conn.close()
        
    return render_template("teacher_dashboard.html", active_tab="analytics", students=students_data, active_students=active_students, avg_score=avg_score, selected_grade=grade, selected_subject=subject)

@app.route("/teacher/messages")
def teacher_messages():
    if "name" not in session or session.get("role") != "teacher":
        return redirect("/")
        
    teacher_name = session.get("name")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Get assigned students for the direct message dropdown
    cursor.execute("SELECT DISTINCT student_name FROM student_teacher_assignments WHERE teacher_name = ? ORDER BY student_name", (teacher_name,))
    assigned_students = [row[0] for row in cursor.fetchall()]
    
    # Get announcements/messages sent by this teacher
    cursor.execute("SELECT target_student, message, date FROM messages WHERE teacher_name = ? ORDER BY id DESC", (teacher_name,))
    announcements = cursor.fetchall()
    
    # Get all doubts aimed at this teacher
    cursor.execute("SELECT id, student_name, question, reply, is_read_by_teacher, date, reply_date FROM doubts WHERE teacher_name = ? ORDER BY id DESC", (teacher_name,))
    doubts = cursor.fetchall()
    
    conn.close()
    
    return render_template("teacher_dashboard.html", active_tab="messages", announcements=announcements, doubts=doubts, assigned_students=assigned_students)

@app.route("/teacher/send_message", methods=["POST"])
def teacher_send_message():
    if "name" not in session or session.get("role") != "teacher":
        return redirect("/")
        
    teacher_name = session.get("name")
    message = request.form["message"]
    
    current_date = datetime.now().strftime("%b %d, %Y, %I:%M %p")
    
    target_student = request.form.get("target_student", "ALL")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (teacher_name, target_student, message, date) VALUES (?, ?, ?, ?)", (teacher_name, target_student, message, current_date))
    conn.commit()
    conn.close()
    
    return redirect("/teacher/messages")

@app.route("/teacher/reply_doubt", methods=["POST"])
def teacher_reply_doubt():
    if "name" not in session or session.get("role") != "teacher":
        return redirect("/")
        
    doubt_id = request.form["doubt_id"]
    reply = request.form["reply"]
    
    current_date = datetime.now().strftime("%b %d, %Y, %I:%M %p")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE doubts SET reply = ?, reply_date = ? WHERE id = ?", (reply, current_date, doubt_id))
    conn.commit()
    conn.close()
    
    return redirect("/teacher/messages")


# Grade 6 Maths Game Route
@app.route("/student/play/maths/g6/ch1")
def play_g6_maths_ch1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g6_maths_ch1.html")

# Quiz / Game Page
@app.route("/quiz")
def quiz():
    return render_template("quiz_game.html")


# Save game score
@app.route("/save_score", methods=["POST"])
def save_score():
    username = request.form["username"]
    score = request.form["score"]
    subject = request.form.get("subject", "Math")
    game_name = request.form.get("game_name", "Demo_Quiz")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check if this user already has a score for this specific game
    cursor.execute("SELECT id FROM scores WHERE username=? AND game_name=?", (username, game_name))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute("INSERT INTO scores(username,score,subject,game_name) VALUES (?,?,?,?)",
                       (username,score,subject,game_name))
        conn.commit()

    conn.close()

    return "Score Processed"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)