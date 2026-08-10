import json


def calculate_average(subjects):
    """Calculate the average grade."""
    return sum(subjects.values()) / len(subjects)


def get_letter_grade(average):
    """Return letter grade based on average."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def get_highest_grade(subjects):
    """Return subject and grade with the highest score."""
    subject = max(subjects, key=subjects.get)
    return subject, subjects[subject]


def get_lowest_grade(subjects):
    """Return subject and grade with the lowest score."""
    subject = min(subjects, key=subjects.get)
    return subject, subjects[subject]


def save_grade_data(student_name, subjects):
    """Save student data to a JSON file."""
    filename = student_name.replace(" ", "_") + "_grades.json"

    data = {
        "student_name": student_name,
        "subjects": subjects
    }

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"✅ Grade data saved successfully as: {filename}")

    except OSError:
        print("❌ Could not save the file.")


def load_grade_data(student_name):
    """Load student data from a JSON file."""
    filename = student_name.replace(" ", "_") + "_grades.json"

    try:
        with open(filename, "r") as file:
            data = json.load(file)

        print(f"✅ Grade data loaded successfully from: {filename}")

        return data["student_name"], data["subjects"]

    except FileNotFoundError:
        print(f"❌ No saved grade data found for {student_name}.")

    except (json.JSONDecodeError, KeyError):
        print("❌ The saved grade file is invalid.")

    return student_name, {}


def save_text_report(student_name, subjects):
    """Save a formatted grade report to a text file."""
    average = calculate_average(subjects)

    highest_subject, highest_grade = get_highest_grade(subjects)
    lowest_subject, lowest_grade = get_lowest_grade(subjects)

    letter = get_letter_grade(average)
    status = "PASS" if average >= 50 else "FAIL"

    filename = student_name.replace(" ", "_") + "_grade_report.txt"

    try:
        with open(filename, "w") as file:
            file.write("========================================\n")
            file.write("           STUDENT GRADE REPORT\n")
            file.write("========================================\n")
            file.write(f"Student: {student_name}\n")
            file.write(f"Number of Subjects: {len(subjects)}\n")
            file.write("----------------------------------------\n")

            for subject, grade in subjects.items():
                file.write(f"{subject}: {grade:.2f}\n")

            file.write("----------------------------------------\n")
            file.write(f"Average Grade: {average:.2f}\n")
            file.write(
                f"Highest Grade: {highest_subject} "
                f"({highest_grade:.2f})\n"
            )
            file.write(
                f"Lowest Grade: {lowest_subject} "
                f"({lowest_grade:.2f})\n"
            )
            file.write(f"Overall Grade: {letter}\n")
            file.write(f"Status: {status}\n")
            file.write("========================================\n")

        print(f"✅ Text report saved as: {filename}")

    except OSError:
        print("❌ Could not save the report.")


def show_grade_report(student_name, subjects):
    """Display the complete grade report."""
    average = calculate_average(subjects)

    highest_subject, highest_grade = get_highest_grade(subjects)
    lowest_subject, lowest_grade = get_lowest_grade(subjects)

    letter = get_letter_grade(average)
    status = "PASS" if average >= 50 else "FAIL"

    print("\n========================================")
    print("           STUDENT GRADE REPORT")
    print("========================================")
    print(f"Student: {student_name}")
    print(f"Number of Subjects: {len(subjects)}")
    print("----------------------------------------")

    for subject, grade in subjects.items():
        print(f"{subject}: {grade:.2f}")

    print("----------------------------------------")
    print(f"Average Grade: {average:.2f}")
    print(f"Highest Grade: {highest_subject} ({highest_grade:.2f})")
    print(f"Lowest Grade: {lowest_subject} ({lowest_grade:.2f})")
    print(f"Overall Grade: {letter}")
    print(f"Status: {status}")
    print("========================================")


# ----------------------------------------
# MAIN PROGRAM
# ----------------------------------------

print("========================================")
print("       STUDENT GRADE TRACKER")
print("========================================")

student_name = input("Enter student name: ").strip()

subjects = {}

while True:

    print("\n========================================")
    print("                 MENU")
    print("========================================")
    print("1. Add Subject & Grade")
    print("2. View Grades")
    print("3. Calculate Average")
    print("4. Show Grade Report")
    print("5. Save Grade Data")
    print("6. Load Grade Data")
    print("7. Save Text Report")
    print("8. Exit")
    print("========================================")

    choice = input("Enter your choice: ").strip()

    # ------------------------------------
    # 1. Add Subject & Grade
    # ------------------------------------

    if choice == "1":

        subject = input("Enter subject name: ").strip()

        if subject == "":
            print("❌ Subject name cannot be empty.")
            continue

        try:
            grade = float(input(f"Enter grade for {subject}: "))

            if grade < 0 or grade > 100:
                print("❌ Grade must be between 0 and 100.")
            else:
                subjects[subject] = grade
                print("✅ Grade added successfully!")

        except ValueError:
            print("❌ Please enter a valid number.")

    # ------------------------------------
    # 2. View Grades
    # ------------------------------------

    elif choice == "2":

        if not subjects:
            print("❌ No grades have been added yet.")

        else:
            print("\n----------- GRADES -----------")

            for subject, grade in subjects.items():
                print(f"{subject}: {grade:.2f}")

    # ------------------------------------
    # 3. Calculate Average
    # ------------------------------------

    elif choice == "3":

        if not subjects:
            print("❌ No grades available.")

        else:
            average = calculate_average(subjects)
            print(f"\n📊 Average Grade: {average:.2f}")

    # ------------------------------------
    # 4. Show Grade Report
    # ------------------------------------

    elif choice == "4":

        if not subjects:
            print("❌ No grades available.")

        else:
            show_grade_report(student_name, subjects)

    # ------------------------------------
    # 5. Save Grade Data
    # ------------------------------------

    elif choice == "5":

        if not subjects:
            print("❌ No grades available to save.")

        else:
            save_grade_data(student_name, subjects)

    # ------------------------------------
    # 6. Load Grade Data
    # ------------------------------------

    elif choice == "6":

        student_name, loaded_subjects = load_grade_data(
            student_name
        )

        if loaded_subjects:
            subjects = loaded_subjects

    # ------------------------------------
    # 7. Save Text Report
    # ------------------------------------

    elif choice == "7":

        if not subjects:
            print("❌ No grades available to save.")

        else:
            save_text_report(student_name, subjects)

    # ------------------------------------
    # 8. Exit
    # ------------------------------------

    elif choice == "8":

        print("\nThank you for using Student Grade Tracker!")
        print("Program finished.")
        break

    else:
        print("❌ Invalid choice. Please select 1-8.")