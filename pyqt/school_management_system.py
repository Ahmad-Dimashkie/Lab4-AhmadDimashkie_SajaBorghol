import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFormLayout, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QFileDialog
import csv
import re
from operations import assign_instructor, enroll_student, add_student, get_students, update_student, delete_student, get_instructors, add_instructor, delete_instructor, get_courses, add_course, delete_course, get_students

# Create a main window class


class SchoolManagementSystem(QMainWindow):

    """
    A PyQt5-based GUI for managing students, instructors, and courses in a school.

    This class provides a user interface for adding, editing, and deleting students,
    instructors, and courses, as well as registering students in courses and assigning
    instructors to courses.

    Methods
    -------
    create_student_form()
        Creates the form for adding new students.
    create_instructor_form()
        Creates the form for adding new instructors.
    create_course_form()
        Creates the form for adding new courses.
    create_registration_form()
        Creates the form for registering students for courses.
    create_assignment_form()
        Creates the form for assigning instructors to courses.
    add_student()
        Adds a new student to the system.
    add_instructor()
        Adds a new instructor to the system.
    add_course()
        Adds a new course to the system.
    update_student_dropdown()
        Updates the student dropdown list with available students.
    update_instructor_dropdown()
        Updates the instructor dropdown list with available instructors.
    update_course_dropdown()
        Updates the course dropdown list with available courses.
    update_table()
        Refreshes the table to display the latest student, instructor, and course data.
    export_to_csv()
        Exports the current records to a CSV file.
    search_records()
        Searches for records based on a user query.
    edit_record()
        Edits the selected record in the table.
    delete_record()
        Deletes the selected record from the database.
    """

    def __init__(self):
        """
        Initializes the SchoolManagementSystem GUI.

        Sets up the main window layout, including forms for students, instructors,
        courses, and registration/assignment functions.
        """
        super().__init__()

        # Set window title
        self.setWindowTitle("School Management System")

        # Set window size
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create the main layout
        main_layout = QVBoxLayout()

        # Add Student Form
        student_form = self.create_student_form()
        main_layout.addLayout(student_form)

        # Add Instructor Form
        instructor_form = self.create_instructor_form()
        main_layout.addLayout(instructor_form)

        # Add Course Form
        course_form = self.create_course_form()
        main_layout.addLayout(course_form)

        # Add Student Registration Form
        registration_form = self.create_registration_form()
        main_layout.addLayout(registration_form)

        # Add Instructor Assignment Form
        assignment_form = self.create_assignment_form()
        main_layout.addLayout(assignment_form)

        # Add Search Bar
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by Name or ID")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        self.record_table = QTableWidget()
        self.record_table.setColumnCount(3)
        self.record_table.setHorizontalHeaderLabels(["ID", "Name", "Type"])
        main_layout.addWidget(self.record_table)

        # Add buttons for editing and deleting records
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)

        # Add the buttons to the layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        main_layout.addLayout(button_layout)

        # Add button for exporting data to CSV
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)

        # Add the button to the layout
        button_layout.addWidget(export_button)
        main_layout.addLayout(button_layout)

        # Set the main layout
        central_widget.setLayout(main_layout)

        self.update_student_dropdown()
        self.update_course_dropdown()
        self.update_course_dropdown_for_instructors()
        self.update_instructor_dropdown()
        # Load the initial data from the database
        self.update_table()

    # Function to create the Student Form
    def create_student_form(self):
        """
        Creates the student form layout.

        Returns
        -------
        QFormLayout
            A form layout containing fields for entering student details.
        """

        form_layout = QFormLayout()

        # Create labels and line edits for student form
        student_name_label = QLabel("Student Name:")
        self.student_name_edit = QLineEdit()

        student_id_label = QLabel("Student ID:")
        self.student_id_edit = QLineEdit()

        student_age_label = QLabel("Student Age:")
        self.student_age_edit = QLineEdit()

        # Email for student
        student_email_label = QLabel("Student Email:")
        self.student_email_edit = QLineEdit()

        # Create the button to add student
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)

        # Add the widgets to the form layout
        form_layout.addRow(student_name_label, self.student_name_edit)
        form_layout.addRow(student_id_label, self.student_id_edit)
        form_layout.addRow(student_age_label, self.student_age_edit)
        form_layout.addRow(student_email_label, self.student_email_edit)
        form_layout.addWidget(add_student_button)

        return form_layout

    # Function to create the Instructor Form
    def create_instructor_form(self):
        """
        Creates the instructor form layout.

        Returns
        -------
        QFormLayout
            A form layout containing fields for entering instructor details.
        """
        form_layout = QFormLayout()

        # Create labels and line edits for instructor form
        instructor_name_label = QLabel("Instructor Name:")
        self.instructor_name_edit = QLineEdit()

        instructor_id_label = QLabel("Instructor ID:")
        self.instructor_id_edit = QLineEdit()

        instructor_age_label = QLabel("Instructor Age:")
        self.instructor_age_edit = QLineEdit()

        # Email for instructor
        instructor_email_label = QLabel("Instructor Email:")
        self.instructor_email_edit = QLineEdit()

        # Create the button to add instructor
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)

        # Add the widgets to the form layout
        form_layout.addRow(instructor_id_label, self.instructor_id_edit)
        form_layout.addRow(instructor_name_label, self.instructor_name_edit)
        form_layout.addRow(instructor_age_label, self.instructor_age_edit)
        form_layout.addRow(instructor_email_label, self.instructor_email_edit)
        form_layout.addWidget(add_instructor_button)

        return form_layout

    # Function to create the Course Form
    def create_course_form(self):
        """
        Creates the course form layout.

        Returns
        -------
        QFormLayout
            A form layout containing fields for entering course details.
        """
        form_layout = QFormLayout()

        # Create labels and line edits for course form
        course_id_label = QLabel("Course ID:")
        self.course_id_edit = QLineEdit()  # Input for course ID

        course_name_label = QLabel("Course Name:")
        self.course_name_edit = QLineEdit()  # Input for course name

        # Create the button to add course
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)

        # Add the widgets to the form layout
        form_layout.addRow(course_id_label, self.course_id_edit)
        form_layout.addRow(course_name_label, self.course_name_edit)
        form_layout.addWidget(add_course_button)

        return form_layout

    def create_registration_form(self):
        """
        Creates the form layout for registering a student to a course.

        This method sets up a form that allows the user to register a student for a selected course.
        The form includes:
        - A dropdown to select a student.
        - A dropdown to select a course.
        - A button to confirm the registration, which triggers the `register_student_for_course` method.

        Returns
        -------
        QFormLayout
            A form layout containing the fields and button for registering a student to a course.
        """
        form_layout = QFormLayout()

        # Dropdown to select student
        self.student_dropdown = QComboBox()
        self.student_dropdown.addItem("Select Student")

        # Dropdown to select course
        self.course_dropdown = QComboBox()
        self.course_dropdown.addItem("Select Course")

        # Button to register student for course
        register_button = QPushButton("Register Student for Course")
        register_button.clicked.connect(self.register_student_for_course)

        form_layout.addRow(QLabel("Register Student for Course"))
        form_layout.addRow(QLabel("Select Student:"), self.student_dropdown)
        form_layout.addRow(QLabel("Select Course:"), self.course_dropdown)
        form_layout.addWidget(register_button)

        return form_layout

    # Function to create the Instructor Assignment Form
    def create_assignment_form(self):
        """
        Creates the form layout for assigning an instructor to a course.

        This method sets up a form that allows the user to assign an instructor to a selected course.
        The form includes:
        - A dropdown to select an instructor.
        - A dropdown to select a course.
        - A button to confirm the assignment, which triggers the `assign_instructor_to_course` method.

        Returns
        -------
        QFormLayout
            A form layout containing the fields and button for assigning an instructor to a course.
        """
        form_layout = QFormLayout()

        # Dropdown to select instructor
        self.instructor_dropdown = QComboBox()
        self.instructor_dropdown.addItem("Select Instructor")

        # Dropdown to select course
        self.course_dropdown_for_instructors = QComboBox()
        self.course_dropdown_for_instructors.addItem("Select Course")

        # Button to assign instructor to course
        assign_button = QPushButton("Assign Instructor to Course")
        assign_button.clicked.connect(self.assign_instructor_to_course)

        form_layout.addRow(QLabel("Assign Instructor to Course"))
        form_layout.addRow(QLabel("Select Instructor:"),
                           self.instructor_dropdown)
        form_layout.addRow(QLabel("Select Course:"),
                           self.course_dropdown_for_instructors)
        form_layout.addWidget(assign_button)

        return form_layout

    # Slots for buttons to add Student, Instructor, and Course
    def add_student(self):
        """
        Adds a new student to the database.

        This method validates the student's name, age, ID, and email, ensuring
        that all fields are filled correctly. It also verifies the email format and
        the student's age as a positive integer. If all validations pass, the student
        is added to the database, and the registration is updated.

        Shows a success message upon successful addition or an error message in
        case of invalid input or database issues.
        """
        student_name = self.student_name_edit.text()
        student_id = self.student_id_edit.text()  # Get the student_id
        student_age = self.student_age_edit.text()
        student_email = self.student_email_edit.text()

        # Validate that the fields are not empty
        if not student_name or not student_id or not student_age or not student_email:
            QMessageBox.warning(self, "Input Error",
                                "All fields are required for adding a student.")
            return

        # Validate that the age is a positive integer
        if not student_age.isdigit() or int(student_age) <= 0:
            QMessageBox.warning(self, "Input Error",
                                "Age must be a positive integer.")
            return

        # Validate the email format
        if not self.is_valid_email(student_email):
            QMessageBox.warning(self, "Input Error",
                                "Please enter a valid email address.")
            return

        # Add the student to the database using the function from operations.py
        add_student(student_id, student_name, student_age, student_email)

        # Update the table to reflect changes
        self.update_table()
        self.update_student_dropdown()

        # Clear the input fields after adding
        self.student_name_edit.clear()
        self.student_id_edit.clear()  # Clear the student_id field
        self.student_age_edit.clear()
        self.student_email_edit.clear()

    def add_instructor(self):
        """
        Adds a new instructor to the database.

        This method validates the instructor's name, age, ID, and email, ensuring
        that all fields are filled correctly. It also verifies the email format and
        the instructor's age as a positive integer. If all validations pass, the instructor
        is added to the database.

        Shows a success message upon successful addition or an error message in
        case of invalid input or database issues.
        """
        instructor_name = self.instructor_name_edit.text()
        instructor_id = self.instructor_id_edit.text()  # Get the instructor_id
        instructor_age = self.instructor_age_edit.text()
        instructor_email = self.instructor_email_edit.text()

        # Validate that the fields are not empty
        if not instructor_name or not instructor_id or not instructor_age or not instructor_email:
            QMessageBox.warning(
                self, "Input Error", "All fields are required for adding an instructor.")
            return

        # Validate that the age is a positive integer
        if not instructor_age.isdigit() or int(instructor_age) <= 0:
            QMessageBox.warning(self, "Input Error",
                                "Age must be a positive integer.")
            return

        # Validate the email format
        if not self.is_valid_email(instructor_email):
            QMessageBox.warning(self, "Input Error",
                                "Please enter a valid email address.")
            return

        # Add the instructor to the database using the function from operations.py
        add_instructor(instructor_id, instructor_name,
                       instructor_age, instructor_email)

        # Update the table and dropdowns
        self.update_table()
        self.update_instructor_dropdown()

        # Clear the input fields
        self.instructor_name_edit.clear()
        self.instructor_id_edit.clear()  # Clear the instructor_id field
        self.instructor_age_edit.clear()
        self.instructor_email_edit.clear()

    def update_student_dropdown(self):
        """
        Updates the student dropdown with the latest student names from the database.

        Fetches the current list of students from the database and populates the
        student dropdown with their names, allowing users to select students for
        registration or search purposes.
        """
        # Clear the dropdown
        self.student_dropdown.clear()

        # Add the default item
        self.student_dropdown.addItem("Select Student")

        # Fetch students from the database
        students = get_students()

        # Add each student to the dropdown
        for student in students:
            print(f"Adding student: {student}")  # Debugging print statement
            # Assuming student[2] is the student's name
            self.student_dropdown.addItem(student[2])

    def update_instructor_dropdown(self):
        """
        Updates the instructor dropdown with the latest instructor names from the database.

        Fetches the current list of instructors from the database and populates the
        instructor dropdown with their names, allowing users to select instructors
        for assignment or search purposes.
        """
        # Clear the dropdown
        self.instructor_dropdown.clear()

        # Add the default item
        self.instructor_dropdown.addItem("Select Instructor")

        # Fetch instructors from the database
        instructors = get_instructors()

        # Add each instructor to the dropdown
        for instructor in instructors:
            # Assuming instructor[1] is the instructor name
            self.instructor_dropdown.addItem(instructor[2])

    def add_course(self):
        """
        Adds a new course to the database.

        This method validates the course ID and course name, ensuring that both
        fields are filled correctly. If validation passes, the course is added to the
        database.

        Shows a success message upon successful addition or an error message in
        case of invalid input or database issues.
        """
        course_id = self.course_id_edit.text()  # Get the course_id
        course_name = self.course_name_edit.text()

        # Validate the fields
        if not course_id or not course_name:
            QMessageBox.warning(self, "Input Error",
                                "Both Course ID and Course Name are required.")
            return

        # Add the course to the database
        add_course(course_id, course_name)

        # Update the table and dropdowns
        self.update_table()
        self.update_course_dropdown()
        self.update_course_dropdown_for_instructors()

        # Clear the input fields after adding
        self.course_id_edit.clear()
        self.course_name_edit.clear()

    def update_course_dropdown(self):
        """
        Updates the course dropdown with the latest course names from the database.

        Fetches the current list of courses from the database and populates the
        course dropdown with their names, allowing users to select courses for
        student registration or instructor assignment.
        """
        # Clear the dropdown
        self.course_dropdown.clear()

        # Add the default item
        self.course_dropdown.addItem("Select Course")

        # Fetch courses from the database
        courses = get_courses()

        # Add each course with ID and name to the dropdown
        for course in courses:
            print(f"Adding course: {course}")  # Debugging print statement
            # Show both course_id and course_name
            self.course_dropdown.addItem(f"{course[0]} - {course[2]}")

    def update_course_dropdown_for_instructors(self):
        """
        Updates the course dropdown for instructor assignment.

        This method refreshes the contents of the course dropdown used for assigning
        instructors to courses. It retrieves the list of available courses from the database,
        clears any existing items in the dropdown, and populates it with the updated list.
        Each course is displayed in the format "course_id - course_name" for clarity.

        The method ensures that the dropdown always has a default option "Select Course"
        before adding the list of available courses.

        Returns
        -------
        None
        """
        self.course_dropdown_for_instructors.clear()
        self.course_dropdown_for_instructors.addItem("Select Course")

        courses = get_courses()

        # Add each course with ID and name to the dropdown
        for course in courses:
            print(f"Adding course for instructor assignment: {
                  course}")  # Debugging print statement
            # Format the dropdown item as "course_id - course_name"
            self.course_dropdown_for_instructors.addItem(
                f"{course[0]} - {course[2]}")

    def update_table(self):
        """
        Refreshes the records table to display the latest students, instructors, and courses.

        Fetches data from the database for students, instructors, and courses, and
        updates the table displayed in the user interface. This method ensures that
        the displayed data is up to date.
        """
        self.record_table.setRowCount(0)  # Clear existing rows

        # Fetch students from the database
        students = get_students()
        for student in students:
            row_position = self.record_table.rowCount()
            self.record_table.insertRow(row_position)
            self.record_table.setItem(
                # Student ID (not the primary key)
                row_position, 0, QTableWidgetItem(student[1]))
            self.record_table.setItem(
                row_position, 1, QTableWidgetItem(student[2]))  # Student Name
            self.record_table.setItem(
                # Type (always "Student")
                row_position, 2, QTableWidgetItem("Student"))

        # Fetch instructors from the database
        instructors = get_instructors()
        for instructor in instructors:
            row_position = self.record_table.rowCount()
            self.record_table.insertRow(row_position)
            self.record_table.setItem(row_position, 0, QTableWidgetItem(
                str(instructor[1])))  # Instructor ID
            self.record_table.setItem(row_position, 1, QTableWidgetItem(
                instructor[2]))  # Instructor Name
            self.record_table.setItem(
                row_position, 2, QTableWidgetItem("Instructor"))

        # Fetch courses from the database
        courses = get_courses()
        for course in courses:
            row_position = self.record_table.rowCount()
            self.record_table.insertRow(row_position)
            self.record_table.setItem(
                row_position, 0, QTableWidgetItem(str(course[1])))  # Course ID
            self.record_table.setItem(
                row_position, 1, QTableWidgetItem(course[2]))  # Course Name
            self.record_table.setItem(
                row_position, 2, QTableWidgetItem("Course"))

    def delete_record(self):
        """
        Deletes the selected record from the database.

        Prompts the user for confirmation before deleting the selected record.
        If confirmed, removes the record from the database and refreshes the
        records table.
        """

        selected_row = self.record_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error",
                                "Please select a record to delete.")
            return

        # Get the type (Student, Instructor, or Course)
        record_type = self.record_table.item(selected_row, 2).text()
        # Get the ID of the selected record (Primary Key ID)
        display_id = self.record_table.item(selected_row, 0).text()

        # Fetch the actual primary key `id` for deletion
        if record_type == "Student":
            students = get_students()
            # Match the displayed student_id with the database's actual primary key `id`
            student_record = next(
                (s for s in students if str(s[1]) == display_id), None)
            if student_record:
                # Pass the actual primary key `id`
                delete_student(student_record[0])
        elif record_type == "Instructor":
            instructors = get_instructors()
            # Match the displayed instructor_id with the database's actual primary key `id`
            instructor_record = next(
                (i for i in instructors if str(i[1]) == display_id), None)
            if instructor_record:
                # Pass the actual primary key `id`
                delete_instructor(instructor_record[0])
        elif record_type == "Course":
            courses = get_courses()
            # Match the displayed course_code with the database's actual primary key `id`
            course_record = next(
                (c for c in courses if str(c[1]) == display_id), None)
            if course_record:
                # Pass the actual primary key `id`
                delete_course(course_record[0])

        # Update the table to reflect the changes
        self.update_table()

        # Show success message
        QMessageBox.information(
            self, "Success", f"{record_type} deleted successfully.")

    def export_to_csv(self):
        """
        Exports the records of students, instructors, and courses to a CSV file.

        Prompts the user to select a file location for saving the exported data,
        and writes the student, instructor, and course records to the specified
        CSV file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "", "CSV Files (*.csv)", options=options)

        if file_name:
            if not file_name.endswith(".csv"):
                file_name += ".csv"

            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Name', 'Type'])

                # Write students
                students = get_students()
                for student in students:
                    writer.writerow([student[0], student[1], 'Student'])

                # Write instructors
                instructors = get_instructors()
                for instructor in instructors:
                    writer.writerow(
                        [instructor[0], instructor[1], 'Instructor'])

                # Write courses
                courses = get_courses()
                for course in courses:
                    writer.writerow([course[0], course[1], 'Course'])

            QMessageBox.information(
                self, "Success", "Data exported to CSV successfully!")

    def is_valid_email(self, email):
        """
        Validates the format of an email address using a regular expression.

        This method checks if the provided email matches a standard email format
        using a regular expression pattern. It supports common email formats
        including alphanumeric characters, dots, underscores, and domain names.

        Parameters
        ----------
        email : str
            The email address to be validated.

        Returns
        -------
        bool
            Returns True if the email matches the valid format, otherwise False.
        """
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    def assign_instructor_to_course(self):
        """
        Assigns an instructor to a selected course based on user input.

        This method retrieves the selected instructor and course from the dropdown menus.
        It extracts the course ID and name, fetches the list of instructors and courses
        from the database, and matches the selected instructor and course with their IDs.
        If both the instructor and course are valid, it calls the `assign_instructor`
        function to link the instructor to the course in the database.

        If an invalid selection is made or if there is an error in the process, it displays
        an appropriate warning message to the user.

        Returns
        -------
        None
        """
        instructor_name = self.instructor_dropdown.currentText()
        course_info = self.course_dropdown_for_instructors.currentText()

        print(f"Selected instructor: {instructor_name}")
        print(f"Selected course: {course_info}")

        if instructor_name != "Select Instructor" and course_info != "Select Course":
            # Extract course_id and course_name from course_info
            try:
                course_id, course_name = course_info.split(' - ')
                print(f"Split course_id: {
                      course_id}, course_name: {course_name}")
            except ValueError:
                print("Error splitting course info")
                QMessageBox.warning(self, "Selection Error",
                                    "Course selection is incorrect")
                return

            # Fetch instructor and course IDs from the database
            instructors = get_instructors()
            courses = get_courses()

            print(f"Fetched instructors: {instructors}")
            print(f"Fetched courses: {courses}")

            # Find the instructor_id by matching the instructor name
            instructor_id = next(
                (i[0] for i in instructors if i[2] == instructor_name), None)

            # Find the course_id by matching the course code
            found_course_id = next(
                (c[0] for c in courses if c[0] == int(course_id)), None)

            print(f"Found instructor_id: {instructor_id}")
            print(f"Found course_id: {found_course_id}")

            if instructor_id and found_course_id:
                # Call the function to assign instructor to course
                assign_instructor(instructor_id, found_course_id)
                QMessageBox.information(self, "Success", f"Assigned {
                                        instructor_name} to {course_name}")
            else:
                QMessageBox.warning(self, "Selection Error",
                                    "Invalid instructor or course selection")
        else:
            QMessageBox.warning(self, "Selection Error",
                                "Please select both an instructor and a course")

    def register_student_for_course(self):
        """
        Registers a selected student for a selected course.

        This method retrieves the selected student and course from the respective dropdowns
        and attempts to register the student for the specified course. It performs validation
        to ensure that valid selections are made, extracts the course ID, and checks for the existence
        of the student and course in the database before proceeding with the registration.

        If the registration is successful, a confirmation message is displayed. In the case of an error
        during the selection or registration process, appropriate warning messages are shown.

        Returns
        -------
        None
        """
        student_name = self.student_dropdown.currentText()  # Get the selected student name
        # Get the selected course info (course_id - course_name)
        course_info = self.course_dropdown.currentText()

        print(f"Selected student: {student_name}")
        print(f"Selected course: {course_info}")

        if student_name != "Select Student" and course_info != "Select Course":
            try:
                # Extract course_id and course_name from course_info (format: 'course_id - course_name')
                course_id, course_name = course_info.split(' - ')
                print(f"Split course_id: {
                      course_id}, course_name: {course_name}")
            except ValueError:
                print("Error splitting course info")
                QMessageBox.warning(self, "Selection Error",
                                    "Course selection is incorrect")
                return

            # Get students and courses from the database
            students = get_students()
            courses = get_courses()

            print(f"Fetched students: {students}")
            print(f"Fetched courses: {courses}")

            # Find the student_id by matching the student name
            student_id = next(
                (s[0] for s in students if s[2] == student_name), None)

            # Find the course_id by matching the extracted course_id
            found_course_id = next(
                (c[0] for c in courses if str(c[0]) == course_id), None)

            print(f"Found student_id: {student_id}")
            print(f"Found course_id: {found_course_id}")

            if student_id and found_course_id:
                enroll_student(student_id, found_course_id)
                QMessageBox.information(self, "Success", f"Registered {
                                        student_name} for {course_name}")
            else:
                print("Invalid student or course selection")
                QMessageBox.warning(self, "Selection Error",
                                    "Invalid student or course selection")
        else:
            QMessageBox.warning(self, "Selection Error",
                                "Please select both a student and a course")

    def search_records(self):
        """
        Searches for records in the database based on the user input and selected criteria.

        Retrieves records of students, instructors, or courses that match the search
        query entered by the user. Updates the records table to display the filtered
        results.
        """
        search_query = self.search_edit.text().lower()

        # Clear the table for filtered results
        self.record_table.setRowCount(0)

        # Search in students
        students = get_students()  # Fetch students from the database
        for student in students:
            # student[2] is the name
            if search_query in student[2].lower() or search_query in str(student[1]):
                row_position = self.record_table.rowCount()
                self.record_table.insertRow(row_position)
                self.record_table.setItem(
                    # Student ID
                    row_position, 0, QTableWidgetItem(str(student[1])))
                self.record_table.setItem(
                    # Student Name
                    row_position, 1, QTableWidgetItem(student[2]))
                self.record_table.setItem(
                    # Type: Student
                    row_position, 2, QTableWidgetItem("Student"))

        # Search in instructors
        instructors = get_instructors()  # Fetch instructors from the database
        for instructor in instructors:
            # instructor[2] is the name
            if search_query in instructor[2].lower() or search_query in str(instructor[1]):
                row_position = self.record_table.rowCount()
                self.record_table.insertRow(row_position)
                self.record_table.setItem(
                    # Instructor ID
                    row_position, 0, QTableWidgetItem(str(instructor[1])))
                self.record_table.setItem(
                    # Instructor Name
                    row_position, 1, QTableWidgetItem(instructor[2]))
                self.record_table.setItem(
                    # Type: Instructor
                    row_position, 2, QTableWidgetItem("Instructor"))

        # Search in courses
        courses = get_courses()  # Fetch courses from the database
        for course in courses:
            # course[2] is the course name
            if search_query in course[2].lower() or search_query in str(course[1]):
                row_position = self.record_table.rowCount()
                self.record_table.insertRow(row_position)
                self.record_table.setItem(
                    # Course Code
                    row_position, 0, QTableWidgetItem(str(course[1])))
                self.record_table.setItem(
                    # Course Name
                    row_position, 1, QTableWidgetItem(course[2]))
                self.record_table.setItem(
                    # Type: Course
                    row_position, 2, QTableWidgetItem("Course"))

    def edit_record(self):
        """
        Allows the user to edit the selected record in the table.

        Populates the form with the existing details of the selected record,
        allowing the user to modify the information. Saves the updated record to
        the database upon submission.
        """
        # Get the selected row
        selected_row = self.record_table.currentRow()

        # Check if a row is selected
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error",
                                "Please select a record to edit.")
            return

        # Get the type (Student, Instructor, or Course)
        record_type = self.record_table.item(selected_row, 2).text()
        # Get the ID (or displayed ID like student_id, instructor_id) of the selected record
        display_id = self.record_table.item(selected_row, 0).text()

        if record_type == "Student":
            students = get_students()
            student = next(
                (s for s in students if str(s[1]) == display_id), None)
            if student:
                # Populate the form fields with the student details
                self.student_id_edit.setText(student[1])
                self.student_name_edit.setText(student[2])
                self.student_age_edit.setText(str(student[3]))
                self.student_email_edit.setText(student[4])

                # When the user clicks "Add Student" again, update instead of adding a new one
                self.delete_student_record_before_update(student[0])

        elif record_type == "Instructor":
            instructors = get_instructors()
            instructor = next(
                (i for i in instructors if str(i[1]) == display_id), None)
            if instructor:
                # Populate the form fields with the instructor details
                self.instructor_id_edit.setText(instructor[1])
                self.instructor_name_edit.setText(instructor[2])
                self.instructor_age_edit.setText(str(instructor[3]))
                self.instructor_email_edit.setText(instructor[4])

                # When the user clicks "Add Instructor" again, update instead of adding a new one
                self.delete_instructor_record_before_update(instructor[0])

        elif record_type == "Course":
            courses = get_courses()
            course = next(
                (c for c in courses if str(c[1]) == display_id), None)
            if course:
                # Populate the form fields with the course details
                self.course_id_edit.setText(course[1])
                self.course_name_edit.setText(course[2])

                # When the user clicks "Add Course" again, update instead of adding a new one
                self.delete_course_record_before_update(course[0])

        # Update the table to reflect the changes
        self.update_table()

    def delete_student_record_before_update(self, student_id):
        delete_student(student_id)

    def delete_instructor_record_before_update(self, instructor_id):
        delete_instructor(instructor_id)

    def delete_course_record_before_update(self, course_id):
        delete_course(course_id)


# Main function to run the PyQt5 application


def main():
    """
    The main function to run the School Management System PyQt5 application.

    Creates an instance of QApplication and SchoolManagementSystem,
    then starts the application's event loop.
    """
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
