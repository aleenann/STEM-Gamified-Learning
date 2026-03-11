from flask import Flask, render_template, request, redirect, session
import sqlite3

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

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?", 
                   (username, password, role))

    user = cursor.fetchone()
    conn.close()

    if user:
        session["name"] = user[4]  # name is at index 4
        if role == "student":
            return redirect("/student")
        if role == "teacher":
            return redirect("/teacher")

    return f"Invalid Login. Please try again from the <a href='/login/{role}'>login page</a>."

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")




# Student dashboard
@app.route("/student")
def student():
    return render_template("student_dashboard.html")


# Teacher dashboard
@app.route("/teacher")
def teacher():
    return render_template("teacher_dashboard.html")


# Quiz / Game Page
@app.route("/quiz")
def quiz():
    return render_template("quiz_game.html")


# Save game score
@app.route("/save_score", methods=["POST"])
def save_score():

    username = request.form["username"]
    score = request.form["score"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO scores(username,score) VALUES (?,?)",
                   (username,score))

    conn.commit()
    conn.close()

    return "Score Saved"


if __name__ == "__main__":
    app.run(debug=True)