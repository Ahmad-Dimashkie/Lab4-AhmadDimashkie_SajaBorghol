# School Management System Using Tkinter and PostgreSQL

This Python project is a school management system developed using Tkinter for the graphical user interface (GUI) and PostgreSQL for the database backend. The system allows users to add, edit, delete, search, and manage students, instructors, and courses. It also includes a feature for backing up the database to a JSON file.

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.x**
2. **PostgreSQL** - A relational database management system.
3. **Psycopg2** - A PostgreSQL adapter for Python. Install it using pip:
   ```bash
   pip install psycopg2
   ```

## Database Setup

Ensure that your PostgreSQL database is set up with the necessary tables:

```sql
CREATE TABLE students (
    student_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    email VARCHAR(100)
);

CREATE TABLE instructors (
    instructor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    email VARCHAR(100)
);

CREATE TABLE courses (
    course_id VARCHAR(50) PRIMARY KEY,
    course_name VARCHAR(100)
);

CREATE TABLE registrations (
    registration_id SERIAL PRIMARY KEY,
    student_id VARCHAR(50) REFERENCES students(student_id),
    course_id VARCHAR(50) REFERENCES courses(course_id)
);

CREATE TABLE instructor_courses (
    instructor_id VARCHAR(50) REFERENCES instructors(instructor_id),
    course_id VARCHAR(50) REFERENCES courses(course_id),
    PRIMARY KEY (instructor_id, course_id)
);
```

## Project Structure

The project contains several functions and GUI components to manage the school system effectively:

Key Functions

- `connect_to_db()`: Establishes a connection to the PostgreSQL database.
- `student_form()`: Creates a form for adding new students.
- `instructor_form()`: Creates a form for adding new instructors.
- `course_form()`: Creates a form for adding new courses.
- `add_student(name, age, email, student_id, course_name)`: Adds a student to the database.
- `add_instructor(name, age, email, instructor_id, course_name)`: Adds an instructor to the database.
- `add_course(course_id, course_name)`: Adds a course to the database.
- `populate_treeviews()`: Populates the tree views with data from the database.
- `edit_record(treeview, data_list, columns)`: Allows editing of records in the tree view.
- `delete_record(treeview, data_list)`: Deletes a selected record from the database.
- `update_course_dropdowns()`: Updates dropdown menus with available courses from the database.
- `search_records(search_term, criteria)`: Searches records in the database based on the provided criteria.
- `backup_database()`: Backs up the current state of the database to a JSON file.

## Graphical User Interface (GUI)

The GUI is built using Tkinter and is organized into three main tabs:

- Students Tab: Allows users to view, add, edit, and delete students.
- Instructors Tab: Allows users to view, add, edit, and delete instructors.
- Courses Tab: Allows users to view, add, edit, and delete courses.

## Database Backup

The backup_database() function provides the ability to back up the database to a JSON file. This backup includes all data from the students, instructors, courses, registrations, and instructor_courses tables.

## How to Run the Project

1. Clone the repository or copy the project files to your local machine.
2. Ensure PostgreSQL is running and the database is set up correctly with the necessary tables.
3. Run the Python script:

```
python Tkinter_with_db.py
```

4. Interact with the GUI to manage students, instructors, and courses.
5.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
