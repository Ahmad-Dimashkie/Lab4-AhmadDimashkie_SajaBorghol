import sqlite3

# ----------------- Create Operations -----------------

# Function to add a student to the database


def add_student(student_id, name, age, email):
    """
    Adds a new student to the database.

    Parameters
    ----------
    student_id : str
        The unique identifier for the student.
    name : str
        The name of the student.
    age : int
        The age of the student.
    email : str
        The email address of the student.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Insert student into the students table
    cursor.execute(
        'INSERT INTO students (student_id,name, age, email) VALUES (?, ?, ?, ?)', (student_id, name, age, email))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to add an instructor to the database


def add_instructor(instructor_id, name, age, email):
    """
    Adds a new instructor to the database.

    Parameters
    ----------
    instructor_id : str
        The unique identifier for the instructor.
    name : str
        The name of the instructor.
    age : int
        The age of the instructor.
    email : str
        The email address of the instructor.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Insert instructor into the instructors table
    cursor.execute(
        'INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)', (instructor_id, name, age, email))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to add a course to the database


def add_course(course_id, course_name):
    """
    Adds a new course to the database.

    Parameters
    ----------
    course_id : str
        The unique identifier for the course.
    course_name : str
        The name of the course.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Insert the course into the database
    cursor.execute(
        "INSERT INTO courses (course_id, course_name) VALUES (?, ?)", (course_id, course_name))
    conn.commit()
    conn.close()


# Function to enroll a student in a course


def enroll_student(student_id, course_id):
    """
    Enrolls a student in a specified course.

    Parameters
    ----------
    student_id : str
        The ID of the student to enroll.
    course_id : str
        The ID of the course the student is enrolling in.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Insert into registrations (join table)
    cursor.execute(
        'INSERT INTO registrations (student_id, course_id) VALUES (?, ?)', (student_id, course_id))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to assign an instructor to a course


def assign_instructor(instructor_id, course_id):
    """
    Assigns an instructor to a specified course.

    Parameters
    ----------
    instructor_id : str
        The ID of the instructor.
    course_id : str
        The ID of the course.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Insert instructor assignment into the instructor_assignments table
    cursor.execute('''
        INSERT INTO instructor_assignments (instructor_id, course_id)
        VALUES (?, ?)
    ''', (instructor_id, course_id))

    # Commit and close the connection
    conn.commit()
    conn.close()

# ----------------- Read Operations -----------------

# Function to get all students


def get_students():
    """
    Retrieves all students from the database.

    Returns
    -------
    list
        A list of tuples representing each student.
        Each tuple contains (id, student_id, name, age, email).
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Select all students
    cursor.execute("SELECT id, student_id, name, age, email FROM students")
    students = cursor.fetchall()

    conn.close()
    return students

# Function to get all instructors


def get_instructors():
    """
    Retrieves all instructors from the database.

    Returns
    -------
    list
        A list of tuples representing each instructor.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Select all instructors
    cursor.execute('SELECT * FROM instructors')
    instructors = cursor.fetchall()

    conn.close()
    return instructors

# Function to get all courses


def get_courses():
    """
    Retrieves all courses from the database.

    Returns
    -------
    list
        A list of tuples representing each course.
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Select all courses
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()

    conn.close()
    return courses

# Function to get all enrollments


def get_enrollments():
    """
    Retrieves all student enrollments in courses.

    Returns
    -------
    list
        A list of tuples representing each enrollment.
        Each tuple contains (student_name, course_name).
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Select all registrations (enrollments)
    cursor.execute('''SELECT students.name, courses.course_name FROM registrations
                      JOIN students ON students.id = registrations.student_id
                      JOIN courses ON courses.id = registrations.course_id''')
    enrollments = cursor.fetchall()

    conn.close()
    return enrollments

# ----------------- Update Operations -----------------

# Function to update a student's information


def update_student(student_id, name, age, email):
    """
    Updates a student's information in the database.

    Parameters
    ----------
    student_id : str
        The ID of the student to update.
    name : str
        The new name of the student.
    age : int
        The new age of the student.
    email : str
        The new email address of the student.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Update student record
    cursor.execute('UPDATE students SET name = ?, age = ?, email = ? WHERE id = ?',
                   (name, age, email, student_id))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to update an instructor's information


def update_instructor(instructor_id, name, age, email):
    """
    Updates an instructor's information in the database.

    Parameters
    ----------
    instructor_id : str
        The ID of the instructor to update.
    name : str
        The new name of the instructor.
    age : int
        The new age of the instructor.
    email : str
        The new email address of the instructor.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Update instructor record
    cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE id = ?',
                   (name, age, email, instructor_id))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to update a course


def update_course(course_id, course_name):
    """
    Updates a course's name in the database.

    Parameters
    ----------
    course_id : str
        The ID of the course to update.
    course_name : str
        The new name of the course.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Update course record
    cursor.execute(
        'UPDATE courses SET course_name = ? WHERE id = ?', (course_name, course_id))

    # Commit and close the connection
    conn.commit()
    conn.close()

# ----------------- Delete Operations -----------------

# Function to delete a student


def delete_student(student_id):
    """
    Deletes a student from the database.

    Parameters
    ----------
    student_id : str
        The ID of the student to delete.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Delete student record
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to delete an instructor


def delete_instructor(instructor_id):
    """
    Deletes an instructor from the database.

    Parameters
    ----------
    instructor_id : str
        The ID of the instructor to delete.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Delete instructor record
    cursor.execute('DELETE FROM instructors WHERE id = ?', (instructor_id,))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to delete a course


def delete_course(course_id):
    """
    Deletes a course from the database.

    Parameters
    ----------
    course_id : str
        The ID of the course to delete.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Delete course record
    cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to delete a student from a course (remove enrollment)


def delete_enrollment(student_id, course_id):
    """
    Removes a student's enrollment from a course.

    Parameters
    ----------
    student_id : str
        The ID of the student.
    course_id : str
        The ID of the course.

    Returns
    -------
    None
    """
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Delete enrollment record
    cursor.execute(
        'DELETE FROM registrations WHERE student_id = ? AND course_id = ?', (student_id, course_id))

    # Commit and close the connection
    conn.commit()
    conn.close()
