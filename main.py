from student_system.manager import (
    register_student,
    update_grades,
    get_top_students,
    delete_student,
    list_all_students,
)


from student_system.exporter import (
    export_to_json,
    export_to_csv,
)

from student_system.utils import load_students
from student_system.validators import StudentSystemError


def run():
    while True:
        print("\n===== Student Management System =====")
        print("1 - Register a new student")
        print("2 - Update student grades")
        print("3 - List top 3 students")
        print("4 - List all students")
        print("5 - Export to JSON")
        print("6 - Export to CSV")
        print("7 - Delete a student")
        print("0 - Quit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                name = input("Name: ")
                student_id = input("Student ID: ")
                email = input("Email: ")

                grades = list(
                    map(
                        float,
                        input("Grades (comma separated): ").split(","),
                    )
                )

                register_student(name, student_id, email, grades)
                print("Student registered successfully.")

            elif choice == "2":
                student_id = input("Student ID: ")

                grades = list(
                    map(
                        float,
                        input("New grades (comma separated): ").split(","),
                    )
                )

                update_grades(student_id, grades)
                print("Grades updated successfully.")

            elif choice == "3":
                top_students = get_top_students()

                print("\nTop Students")
                for name, student_id, average in top_students:
                    print(f"{name} ({student_id}) - Average: {average}")

            elif choice == "4":
                students = list_all_students()

                print()
                for student in students:
                    print(student)

            elif choice == "5":
                filepath = input("Export JSON file path: ")
                export_to_json(load_students("students.json"), filepath)
                print("Export completed.")

            elif choice == "6":
                filepath = input("Export CSV file path: ")
                export_to_csv(load_students("students.json"), filepath)
                print("Export completed.")

            elif choice == "7":
                student_id = input("Student ID: ")
                delete_student(student_id)
                print("Student deleted successfully.")

            elif choice == "0":
                break

            else:
                print("Invalid option.")

        except StudentSystemError as error:
            print(f"Error: {error}")

    print("Goodbye!")


if __name__ == "__main__":
    try:
        run()
    finally:
        print("Thank you for using the Student Management System.")
