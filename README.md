# Lab 4 - Ahmad Dimashkie & Saja Borghol

## Project Description

This project is a combined implementation of two separate GUI frameworks: Tkinter and PyQt. It showcases both graphical user interfaces (GUIs) with individual functionalities, and their integration into a single cohesive system. This project was completed as part of **EECE 435L**, in collaboration between Ahmad Dimashkie and Saja Borghol.

## Features

- **Tkinter Interface**: A simple school management system implemented using Tkinter. The system allows users to:
  - Add, edit, and delete students, instructors, and courses.
  - Search for students or instructors based on name, ID, or course.
  - Backup the database to a JSON file.

- **PyQt Interface**: A graphical user interface built using PyQt (specific functionalities for this will be added by Saja Borghol).

- **Integration**: Both Tkinter and PyQt UIs are integrated to allow smooth interaction between both interfaces.

## Repository Structure

The repository contains two main branches:
- **`feature-tkinter`**: Contains the implementation of the Tkinter interface by Ahmad Dimashkie.
- **`feature-pyqt`**: Contains the implementation of the PyQt interface by Saja Borghol.

Each branch contains the relevant UI files and code for the respective parts.

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.x**
- **Pip** for installing dependencies
- **Tkinter** (usually comes pre-installed with Python)
- **PyQt5** (can be installed via pip)

To install PyQt5, run:
```bash
pip install PyQt5 pscopg2 sphinx sphinx_rtd_theme
```

### Cloning the Repository

To clone this repository to your local machine, run:
```bash
git clone https://github.com/Ahmad-Dimashkie/Lab4-AhmadDimashkie_SajaBorghol.git
```

### Running the Project

To run the Tkinter-based school management system:
1. Navigate to the Tkinter folder in the cloned repository.
2. Execute the following command after installing the required libraries:
   ```bash
   python tkinter_school_management.py
   ```

To run the PyQt interface (once added by Saja Borghol):
1. Navigate to the PyQt folder in the cloned repository.
2. Execute the following command:
   ```bash
   python pyqt_interface.py
   ```

## Collaboration and Branching

This project uses a branching strategy for collaboration:
- **Tkinter** development is handled in the `feature-tkinter` branch.
- **PyQt** development is handled in the `feature-pyqt` branch.

Both branches will eventually be merged into the `main` branch after code review and resolving any potential conflicts.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project is part of **EECE 435L** coursework at the **American University of Beirut**.
