import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# Drop existing tables to start fresh
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS scores")
cursor.execute("DROP TABLE IF EXISTS messages")
cursor.execute("DROP TABLE IF EXISTS doubts")
cursor.execute("DROP TABLE IF EXISTS assignments")
cursor.execute("DROP TABLE IF EXISTS student_teacher_assignments")

cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
role TEXT,
name TEXT,
subject TEXT
)
""")

cursor.execute("""
CREATE TABLE scores(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
score INTEGER,
subject TEXT,
game_name TEXT
)
""")

cursor.execute("""
CREATE TABLE messages(
id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_name TEXT,
target_student TEXT,
message TEXT,
date TEXT,
is_read INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE doubts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_name TEXT,
teacher_name TEXT,
question TEXT,
reply TEXT,
date TEXT,
reply_date TEXT,
is_read_by_student INTEGER DEFAULT 0,
is_read_by_teacher INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE student_teacher_assignments(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_name TEXT,
subject TEXT,
teacher_name TEXT
)
""")

# demo teachers
teachers = [
    ('T-01', 'T-01@123', 'teacher', 'Mr. Davis', 'Math'),
    ('T-02', 'T-02@123', 'teacher', 'Ms. Lee', 'Science'),
    ('T-03', 'T-03@123', 'teacher', 'Mrs. Smith', 'Technology'),
    ('T-04', 'T-04@123', 'teacher', 'Mr. Johnson', 'Engineering'),
    ('T-05', 'T-05@123', 'teacher', 'Ms. Williams', 'Math'),
    ('T-06', 'T-06@123', 'teacher', 'Mr. Brown', 'Science'),
    ('T-07', 'T-07@123', 'teacher', 'Mrs. Jones', 'Technology'),
    ('T-08', 'T-08@123', 'teacher', 'Mr. Garcia', 'Engineering'),
    ('T-09', 'T-09@123', 'teacher', 'Ms. Miller', 'Math'),
    ('T-10', 'T-10@123', 'teacher', 'Mr. Wilson', 'Science')
]
cursor.executemany("INSERT INTO users(username,password,role,name,subject) VALUES (?,?,?,?,?)", teachers)

# demo students
students = [
    ('G6-01', 'G6-01@123', 'student', 'Afna T A', None),
    ('G6-02', 'G6-02@123', 'student', 'Aleena Ann Francis', None),
    ('G6-03', 'G6-03@123', 'student', 'Anliya Dcunja', None),
    ('G7-01', 'G7-01@123', 'student', 'Almas N', None),
    ('G7-02', 'G7-02@123', 'student', 'Agnel Dsilva', None),
    ('G7-03', 'G7-03@123', 'student', 'Abhishek Nithin', None),
    ('G8-01', 'G8-01@123', 'student', 'Abhiram K', None),
    ('G8-02', 'G8-02@123', 'student', 'Jishnuraj P M', None),
    ('G8-03', 'G8-03@123', 'student', 'Alister Jibin', None),
    ('G8-04', 'G8-04@123', 'student', 'Alan Johnson', None),
    ('G9-01', 'G9-01@123', 'student', 'Kevin Hart', None),
    ('G9-02', 'G9-02@123', 'student', 'Laura Dern', None),
    ('G9-03', 'G9-03@123', 'student', 'Mike Ross', None),
    ('G9-04', 'G9-04@123', 'student', 'Nina Dobrev', None),
    ('G10-01', 'G10-01@123', 'student', 'Oscar Isaac', None),
    ('G10-02', 'G10-02@123', 'student', 'Peter Parker', None),
    ('G10-03', 'G10-03@123', 'student', 'Quinn Fabray', None),
    ('G10-04', 'G10-04@123', 'student', 'Rachel Green', None),
    ('G10-05', 'G10-05@123', 'student', 'Steve Rogers', None),
    ('G10-06', 'G10-06@123', 'student', 'Tony Stark', None)
]
cursor.executemany("INSERT INTO users(username,password,role,name,subject) VALUES (?,?,?,?,?)", students)

# demo scores (4 per student: Math, Science, Technology, Engineering)
import random
random.seed(42)  # For reproducible demo data
subjects = ['Math', 'Science', 'Technology', 'Engineering']
scores = []
for student in students:
    username = student[0]
    for subject in subjects:
        # Generate a random score between 100 and 1500
        score = random.randint(100, 1500)
        game_name = f"{username}_{subject}_Quiz"
        scores.append((username, score, subject, game_name))

cursor.executemany("INSERT INTO scores(username,score,subject,game_name) VALUES (?,?,?,?)", scores)

# demo student-teacher assignments
# Assign specific teachers to each grade cohort
assignments = []
for student in students:
    student_name = student[3] # name is at index 3
    username = student[0]
    grade = username.split('-')[0]
    
    # Simple assignment logic based on grade to ensure realistic data
    if grade in ['G6', 'G7']:
        assignments.append((student_name, 'Math', 'Mr. Davis'))
        assignments.append((student_name, 'Science', 'Ms. Lee'))
        assignments.append((student_name, 'Technology', 'Mrs. Smith'))
        assignments.append((student_name, 'Engineering', 'Mr. Johnson'))
    else:
        assignments.append((student_name, 'Math', 'Ms. Williams'))
        assignments.append((student_name, 'Science', 'Mr. Brown'))
        assignments.append((student_name, 'Technology', 'Mrs. Jones'))
        assignments.append((student_name, 'Engineering', 'Mr. Garcia'))

cursor.executemany("INSERT INTO student_teacher_assignments(student_name, subject, teacher_name) VALUES (?,?,?)", assignments)

# demo messages
messages = [
    ('Mr. Davis', 'ALL', 'Assignment 2 deadline: Friday', 'Mar 15, 2026, 09:30 AM', 0),
    ('Ms. Lee', 'ALL', 'Tomorrow we will have a science quiz', 'Mar 16, 2026, 02:15 PM', 0),
    ('Mrs. Smith', 'ALL', 'New technology module added', 'Mar 17, 2026, 11:00 AM', 0),
    ('Mr. Davis', 'Afna T A', 'Great job on the Math test!', 'Mar 18, 2026, 04:45 PM', 0)
]
cursor.executemany("INSERT INTO messages(teacher_name, target_student, message, date, is_read) VALUES (?,?,?,?,?)", messages)

# demo doubts
doubts = [
    ('Afna T A', 'Mr. Davis', "I didn't understand Newton's law. Can you explain?", None, 'Mar 18, 2026, 10:20 AM', None, 0, 0),
    ('Agnel Dsilva', 'Ms. Lee', "When is the next math quiz?", "It will be next Tuesday.", 'Mar 18, 2026, 11:30 AM', 'Mar 18, 2026, 01:15 PM', 0, 1),
    ('Almas N', 'Mrs. Smith', "Are we building robots next week?", None, 'Mar 19, 2026, 09:05 AM', None, 0, 0)
]
cursor.executemany("INSERT INTO doubts(student_name, teacher_name, question, reply, date, reply_date, is_read_by_student, is_read_by_teacher) VALUES (?,?,?,?,?,?,?,?)", doubts)

conn.commit()
conn.close()

print("Database recreated with realistic seed data")