Student Grade Tracker

A Python-based Student Grade Tracker developed as part of the Rhombix Technologies Python Development Internship.

📌 Project Overview

The Student Grade Tracker is a console-based Python application that allows users to enter student grades for different subjects, calculate the average grade, generate a complete grade report, and save student data for future use.

The project demonstrates fundamental and practical Python programming concepts including dictionaries, functions, loops, conditional statements, input validation, file handling, and JSON data storage.

✨ Features

- Add subjects and grades
- Validate grades between 0 and 100
- View all entered grades
- Calculate the average grade
- Determine the highest grade
- Determine the lowest grade
- Calculate the overall letter grade
- Display PASS/FAIL status
- Generate a complete student grade report
- Save student data in JSON format
- Load previously saved student data
- Save a formatted text report
- User-friendly menu system
- Handles invalid input

🛠️ Technologies Used

- Python 3
- JSON
- File Handling
- Dictionaries
- Functions
- Loops
- Conditional Statements
- Exception Handling

📂 Project Structure

Student-Grade-Tracker/
│
├── student_grade_tracker.py
└── README.md

The program automatically creates JSON and text report files when the corresponding options are selected.

▶️ How to Run

1. Install Python

Make sure Python 3 is installed on your device.

2. Run the program

Open a terminal in the project directory and run:

python student_grade_tracker.py

If you are using Pydroid 3, simply open "student_grade_tracker.py" and press the Run button.

📋 Menu Options

1. Add Subject & Grade
2. View Grades
3. Calculate Average
4. Show Grade Report
5. Save Grade Data
6. Load Grade Data
7. Save Text Report
8. Exit

📊 Example

========================================
           STUDENT GRADE REPORT
========================================
Student: Muneeb
Number of Subjects: 6
----------------------------------------
Math: 99.00
English: 90.00
Circuit: 95.00
Programming: 98.00
Electronics: 93.00
Ethics: 100.00
----------------------------------------
Average Grade: 95.83
Highest Grade: Ethics (100.00)
Lowest Grade: English (90.00)
Overall Grade: A
Status: PASS
========================================

💾 Data Storage

The application uses JSON to store student information and grades.

Example:

Muneeb_grades.json

A formatted report can also be saved as:

Muneeb_grade_report.txt

These files are generated automatically by the program.

🎓 Internship Task

Organization: Rhombix Technologies
Domain: Python Development
Task: Student Grade Tracker

This project was developed as part of the Rhombix Technologies Python Development Internship.

👨‍💻 Author

Muneeb Dawar

Python Development Intern

🚀 Future Improvements

Possible future improvements include:

- Support for multiple students
- Student search functionality
- Delete or edit grades
- Graphical user interface
- Database integration
- Export reports to PDF
- More advanced grading systems
