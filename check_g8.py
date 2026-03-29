import sqlite3
try:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM students WHERE username LIKE 'G8-%' LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(row[0])
    else:
        print("None")
except Exception as e:
    print(f"Error: {e}")
finally:
    if conn: conn.close()
