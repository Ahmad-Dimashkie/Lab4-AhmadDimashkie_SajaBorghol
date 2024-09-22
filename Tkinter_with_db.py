import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re
import json
import subprocess
import os

def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        conn (psycopg2.connection): The connection object to interact with the database.
        None: If the connection attempt fails, displays an error message and returns None.

    Raises:
        psycopg2.Error: If there is an issue connecting to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            dbname="Lab_2_435L_tkinter",  # The name of the database to connect to.
            user="postgres",              # The username to authenticate with PostgreSQL.
            password="doudi123$",         # The password for the PostgreSQL user.
            host="localhost",             # The host where the PostgreSQL server is located.
            port="5432"                   # The port where PostgreSQL is listening.
        )
        return conn
    except psycopg2.Error as e:
        # Show an error message if the connection fails.
        messagebox.showerror("Database Connection Error", str(e))
        return None

def create_search_frame():
    """
    Creates a search frame for the user interface where users can input search queries.
    
    The frame contains:
        - A label for "Search".
        - An entry box to input the search query.
        - A dropdown (combobox) to choose search criteria ("Name", "ID", "Course").
        - A "Search" button that triggers the search_records function when clicked.
    
    The search is performed based on the selected criteria and the user's input.
    
    Args:
        None
    
    Returns:
        None
    """
    # Create a frame within the root window for the search interface.
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)  # Add padding around the frame for spacing.

    # Add a label "Search" to the frame.
    tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)

    # Add an entry widget (input field) where the user can type the search query.
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)  # Add padding to space out elements.

    # Add a label "Search by:" to the frame.
    tk.Label(search_frame, text="Search by:").pack(side=tk.LEFT, padx=5)

    # Add a combobox (dropdown menu) for the user to select search criteria (Name, ID, or Course).
    search_criteria = ttk.Combobox(search_frame, values=["Name", "ID", "Course"], state="readonly")
    search_criteria.pack(side=tk.LEFT, padx=5)
    search_criteria.current(0)  # Set the default selection to "Name".

    # Add a "Search" button that triggers the search_records function when clicked.
    # It passes the search entry and the selected criteria as arguments to search_records.
    tk.Button(search_frame, text="Search", command=lambda: search_records(search_entry.get(), search_criteria.get())).pack(side=tk.LEFT, padx=5)


# Initialize the main application window
root = tk.Tk()
root.title("School Management System")
root.geometry("1000x600")
root.resizable(True, True)

# Create a canvas widget for displaying scrollable content within the window
canvas = tk.Canvas(root)

# Create a vertical scrollbar that will allow the canvas to be scrolled
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

# Create a scrollable frame that will hold all the elements and widgets
scrollable_frame = tk.Frame(canvas)

# Bind the configuration of the frame to update the canvas scroll region
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Create a window in the canvas where the scrollable frame will be embedded
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Configure the canvas to work with the vertical scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas to fill the available space within the window
canvas.pack(side="left", fill="both", expand=True)

# Pack the scrollbar on the right side of the window, filling the vertical space
scrollbar.pack(side="right", fill="y")

# Initialize global variables to store the available courses and dropdown widgets
available_courses = []  # This will store the available courses fetched from the database
course_dropdown = None  # Dropdown widget for selecting courses in the student form
instructor_course_dropdown = None  # Dropdown widget for selecting courses in the instructor form
students = []  # List to store student data
instructors = []  # List to store instructor data

def validate_age(age):
    """
    Validates if the provided age is a positive integer.

    Args:
        age (str): The age input as a string.

    Returns:
        int: The validated age as an integer if valid, or None if invalid.

    Raises:
        ValueError: If the age is negative or not a valid integer.
    """
    try:
        # Attempt to convert the age to an integer
        age = int(age)
        if age < 0:
            # Raise an error if the age is negative
            raise ValueError("Age cannot be negative.")
        return age
    except ValueError as ve:
        # Show an error message box if the age is invalid
        messagebox.showerror("Invalid Age", f"Invalid age: {ve}")
        return None


def validate_email(email):
    """
    Validates if the provided email follows a valid email format using a regular expression.

    Args:
        email (str): The email address input as a string.

    Returns:
        str: The validated email if it matches the expected format, or None if invalid.
    """
    # Regular expression pattern for validating an email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Check if the email matches the pattern
    if not re.match(pattern, email):
        # Show an error message if the email is invalid
        messagebox.showerror("Invalid Email", f"Invalid email format: {email}")
        return None
    
    return email

def student_form():
    """
    Creates a form in the GUI for adding a new student to the system.
    
    This function generates a form where users can input student details, including
    name, age, email, student ID, and course. Upon clicking the "Add Student" button, 
    the provided information is passed to the `add_student` function for validation 
    and database insertion.
    
    Returns:
        None
    """
    global course_dropdown  # To be updated with the available courses

    # Create a frame for the student form with padding
    student_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
    student_frame.pack(pady=20)

    # Title Label
    tk.Label(student_frame, text="Add Student", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

    # Name Input
    tk.Label(student_frame, text="Name:").grid(row=1, column=0, sticky="e")
    student_name = tk.Entry(student_frame)
    student_name.grid(row=1, column=1)

    # Age Input
    tk.Label(student_frame, text="Age:").grid(row=2, column=0, sticky="e")
    student_age = tk.Entry(student_frame)
    student_age.grid(row=2, column=1)

    # Email Input
    tk.Label(student_frame, text="Email:").grid(row=3, column=0, sticky="e")
    student_email = tk.Entry(student_frame)
    student_email.grid(row=3, column=1)

    # Student ID Input
    tk.Label(student_frame, text="Student ID:").grid(row=4, column=0, sticky="e")
    student_id = tk.Entry(student_frame)
    student_id.grid(row=4, column=1)

    # Course Selection Dropdown
    tk.Label(student_frame, text="Select Course:").grid(row=5, column=0, sticky="e")
    selected_course = tk.StringVar()
    course_dropdown = ttk.Combobox(student_frame, textvariable=selected_course, state="readonly")
    course_dropdown['values'] = [course['course_name'] for course in available_courses]  # Populating with available courses
    course_dropdown.grid(row=5, column=1)

    # Add Student Button, connected to the `add_student` function
    tk.Button(student_frame, text="Add Student", command=lambda: add_student(
        student_name.get(), student_age.get(), student_email.get(), student_id.get(), selected_course.get())
    ).grid(row=6, columnspan=2, pady=10)

def instructor_form():
    """
    Creates a form in the GUI for adding a new instructor to the system.
    
    This function generates a form where users can input instructor details, including
    name, age, email, instructor ID, and the course they will be assigned to. Upon 
    clicking the "Add Instructor" button, the provided information is passed to the 
    `add_instructor` function for validation and database insertion.
    
    Returns:
        None
    """
    global instructor_course_dropdown  # To be updated with the available courses

    # Create a frame for the instructor form with padding
    instructor_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
    instructor_frame.pack(pady=20)

    # Title Label
    tk.Label(instructor_frame, text="Add Instructor", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

    # Name Input
    tk.Label(instructor_frame, text="Name:").grid(row=1, column=0, sticky="e")
    instructor_name = tk.Entry(instructor_frame)
    instructor_name.grid(row=1, column=1)

    # Age Input
    tk.Label(instructor_frame, text="Age:").grid(row=2, column=0, sticky="e")
    instructor_age = tk.Entry(instructor_frame)
    instructor_age.grid(row=2, column=1)

    # Email Input
    tk.Label(instructor_frame, text="Email:").grid(row=3, column=0, sticky="e")
    instructor_email = tk.Entry(instructor_frame)
    instructor_email.grid(row=3, column=1)

    # Instructor ID Input
    tk.Label(instructor_frame, text="Instructor ID:").grid(row=4, column=0, sticky="e")
    instructor_id = tk.Entry(instructor_frame)
    instructor_id.grid(row=4, column=1)

    # Course Assignment Dropdown
    tk.Label(instructor_frame, text="Assign Course:").grid(row=5, column=0, sticky="e")
    selected_course = tk.StringVar()
    instructor_course_dropdown = ttk.Combobox(instructor_frame, textvariable=selected_course, state="readonly")
    instructor_course_dropdown['values'] = [course['course_name'] for course in available_courses]  # Populate with available courses
    instructor_course_dropdown.grid(row=5, column=1)

    # Add Instructor Button, connected to the `add_instructor` function
    tk.Button(instructor_frame, text="Add Instructor", command=lambda: add_instructor(
        instructor_name.get(), instructor_age.get(), instructor_email.get(), instructor_id.get(), selected_course.get())
    ).grid(row=6, columnspan=2, pady=10)

def course_form():
    """
    Creates a form in the GUI for adding a new course to the system.
    
    This function generates a form where users can input course details, including 
    the Course ID and Course Name. Upon clicking the "Add Course" button, the 
    provided information is passed to the `add_course` function for validation 
    and insertion into the database.

    Returns:
        None
    """
    # Create a frame for the course form with padding
    course_frame = tk.Frame(scrollable_frame, padx=10, pady=10)
    course_frame.pack(pady=20)

    # Title Label
    tk.Label(course_frame, text="Add Course", font=("Arial", 16)).grid(row=0, columnspan=2, pady=10)

    # Course ID Input
    tk.Label(course_frame, text="Course ID:").grid(row=1, column=0, sticky="e")
    course_id = tk.Entry(course_frame)
    course_id.grid(row=1, column=1)

    # Course Name Input
    tk.Label(course_frame, text="Course Name:").grid(row=2, column=0, sticky="e")
    course_name = tk.Entry(course_frame)
    course_name.grid(row=2, column=1)

    # Add Course Button, connected to the `add_course` function
    tk.Button(course_frame, text="Add Course", command=lambda: add_course(course_id.get(), course_name.get())).grid(row=3, columnspan=2, pady=10)

def add_student(name, age, email, student_id, course_name):
    """
    Adds a new student to the database.

    This function takes the student's details (name, age, email, and student ID), 
    validates the input, and then inserts the student information into the 
    'students' table in the database. If a course is selected, it registers 
    the student in that course by inserting into the 'registrations' table.

    Args:
        name (str): The name of the student.
        age (str): The age of the student, which will be validated as a positive integer.
        email (str): The student's email, which will be validated for correct format.
        student_id (str): A unique identifier for the student.
        course_name (str): The course selected by the student (if any).
    
    Returns:
        None
    """
    # Validate the presence of required fields
    if not name or not student_id:
        messagebox.showerror("Error", "Name and Student ID are required.")
        return

    # Validate age and email format
    age = validate_age(age)
    email = validate_email(email)

    if age is not None and email is not None:
        conn = connect_to_db()  # Establish connection to the database
        if conn:
            try:
                cur = conn.cursor()
                
                # Insert the student into the 'students' table
                cur.execute(
                    "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s);",
                    (student_id, name, age, email)
                )

                # If a course is selected, register the student in the course
                if course_name:
                    cur.execute("SELECT course_id FROM courses WHERE course_name = %s;", (course_name,))
                    course_id = cur.fetchone()[0]
                    
                    cur.execute(
                        "INSERT INTO registrations (student_id, course_id) VALUES (%s, %s);",
                        (student_id, course_id)
                    )

                conn.commit()  # Commit the changes to the database
                cur.close()  # Close the cursor
                messagebox.showinfo("Success", f"Student Added: {name}, {age}, {email}")
                
                populate_treeviews()  # Refresh the UI treeviews to reflect the new student
            except psycopg2.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()  # Ensure the connection is closed


def add_instructor(name, age, email, instructor_id, course_name):
    """
    Adds a new instructor to the database.

    This function takes the instructor's details (name, age, email, and instructor ID), 
    validates the input, and then inserts the instructor's information into the 
    'instructors' table in the database. If a course is assigned, it also 
    registers the instructor to that course by inserting into the 'instructor_courses' table.

    Args:
        name (str): The name of the instructor.
        age (str): The age of the instructor, which will be validated as a positive integer.
        email (str): The instructor's email, which will be validated for correct format.
        instructor_id (str): A unique identifier for the instructor.
        course_name (str): The course assigned to the instructor (if any).
    
    Returns:
        None
    """
    # Validate the presence of required fields
    if not name or not instructor_id:
        messagebox.showerror("Error", "Name and Instructor ID are required.")
        return

    # Validate age and email format
    age = validate_age(age)
    email = validate_email(email)

    if age is not None and email is not None:
        conn = connect_to_db()  # Establish connection to the database
        if conn:
            try:
                cur = conn.cursor()

                # Insert the instructor into the 'instructors' table
                cur.execute(
                    "INSERT INTO instructors (instructor_id, name, age, email) VALUES (%s, %s, %s, %s);",
                    (instructor_id, name, age, email)
                )

                # If a course is assigned, register the instructor to that course
                if course_name:
                    cur.execute("SELECT course_id FROM courses WHERE course_name = %s;", (course_name,))
                    course_id = cur.fetchone()[0]

                    cur.execute(
                        "INSERT INTO instructor_courses (instructor_id, course_id) VALUES (%s, %s);",
                        (instructor_id, course_id)
                    )

                conn.commit()  # Commit the changes to the database
                cur.close()  # Close the cursor
                messagebox.showinfo("Success", f"Instructor Added: {name}, {age}, {email}, {instructor_id}")
                
                populate_treeviews()  # Refresh the UI treeviews to reflect the new instructor
            except psycopg2.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()  # Ensure the connection is closed

def add_course(course_id, course_name):
    """
    Adds a new course to the database.

    This function inserts a new course into the 'courses' table in the database 
    after validating the input fields for Course ID and Course Name. It also updates 
    the course dropdowns and refreshes the UI treeviews to display the new course.

    Args:
        course_id (str): Unique identifier for the course.
        course_name (str): Name of the course.
    
    Returns:
        None
    """
    # Validate that both Course ID and Course Name are provided
    if not course_id or not course_name:
        messagebox.showerror("Error", "Course ID and Course Name are required.")
        return
    
    # Establish a connection to the database
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert the course into the 'courses' table
            cur.execute(
                "INSERT INTO courses (course_id, course_name) VALUES (%s, %s);",
                (course_id, course_name)
            )
            conn.commit()  # Commit the changes to the database
            cur.close()  # Close the cursor

            # Show success message
            messagebox.showinfo("Success", f"Course Added: {course_id}, {course_name}")

            # Update dropdowns and refresh the UI treeviews
            update_course_dropdowns()  
            populate_treeviews()
        except psycopg2.Error as e:
            # Show error message if any database errors occur
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()  # Ensure the database connection is closed

def populate_treeviews():
    """
    Populates the treeview widgets with data from the database.

    This function fetches and displays records from the 'students', 'instructors', 
    and 'courses' tables, along with their corresponding relationships in the 
    registrations and instructor_courses tables. The data is displayed in their 
    respective treeviews for students, instructors, and courses.

    Returns:
        None
    """
    # Establish a connection to the database
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()

            # Clear all existing data from the treeviews (students, instructors, courses)
            for tree in [student_tree, instructor_tree, course_tree]:
                for item in tree.get_children():
                    tree.delete(item)

            # Fetch and populate student data
            cur.execute("""
                SELECT s.name, s.age, s.email, s.student_id, c.course_name 
                FROM students s 
                LEFT JOIN registrations r ON s.student_id = r.student_id 
                LEFT JOIN courses c ON r.course_id = c.course_id;
            """)
            students = cur.fetchall()
            for student in students:
                student_tree.insert('', 'end', values=student)

            # Fetch and populate instructor data
            cur.execute("""
                SELECT i.name, i.age, i.email, i.instructor_id, c.course_name 
                FROM instructors i 
                LEFT JOIN instructor_courses ic ON i.instructor_id = ic.instructor_id
                LEFT JOIN courses c ON ic.course_id = c.course_id;
            """)
            instructors = cur.fetchall()
            for instructor in instructors:
                instructor_tree.insert('', 'end', values=instructor)

            # Fetch and populate course data
            cur.execute("SELECT course_id, course_name FROM courses;")
            courses = cur.fetchall()
            for course in courses:
                course_tree.insert('', 'end', values=course)

            cur.close()  # Close the cursor after use
        except psycopg2.Error as e:
            # Handle and display any database errors
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()  # Ensure the database connection is closed

def edit_record(treeview, data_list, columns):
    """
    Allows editing of a selected record in a treeview.

    This function opens a new window with entry fields populated with the 
    selected item's values. Once edited, it updates the corresponding 
    database entry with the new values.

    Args:
        treeview (ttk.Treeview): The treeview from which the record is selected.
        data_list (list): A list of data representing the records.
        columns (list): A list of column names for the data being edited.

    Returns:
        None
    """
    # Ensure a record is selected for editing
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Edit Record", "No record selected.")
        return

    # Get the selected record's values
    item = treeview.item(selected_item)['values']
    
    # Create a new window for editing
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Record")

    # Create entry fields for each column
    entries = []
    for idx, column in enumerate(columns):
        tk.Label(edit_window, text=column).grid(row=idx, column=0)
        entry = tk.Entry(edit_window)
        entry.insert(0, item[idx])  # Pre-fill with current values
        entry.grid(row=idx, column=1)
        entries.append(entry)

    # Function to save changes back to the database
    def save_changes():
        new_values = [entry.get() for entry in entries]
        conn = connect_to_db()
        if conn:
            try:
                cur = conn.cursor()
                # Update the relevant table based on which treeview is being edited
                if treeview == student_tree:
                    cur.execute(
                        "UPDATE students SET name = %s, age = %s, email = %s WHERE student_id = %s;",
                        (new_values[0], new_values[1], new_values[2], item[3])
                    )
                elif treeview == instructor_tree:
                    cur.execute(
                        "UPDATE instructors SET name = %s, age = %s, email = %s WHERE instructor_id = %s::VARCHAR;",
                        (new_values[0], new_values[1], new_values[2], str(item[3]))  
                    )
                elif treeview == course_tree:
                    cur.execute(
                        "UPDATE courses SET course_id = %s, course_name = %s WHERE course_id = %s;",
                        (new_values[0], new_values[1], item[0])
                    )
                
                # Commit changes and refresh the treeviews
                conn.commit()
                cur.close()
                populate_treeviews()  
                edit_window.destroy()
            except psycopg2.Error as e:
                # Show an error message in case of a database error
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

    # Add a button to save the changes
    tk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=len(columns), columnspan=2)

def delete_record(treeview, data_list):
    """
    Deletes a selected record from the database based on the selected treeview.

    This function allows users to select a record from the treeview and delete 
    the corresponding entry from the database. It prompts the user for confirmation 
    before performing the deletion.

    Args:
        treeview (ttk.Treeview): The treeview from which the record is selected for deletion.
        data_list (list): A list representing the data from the treeview.

    Returns:
        None
    """
    # Check if a record is selected for deletion
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Delete Record", "No record selected.")
        return

    # Confirm deletion from the user
    if messagebox.askyesno("Delete Record", "Are you sure you want to delete the selected record?"):
        conn = connect_to_db()
        if conn:
            try:
                cur = conn.cursor()
                item = treeview.item(selected_item)['values']

                # Check which treeview is being used and delete the appropriate record
                if treeview == student_tree:
                    cur.execute("DELETE FROM students WHERE student_id = %s::VARCHAR;", (str(item[3]),))
                    cur.execute("DELETE FROM registrations WHERE student_id = %s::VARCHAR;", (str(item[3]),))
                elif treeview == instructor_tree:
                    cur.execute("DELETE FROM instructor_courses WHERE instructor_id = %s::VARCHAR;", (str(item[3]),))
                    cur.execute("DELETE FROM instructors WHERE instructor_id = %s::VARCHAR;", (str(item[3]),))
                elif treeview == course_tree:
                    cur.execute("DELETE FROM instructor_courses WHERE course_id = %s::VARCHAR;", (str(item[0]),))
                    cur.execute("DELETE FROM registrations WHERE course_id = %s::VARCHAR;", (str(item[0]),))
                    cur.execute("DELETE FROM courses WHERE course_id = %s::VARCHAR;", (str(item[0]),))

                # Commit the deletion and refresh the treeview
                conn.commit()
                cur.close()
                populate_treeviews()  # Refresh the treeviews to reflect changes
            except psycopg2.Error as e:
                # Handle database errors
                messagebox.showerror("Database Error", str(e))
            finally:
                conn.close()

def update_course_dropdowns():
    """
    Updates the dropdown menus for both students and instructors with the available courses.

    This function fetches the course names from the `courses` table in the database and populates 
    the `course_dropdown` (used in the student form) and `instructor_course_dropdown` 
    (used in the instructor form) with the available course options.

    Args:
        None

    Returns:
        None
    """
    # Connect to the database
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            # Fetch all course names from the 'courses' table
            cur.execute("SELECT course_name FROM courses;")
            courses = [course[0] for course in cur.fetchall()]  # Extract course names

            # Update the course dropdown for students if available
            if course_dropdown:
                course_dropdown['values'] = courses

            # Update the course dropdown for instructors if available
            if instructor_course_dropdown:
                instructor_course_dropdown['values'] = courses

            # Close the cursor after successful update
            cur.close()
        except psycopg2.Error as e:
            # Handle database connection errors
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

def search_records(search_term, criteria):
    """
    Searches for records in the database based on the provided search term and criteria.

    Args:
        search_term (str): The term to search for.
        criteria (str): The criteria to search by. It can be "Name", "ID", or "Course".

    Returns:
        None
    """
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()

            # Search by student or instructor name
            if criteria == "Name":
                # Query for students based on name
                cur.execute("""
                    SELECT s.name, s.age, s.email, s.student_id, c.course_name 
                    FROM students s 
                    LEFT JOIN registrations r ON s.student_id = r.student_id 
                    LEFT JOIN courses c ON r.course_id = c.course_id 
                    WHERE s.name ILIKE %s;
                """, ('%' + search_term + '%',))
                filtered_students = cur.fetchall()
                
                # Query for instructors based on name
                cur.execute("""
                    SELECT i.name, i.age, i.email, i.instructor_id, c.course_name 
                    FROM instructors i 
                    LEFT JOIN instructor_courses ic ON i.instructor_id = ic.instructor_id
                    LEFT JOIN courses c ON ic.course_id = c.course_id 
                    WHERE i.name ILIKE %s;
                """, ('%' + search_term + '%',))
                filtered_instructors = cur.fetchall()

            # Search by student or instructor ID
            elif criteria == "ID":
                # Query for students based on ID
                cur.execute("""
                    SELECT s.name, s.age, s.email, s.student_id, c.course_name 
                    FROM students s 
                    LEFT JOIN registrations r ON s.student_id = r.student_id 
                    LEFT JOIN courses c ON r.course_id = c.course_id 
                    WHERE s.student_id::TEXT ILIKE %s;
                """, ('%' + search_term + '%',))
                filtered_students = cur.fetchall()
                
                # Query for instructors based on ID
                cur.execute("""
                    SELECT i.name, i.age, i.email, i.instructor_id, c.course_name 
                    FROM instructors i 
                    LEFT JOIN instructor_courses ic ON i.instructor_id = ic.instructor_id
                    LEFT JOIN courses c ON ic.course_id = c.course_id 
                    WHERE i.instructor_id::TEXT ILIKE %s;
                """, ('%' + search_term + '%',))
                filtered_instructors = cur.fetchall()

            # Search by course name
            elif criteria == "Course":
                # Query for students based on course name
                cur.execute("""
                    SELECT s.name, s.age, s.email, s.student_id, c.course_name 
                    FROM students s 
                    LEFT JOIN registrations r ON s.student_id = r.student_id 
                    LEFT JOIN courses c ON r.course_id = c.course_id 
                    WHERE c.course_name ILIKE %s;
                """, ('%' + search_term + '%',))
                filtered_students = cur.fetchall()
                
                # Query for instructors based on course name
                cur.execute("""
                    SELECT i.name, i.age, i.email, i.instructor_id, c.course_name 
                    FROM instructors i 
                    LEFT JOIN instructor_courses ic ON i.instructor_id = ic.instructor_id
                    LEFT JOIN courses c ON ic.course_id = c.course_id 
                    WHERE c.course_name ILIKE %s;
                """, ('%' + search_term + '%',))
                filtered_instructors = cur.fetchall()

            # Update the tree views with the filtered results
            update_treeview(student_tree, filtered_students)
            update_treeview(instructor_tree, filtered_instructors)

            # Query for courses based on course name
            cur.execute("SELECT course_id, course_name FROM courses WHERE course_name ILIKE %s;", ('%' + search_term + '%',))
            filtered_courses = cur.fetchall()
            update_treeview(course_tree, filtered_courses)

            cur.close()
        except psycopg2.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

def update_treeview(treeview, data):
    """
    Updates the specified treeview widget with new data.

    Args:
        treeview (ttk.Treeview): The treeview widget to update.
        data (list): A list of tuples containing the data to display in the treeview.

    Returns:
        None
    """
    # Clear all existing items in the treeview
    for item in treeview.get_children():
        treeview.delete(item)

    # Insert new data into the treeview
    for record in data:
        treeview.insert('', 'end', values=record)

def backup_database():
    """
    Backs up the current database contents (students, instructors, courses, registrations, and assignments)
    into a JSON file selected by the user.

    This function prompts the user to select a file location and name, then gathers data from the database,
    including students, instructors, courses, registrations, and instructor assignments, and writes this
    data into a JSON file.
    
    Returns:
        None
    """
    # Ask user to specify a file path for saving the JSON backup
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json")],
        title="Save Database Backup"
    )
    
    # If the user provides a file path, proceed with the backup
    if file_path:
        conn = connect_to_db()
        if not conn:
            return
        cursor = conn.cursor()

        try:
            # Fetch data from each table in the database
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()

            cursor.execute("SELECT * FROM instructors")
            instructors = cursor.fetchall()

            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()

            cursor.execute("SELECT * FROM registrations")
            registrations = cursor.fetchall()

            cursor.execute("SELECT * FROM instructor_courses")
            assignments = cursor.fetchall()

            # Organize fetched data into a structured dictionary for JSON export
            backup_data = {
                "students": [{"student_id": s[0], "name": s[1], "age": s[2], "email": s[3]} for s in students],
                "instructors": [{"instructor_id": i[0], "name": i[1], "age": i[2], "email": i[3]} for i in instructors],
                "courses": [{"course_id": c[0], "course_name": c[1]} for c in courses],
                "registrations": [{"student_id": r[1], "course_id": r[2]} for r in registrations],
                "assignments": [{"instructor_id": a[0], "course_id": a[1]} for a in assignments]
            }

            # Save the data into the selected JSON file
            with open(file_path, 'w') as backup_file:
                json.dump(backup_data, backup_file, indent=4)
            
            # Notify user of successful backup
            messagebox.showinfo("Success", "Database backup saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to back up database: {e}")
        finally:
            # Close the database connection
            cursor.close()
            conn.close()

def initialize_ui():
    """
    Initializes the user interface by creating and displaying the search frame, 
    student form, instructor form, course form, and populating the treeviews with data.

    This function sets up the essential components of the School Management System's
    graphical user interface (GUI), including forms for adding students, instructors, and
    courses, as well as a search frame for querying data. It also populates the treeviews
    with the current data from the database.
    
    Returns:
        None
    """
    # Set up the search frame for filtering and searching data
    create_search_frame()
    
    # Create the student form interface for adding new students
    student_form()
    
    # Create the instructor form interface for adding new instructors
    instructor_form()
    
    # Create the course form interface for adding new courses
    course_form()
    
    # Populate the treeviews with data from the database (students, instructors, courses)
    populate_treeviews()


notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --- Students Tab ---
student_tab = ttk.Frame(notebook)
notebook.add(student_tab, text='Students')

# Treeview for displaying student data
student_tree = ttk.Treeview(student_tab, columns=("Name", "Age", "Email", "Student ID", "Registered Course"), show="headings")
student_tree.heading("Name", text="Name")
student_tree.heading("Age", text="Age")
student_tree.heading("Email", text="Email")
student_tree.heading("Student ID", text="Student ID")
student_tree.heading("Registered Course", text="Registered Course")
student_tree.pack(fill="both", expand=True)

# Horizontal scrollbar for the student treeview
student_tree_scroll_x = tk.Scrollbar(student_tab, orient='horizontal', command=student_tree.xview)
student_tree.configure(xscrollcommand=student_tree_scroll_x.set)
student_tree_scroll_x.pack(side='bottom', fill='x')

# Edit and Delete buttons for students
tk.Button(student_tab, text="Edit Student", command=lambda: edit_record(student_tree, students, ["Name", "Age", "Email", "Student ID", "Registered Course"])).pack(pady=5)
tk.Button(student_tab, text="Delete Student", command=lambda: delete_record(student_tree, students)).pack(pady=5)

# --- Instructors Tab ---
instructor_tab = ttk.Frame(notebook)
notebook.add(instructor_tab, text='Instructors')

# Treeview for displaying instructor data
instructor_tree = ttk.Treeview(instructor_tab, columns=("Name", "Age", "Email", "Instructor ID", "Assigned Course"), show="headings")
instructor_tree.heading("Name", text="Name")
instructor_tree.heading("Age", text="Age")
instructor_tree.heading("Email", text="Email")
instructor_tree.heading("Instructor ID", text="Instructor ID")
instructor_tree.heading("Assigned Course", text="Assigned Course")
instructor_tree.pack(fill="both", expand=True)

# Horizontal scrollbar for the instructor treeview
instructor_tree_scroll_x = tk.Scrollbar(instructor_tab, orient='horizontal', command=instructor_tree.xview)
instructor_tree.configure(xscrollcommand=instructor_tree_scroll_x.set)
instructor_tree_scroll_x.pack(side='bottom', fill='x')

# Edit and Delete buttons for instructors
tk.Button(instructor_tab, text="Edit Instructor", command=lambda: edit_record(instructor_tree, instructors, ["Name", "Age", "Email", "Instructor ID", "Assigned Course"])).pack(pady=5)
tk.Button(instructor_tab, text="Delete Instructor", command=lambda: delete_record(instructor_tree, instructors)).pack(pady=5)

# --- Courses Tab ---
course_tab = ttk.Frame(notebook)
notebook.add(course_tab, text='Courses')

# Treeview for displaying course data
course_tree = ttk.Treeview(course_tab, columns=("Course ID", "Course Name"), show="headings")
course_tree.heading("Course ID", text="Course ID")
course_tree.heading("Course Name", text="Course Name")
course_tree.pack(fill="both", expand=True)

# Horizontal scrollbar for the course treeview
course_tree_scroll_x = tk.Scrollbar(course_tab, orient='horizontal', command=course_tree.xview)
course_tree.configure(xscrollcommand=course_tree_scroll_x.set)
course_tree_scroll_x.pack(side='bottom', fill='x')

# Edit and Delete buttons for courses
tk.Button(course_tab, text="Edit Course", command=lambda: edit_record(course_tree, available_courses, ["Course ID", "Course Name"])).pack(pady=5)
tk.Button(course_tab, text="Delete Course", command=lambda: delete_record(course_tree, available_courses)).pack(pady=5)

# --- Backup Database Button ---
tk.Button(root, text="Backup Database", command=backup_database).pack(side=tk.LEFT, padx=10, pady=10)

# Initialize the UI
initialize_ui()

# Start the main event loop
root.mainloop()
