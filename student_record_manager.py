"""Student Record Manager - beginner CRUD project using Python + SQLite."""
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).with_name("students.db")


def connect():
    return sqlite3.connect(DB_FILE)


def create_table():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            email TEXT UNIQUE
        )""")


def add_student():
    name = input("Student name: ").strip()
    age_text = input("Age: ").strip()
    course = input("Course: ").strip()
    email = input("Email (optional): ").strip() or None
    if not name or not course:
        print("Name and course are required.")
        return
    try:
        age = int(age_text)
        if age < 1:
            raise ValueError
        with connect() as db:
            db.execute(
                "INSERT INTO students (name, age, course, email) VALUES (?, ?, ?, ?)",
                (name, age, course, email),
            )
        print("Student added successfully.")
    except ValueError:
        print("Please enter a valid positive age.")
    except sqlite3.IntegrityError:
        print("That email is already registered. Try another email.")


def view_students():
    with connect() as db:
        rows = db.execute(
            "SELECT student_id, name, age, course, email FROM students ORDER BY student_id"
        ).fetchall()
    if not rows:
        print("No student records found.")
        return
    print("\nID | Name | Age | Course | Email")
    print("-" * 65)
    for row in rows:
        print(" | ".join(str(value or "-") for value in row))


def update_student():
    try:
        student_id = int(input("Student ID to update: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return
    name = input("New name: ").strip()
    course = input("New course: ").strip()
    if not name or not course:
        print("Name and course cannot be empty.")
        return
    with connect() as db:
        cursor = db.execute(
            "UPDATE students SET name = ?, course = ? WHERE student_id = ?",
            (name, course, student_id),
        )
    print("Record updated." if cursor.rowcount else "Student ID not found.")


def delete_student():
    try:
        student_id = int(input("Student ID to delete: "))
    except ValueError:
        print("Enter a valid numeric ID.")
        return
    with connect() as db:
        cursor = db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    print("Record deleted." if cursor.rowcount else "Student ID not found.")


def main():
    create_table()
    actions = {
        "1": add_student,
        "2": view_students,
        "3": update_student,
        "4": delete_student,
    }
    while True:
        print("\n=== STUDENT RECORD MANAGER ===")
        print("1. Add student\n2. View students\n3. Update student\n4. Delete student\n5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
