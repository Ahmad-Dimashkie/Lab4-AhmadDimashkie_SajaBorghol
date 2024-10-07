import sqlite3


def recreate_tables():
    conn = sqlite3.connect('school_management.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Drop dependent tables first
    cursor.execute('DROP TABLE IF EXISTS instructor_assignments')
    cursor.execute('DROP TABLE IF EXISTS registrations')

    # Now drop the main tables
    cursor.execute('DROP TABLE IF EXISTS students')
    cursor.execute('DROP TABLE IF EXISTS instructors')
    cursor.execute('DROP TABLE IF EXISTS courses')

    # Recreate students table
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Recreate instructors table
    cursor.execute('''
        CREATE TABLE instructors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instructor_id TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Recreate courses table
    cursor.execute('''
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL,
            course_name TEXT NOT NULL
        )
    ''')

    # Recreate instructor_assignments table
    cursor.execute('''
        CREATE TABLE instructor_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            instructor_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (instructor_id) REFERENCES instructors(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    # Recreate registrations table for student-course enrollments
    cursor.execute('''
        CREATE TABLE registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    recreate_tables()
