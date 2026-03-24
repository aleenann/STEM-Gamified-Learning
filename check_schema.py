import sqlite3

def check_schema():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(scores)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"Column: {col[1]}, Type: {col[2]}")
    conn.close()

if __name__ == "__main__":
    check_schema()
