from student_system.exporter import export_to_json
from student_system.utils import load_students
from student_system.validators import (
    validate_student,
    DuplicateStudentError,
    StudentNotFoundError,
    InvalidGradeError,
)


def register_student(name, student_id, email, grades):

    students = load_students("student_system/students.json")

    if student_id in students:
        raise DuplicateStudentError(f"{name} already exists")

    validate_student(name, student_id, email, grades)

    students[student_id] = {
        "name": name,
        "email": email,
        "grades": grades,
    }

    export_to_json(students, "student_system/students.json")


def update_grades(student_id, new_grades):
    students = load_students("student_system/students.json")
    if student_id not in students:
        raise StudentNotFoundError(f"{student_id} not found")

    if any(grade < 0 or grade > 100 for grade in new_grades):
        raise InvalidGradeError("invalid grade list")

    students[student_id]["grades"] = new_grades

    export_to_json(students, "student_system/students.json")



def get_top_students(n=3):
    students = load_students("student_system/students.json")
    students_list = []
    for key, details in students.items():
        average = round(sum(details["grades"]) / len(details["grades"]), 2)
        students_list.append((details["name"], key, average))

    return sorted(students_list, key=lambda x: x[2], reverse=True)[:n]


def delete_student(student_id):
    students = load_students("student_system/students.json")

    if student_id not in students:
        raise StudentNotFoundError(f"{student_id} not found")

    del students[student_id]

    export_to_json(students, "student_system/students.json")


def get_student(student_id):
    students = load_students("student_system/students.json")

    if student_id not in students:
        raise StudentNotFoundError(f"{student_id} not found")

    return students[student_id]


def list_all_students():
    students = load_students("student_system/students.json")

    students_list = []

    for student_id, details in students.items():
        students_list.append(
            {
                "student_id": student_id,
                "name": details["name"],
                "email": details["email"],
                "grades": details["grades"],
            }
        )

    return sorted(students_list, key=lambda student: student["name"])
