import re

EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


class StudentSystemError(Exception):
    pass


class StudentNotFoundError(StudentSystemError):
    pass


class DuplicateStudentError(StudentSystemError):
    pass


class InvalidGradeError(StudentSystemError):
    pass


class InvalidEmailError(StudentSystemError):
    pass


def validate_student(name, student_id, email, grades):
    if not re.fullmatch(EMAIL_PATTERN, email):
        raise InvalidEmailError(f"{email} is invalid")

    if any(grade < 0 or grade > 100 for grade in grades):
        raise InvalidGradeError("invalid grade list")
