import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# Drop existing tables to start fresh
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS scores")

cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
role TEXT,
name TEXT
)
""")

cursor.execute("""
CREATE TABLE scores(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
score INTEGER
)
""")

# demo teachers
teachers = [
    ('T-01', 'T-01@123', 'teacher', 'Mr. Davis'),
    ('T-02', 'T-02@123', 'teacher', 'Ms. Lee'),
    ('T-03', 'T-03@123', 'teacher', 'Mrs. Smith'),
    ('T-04', 'T-04@123', 'teacher', 'Mr. Johnson'),
    ('T-05', 'T-05@123', 'teacher', 'Ms. Williams'),
    ('T-06', 'T-06@123', 'teacher', 'Mr. Brown'),
    ('T-07', 'T-07@123', 'teacher', 'Mrs. Jones'),
    ('T-08', 'T-08@123', 'teacher', 'Mr. Garcia'),
    ('T-09', 'T-09@123', 'teacher', 'Ms. Miller'),
    ('T-10', 'T-10@123', 'teacher', 'Mr. Wilson')
]
cursor.executemany("INSERT INTO users(username,password,role,name) VALUES (?,?,?,?)", teachers)

# demo students
students = [
    ('G6-01', 'G6-01@123', 'student', 'Alice Johnson'),
    ('G6-02', 'G6-02@123', 'student', 'Bob Smith'),
    ('G6-03', 'G6-03@123', 'student', 'Charlie Davis'),
    ('G7-01', 'G7-01@123', 'student', 'Diana Prince'),
    ('G7-02', 'G7-02@123', 'student', 'Ethan Hunt'),
    ('G7-03', 'G7-03@123', 'student', 'Fiona Gallagher'),
    ('G8-01', 'G8-01@123', 'student', 'George Lucas'),
    ('G8-02', 'G8-02@123', 'student', 'Hannah Montana'),
    ('G8-03', 'G8-03@123', 'student', 'Ian Somerhalder'),
    ('G8-04', 'G8-04@123', 'student', 'Jack Sparrow'),
    ('G9-01', 'G9-01@123', 'student', 'Kevin Hart'),
    ('G9-02', 'G9-02@123', 'student', 'Laura Dern'),
    ('G9-03', 'G9-03@123', 'student', 'Mike Ross'),
    ('G9-04', 'G9-04@123', 'student', 'Nina Dobrev'),
    ('G10-01', 'G10-01@123', 'student', 'Oscar Isaac'),
    ('G10-02', 'G10-02@123', 'student', 'Peter Parker'),
    ('G10-03', 'G10-03@123', 'student', 'Quinn Fabray'),
    ('G10-04', 'G10-04@123', 'student', 'Rachel Green'),
    ('G10-05', 'G10-05@123', 'student', 'Steve Rogers'),
    ('G10-06', 'G10-06@123', 'student', 'Tony Stark')
]
cursor.executemany("INSERT INTO users(username,password,role,name) VALUES (?,?,?,?)", students)

# demo scores
scores = [
    ('G6-01', 850),
    ('G6-02', 720),
    ('G6-03', 910),
    ('G7-01', 640),
    ('G7-02', 780),
    ('G7-03', 1020),
    ('G8-01', 890),
    ('G8-02', 760),
    ('G8-03', 980),
    ('G8-04', 670),
    ('G9-01', 1120),
    ('G9-02', 930),
    ('G9-03', 810),
    ('G9-04', 750),
    ('G10-01', 1200),
    ('G10-02', 950),
    ('G10-03', 880),
    ('G10-04', 730),
    ('G10-05', 1010),
    ('G10-06', 840)
]
cursor.executemany("INSERT INTO scores(username,score) VALUES (?,?)", scores)

conn.commit()
conn.close()

print("Database recreated with realistic seed data")