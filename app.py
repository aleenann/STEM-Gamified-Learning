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
        unread_announcements = 0
        unread_private_msgs = 0
        unread_doubts = 0
        if role == "student":
            student_name = session.get("name")
            # Broadcast messages (Announcements)
            cursor.execute("SELECT COUNT(*) FROM messages WHERE is_read = 0 AND target_student = 'ALL'")
            unread_announcements = cursor.fetchone()[0]
            # Private messages
            cursor.execute("SELECT COUNT(*) FROM messages WHERE is_read = 0 AND target_student = ?", (student_name,))
            unread_private_msgs = cursor.fetchone()[0]
            # Doubts (Replies)
            cursor.execute("SELECT COUNT(*) FROM doubts WHERE is_read_by_student = 0 AND student_name = ? AND reply IS NOT NULL", (student_name,))
            unread_doubts = cursor.fetchone()[0]
        elif role == "teacher":
            teacher_name = session.get("name")
            cursor.execute("SELECT COUNT(*) FROM doubts WHERE is_read_by_teacher = 0 AND teacher_name = ?", (teacher_name,))
            unread_doubts = cursor.fetchone()[0]
        conn.close()
        return dict(
            unread_announcements=unread_announcements, 
            unread_private_msgs=unread_private_msgs, 
            unread_doubts=unread_doubts, 
            total_unread=(unread_announcements + unread_private_msgs + unread_doubts)
        )
    return dict(unread_announcements=0, unread_private_msgs=0, unread_doubts=0, total_unread=0)

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
    sub_subject = request.args.get("sub_subject")
    chapter = request.args.get("chapter")
    return render_template("student_dashboard.html", active_tab="learn", grade=grade, subject=subject, sub_subject=sub_subject, chapter=chapter)

@app.route("/student/play")
def student_play():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    subject = request.args.get("subject")
    sub_subject = request.args.get("sub_subject")
    chapter = request.args.get("chapter")
    username = session.get("username", "")
    grade = username.split('-')[0] if '-' in username else "Student"
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT game_name FROM scores WHERE username=?", (username,))
    completed_games = [row[0] for row in cursor.fetchall() if row[0]]
    conn.close()
    
    return render_template("student_dashboard.html", active_tab="play", subject=subject, sub_subject=sub_subject, chapter=chapter, grade=grade, completed_games=completed_games)

@app.route("/student/messages")
def student_messages():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch only broadcast messages for announcements
    cursor.execute("SELECT id, teacher_name, message, date, is_read FROM messages WHERE target_student = 'ALL' ORDER BY id DESC")
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
            
    # Fetch private messages (Specific to this student)
    cursor.execute("SELECT id, teacher_name, message, date, is_read FROM messages WHERE target_student = ? ORDER BY id DESC", (student_name,))
    private_messages = cursor.fetchall()

    cursor.execute("SELECT id, question, reply, teacher_name, date, reply_date, is_read_by_student FROM doubts WHERE student_name = ? ORDER BY id DESC", (student_name,))
    doubts = cursor.fetchall()
    conn.close()
    
    return render_template("student_dashboard.html", active_tab="doubts", doubts=doubts, private_messages=private_messages, teachers=teachers)

@app.route("/student/progress")
def student_progress():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    username = session.get("username")
    student_name = session.get("name")
    subject = request.args.get("subject")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Fetch teachers assigned to the student
    cursor.execute("SELECT subject, teacher_name FROM student_teacher_assignments WHERE student_name = ?", (student_name,))
    assigned_teachers = {row[0]: row[1] for row in cursor.fetchall()}
    
    chapter_progress = []
    if subject:
        if subject == "Maths":
            cursor.execute("""
                SELECT game_name, score 
                FROM scores 
                WHERE username = ? AND subject = ? AND game_name LIKE 'G6_Maths_Ch1%'
            """, (username, subject))
            ch1_scores = cursor.fetchall()
            
            completed_topics = 0
            total_xp = 0
            for row in ch1_scores:
                game_name = row[0]
                xp = row[1]
                total_xp += xp
                if game_name == 'G6_Maths_Ch1':
                    completed_topics += 1
                elif game_name == 'G6_Maths_Ch1_L2':
                    completed_topics += 1
                elif game_name == 'G6_Maths_Ch1_L3':
                    completed_topics += 2
            
            chapter_progress.append({
                "chapter_num": 1,
                "chapter_name": "Knowing Our Numbers",
                "completed": completed_topics,
                "total": 4, # 4 topics across 3 levels
                "xp": total_xp
            })
            
        elif subject == "Science":
            # Fetch ALL Science scores to handle Bio, Chem, Physics
            cursor.execute("""
                SELECT game_name, score 
                FROM scores 
                WHERE username = ? AND subject = ?
            """, (username, subject))
            all_sci_scores = cursor.fetchall()
            
            # Categorize scores
            bio_scores = []
            chem_scores = []
            
            for row in all_sci_scores:
                game_name = row[0]
                xp = row[1]
                if game_name.startswith("G6_Bio_Ch1"):
                    bio_scores.append(xp)
                elif game_name.startswith("G6_Chem_Ch1"):
                    chem_scores.append(xp)
            
            # Prepare chapters for display
            sci_chapters = [
                {"name": "Mindful Eating", "scores": bio_scores, "total": 2, "num": 1},
                {"name": "Matter and Its States", "scores": chem_scores, "total": 1, "num": 1}
            ]
            
            for chap in sci_chapters:
                scores_list = chap["scores"]
                # Explicit check to satisfy linter type inference
                if isinstance(scores_list, list):
                    completed = len(scores_list)
                    total_xp = sum(scores_list)
                    chapter_progress.append({
                        "chapter_num": chap["num"],
                        "chapter_name": chap["name"],
                        "completed": completed,
                        "total": chap["total"],
                        "xp": total_xp
                    })
            
    conn.close()
    
    return render_template("student_dashboard.html", active_tab="progress", subject=subject, chapter_progress=chapter_progress, assigned_teachers=assigned_teachers)

# Student Leaderboard
@app.route("/leaderboard")
def leaderboard():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    username = session.get("username", "")
    grade = username.split('-')[0] if '-' in username else "Student"
    grade_prefix = grade + "-%"
    
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
    
    # Subject-wise Leaderboards
    cursor.execute("""
        SELECT s.subject, u.name, SUM(s.score) as subject_score
        FROM users u
        JOIN scores s ON u.username = s.username
        WHERE u.role = 'student' AND u.username LIKE ?
        GROUP BY s.subject, u.id, u.name
        ORDER BY 
            CASE s.subject
                WHEN 'Science' THEN 1
                WHEN 'Technology' THEN 2
                WHEN 'Engineering' THEN 3
                WHEN 'Maths' THEN 4
                ELSE 5
            END,
            subject_score DESC
    """, (grade_prefix,))
    raw_subject_scores = cursor.fetchall()
    
    conn.close()
    
    subject_leaderboards = {}
    for row in raw_subject_scores:
        subj = row[0]
        name = row[1]
        score = row[2]
        if subj not in subject_leaderboards:
            subject_leaderboards[subj] = []
        subject_leaderboards[subj].append((name, score))
    
    return render_template("leaderboard.html", leaderboard=leaderboard_data, subject_leaderboards=subject_leaderboards, grade=grade)

# Teacher dashboard
@app.route("/teacher")
def teacher():
    if "name" not in session or session.get("role") != "teacher":
        return redirect("/")
        
    subject = session.get("subject", "Stem")
    grade = request.args.get("grade")
    active_tab = request.args.get("active_tab", "analytics")
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Always get distinct grades for navigation/selection
    cursor.execute("SELECT DISTINCT SUBSTR(username, 1, INSTR(username, '-') - 1) FROM users WHERE role = 'student'")
    grades = [row[0] for row in cursor.fetchall() if row[0]]
    # Sort grades numerically
    grades.sort(key=lambda g: int(g[1:]) if len(g) > 1 and g[1:].isdigit() else 0)
    
    # Get unread doubts count for navbar badge
    cursor.execute("SELECT COUNT(*) FROM doubts WHERE teacher_name = ? AND is_read_by_teacher = 0", (session.get("name"),))
    unread_doubts = cursor.fetchone()[0]
    
    if not grade:
        conn.close()
        return render_template("teacher_dashboard.html", grades=grades, selected_grade=None, active_tab=active_tab, unread_doubts=unread_doubts)
    
    # If grade is selected
    grade_prefix = f"{grade}-%"
    
    # Get students and their scores for the teacher's subject in this grade
    # Order by name ASC as requested
    cursor.execute("""
        SELECT u.id, u.name, u.username
        FROM users u
        WHERE u.role = 'student' AND u.username LIKE ?
        ORDER BY u.name ASC
    """, (grade_prefix,))
    
    students_list = cursor.fetchall()
    students_data = []
    total_chapters_set = set()
    
    for row in students_list:
        uid, name, uname = row
        cursor.execute("SELECT game_name, score FROM scores WHERE username = ? AND subject = ?", (uname, subject))
        scores = cursor.fetchall()
        
        total_xp = sum(s[1] for s in scores)
        # Extract chapters from game names (e.g. G6_Maths_Ch1 -> Ch1)
        student_chapters = set()
        for s in scores:
            gn = s[0]
            if "_Ch" in gn:
                parts = gn.split("_")
                for p in parts:
                    if p.startswith("Ch"):
                        student_chapters.add(p)
                        total_chapters_set.add(f"{grade}_{subject}_{p}")
        
        students_data.append((name, total_xp, len(student_chapters)))

    # Calculate stats
    active_students = len(students_data)
    avg_score = 0
    total_modules = len(total_chapters_set)
    if active_students > 0:
        avg_score = sum(student[1] for student in students_data) // active_students

    # Teacher Leaderboard (using same logic as student leaderboard)
    # Teacher Leaderboard - Filtered by teacher's specific subject
    grade_prefix = grade + "-%"
    cursor.execute("""
        SELECT u.name, COALESCE(SUM(s.score), 0) as subject_score
        FROM users u
        LEFT JOIN scores s ON u.username = s.username AND s.subject = ?
        WHERE u.role = 'student' AND u.username LIKE ?
        GROUP BY u.id, u.name
        ORDER BY subject_score DESC
    """, (subject, grade_prefix))
    leaderboard_data = cursor.fetchall()
    
    conn.close()
        
    return render_template("teacher_dashboard.html", 
                         active_tab=active_tab, 
                         students=students_data, 
                         active_students=active_students, 
                         avg_score=avg_score, 
                         total_modules=total_modules, 
                         selected_grade=grade, 
                         selected_subject=subject,
                         leaderboard=leaderboard_data,
                         grades=grades,
                         unread_doubts=unread_doubts)

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
    
    # Get unread doubts count for navbar badge
    cursor.execute("SELECT COUNT(*) FROM doubts WHERE teacher_name = ? AND is_read_by_teacher = 0", (teacher_name,))
    unread_doubts = cursor.fetchone()[0]

    # Get grades for navigation
    cursor.execute("SELECT DISTINCT SUBSTR(username, 1, INSTR(username, '-') - 1) FROM users WHERE role = 'student'")
    grades = [row[0] for row in cursor.fetchall() if row[0]]
    grades.sort(key=lambda g: int(g[1:]) if len(g) > 1 and g[1:].isdigit() else 0)
    
    conn.close()
    
    return render_template("teacher_dashboard.html", active_tab="messages", announcements=announcements, doubts=doubts, assigned_students=assigned_students, unread_doubts=unread_doubts, grades=grades)

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

# Grade 6 Maths Game 2 Route (Rounding Catcher)
@app.route("/student/play/maths/g6/ch1_l2")
def play_g6_maths_ch1_l2():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    username = session.get("username", "")
    # Check progression lock
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM scores WHERE username=? AND game_name='G6_Maths_Ch1'", (username,))
    if not cursor.fetchone():
        conn.close()
        return redirect("/student/play?subject=Maths")
    conn.close()
    
    return render_template("g6_maths_ch1_l2.html")

# Grade 6 Maths Game 3 Route (Elevator Escape)
@app.route("/student/play/maths/g6/ch1_l3")
def play_g6_maths_ch1_l3():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
        
    username = session.get("username", "")
    # Check progression lock
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM scores WHERE username=? AND game_name='G6_Maths_Ch1_L2'", (username,))
    if not cursor.fetchone():
        conn.close()
        return redirect("/student/play?subject=Maths")
    conn.close()
    
    return render_template("g6_maths_ch1_l3.html")

# Grade 7 Maths Game 1 Route (Number Line Ninja)
@app.route("/student/play/maths/g7/ch1_l1")
def play_g7_maths_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_maths_ch1_l1.html")

@app.route("/student/play/maths/g7/ch2_l1")
def play_g7_maths_ch2_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_maths_ch2_l1.html")

@app.route("/student/play/chem/g7/ch1_l1")
def play_g7_chem_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_chem_ch1_l1.html")

@app.route("/student/play/phys/g7/ch1_l1")
def play_g7_phys_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_phys_ch1_l1.html")

@app.route("/student/play/phys/g7/ch1_l2")
def play_g7_phys_ch1_l2():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_phys_ch1_l2.html")

@app.route("/student/play/phys/g7/ch1_l3")
def play_g7_phys_ch1_l3():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_phys_ch1_l3.html")

@app.route("/student/play/phys/g7/ch1_l4")
def play_g7_phys_ch1_l4():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_phys_ch1_l4.html")

@app.route("/student/play/phys/g9/ch9_l1")
def play_g9_phys_ch9_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g9_phys_ch9_l1.html")

@app.route("/student/play/phys/g9/ch9_l2")
def play_g9_phys_ch9_l2():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g9_phys_ch9_l2.html")

@app.route("/student/play/phys/g9/ch9_l3")
def play_g9_phys_ch9_l3():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g9_phys_ch9_l3.html")


@app.route("/student/play/bio/g9/ch5_l1")
def play_g9_bio_ch5_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g9_bio_ch5_l1.html")


@app.route("/student/play/tech/g7/ch1_l1")
def play_g7_tech_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_tech_ch1_l1.html")

@app.route("/student/play/bio/g7/ch1_l1")
def play_g7_bio_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_bio_ch1_l1.html")

@app.route("/student/play/bio/g7/ch2_l1")
def play_g7_bio_ch2_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_bio_ch2_l1.html")

@app.route("/student/play/eng/g7/ch1_l1")
def play_g7_eng_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g7_eng_ch1_l1.html")

# Grade 6 Biology Game 1 Route (Nutrient Sort)
@app.route("/student/play/bio/g6/ch1_l1")
def play_g6_bio_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g6_bio_ch1_l1.html")

# Grade 6 Chemistry Game 1 Route (Elements Explorer)
@app.route("/student/play/chem/g6/ch1_l1")
def play_g6_chem_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g6_chem_ch1_l1.html")

# Grade 6 Biology Game 2 Route (Vitamin Diagnosis)
@app.route("/student/play/bio/g6/ch1_l2")
def play_g6_bio_ch1_l2():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    
    return render_template("g6_bio_ch1_l2.html")
    
# Grade 6 Engineering Game 1 Route (Circuit Fixer)
@app.route("/student/play/eng/g6/ch1_l1")
def play_g6_eng_ch1_l1():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("g6_eng_ch1_l1.html")


# Save game score
@app.route("/save_score", methods=["POST"])
def save_score():
    username = request.form["username"]
    score = request.form["score"]
    subject = request.form.get("subject", "Maths")
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


# ─── CHEMISTRY GAME ──────────────────────────────────

@app.route("/student/games/chemistry")
def chemistry_game():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("chemistry_game.html")

@app.route("/student/play/chemistry/g8")
def chemistry_game_g8():
    if "name" not in session or session.get("role") != "student":
        return redirect("/")
    return render_template("chemistry_game.html")

@app.route("/student/games/save_score", methods=["POST"])
def save_game_score():
    # Only logged-in students can save scores
    if "name" not in session or session.get("role") != "student":
        return {"error": "unauthorized"}, 401

    data     = request.get_json()
    username = session.get("username")
    score    = int(data.get("xp", 0))          # XP earned in the game
    subject  = data.get("subject", "Science")   # always "Science" for chemistry game
    game_name = data.get("game_name", "Chemistry_Game")

    conn   = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check if this user already has a score for this specific game to prevent farming
    cursor.execute("SELECT id FROM scores WHERE username=? AND game_name=?", (username, game_name))
    existing = cursor.fetchone()

    if not existing:
        cursor.execute(
            "INSERT INTO scores(username, score, subject, game_name) VALUES (?, ?, ?, ?)",
            (username, score, subject, game_name)
        )
        conn.commit()

    conn.close()

    return {"success": True, "saved": score if not existing else 0}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)