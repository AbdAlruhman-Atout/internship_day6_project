import csv
import json
import pytest

from student_system import manager
from student_system.exporter import export_to_csv, export_to_json
from student_system.validators import (
    DuplicateStudentError,
    InvalidEmailError,
    InvalidGradeError,
    StudentNotFoundError,
    StudentSystemError,
    validate_student,
)


@pytest.fixture
def sample_students():
    return {
        "1001": {
            "name": "Alice",
            "email": "alice@example.com",
            "grades": [90, 95, 100],
        },
        "1002": {
            "name": "Bob",
            "email": "bob@example.com",
            "grades": [70, 75, 80],
        },
    }


@pytest.fixture
def fake_storage(monkeypatch, sample_students):
    storage = {}

    for student_id, details in sample_students.items():
        storage[student_id] = details.copy()

    def fake_load(filepath):
        return storage

    def fake_save(students, filepath):
        storage.update(students)

    monkeypatch.setattr(manager, "load_students", fake_load)
    monkeypatch.setattr(manager, "export_to_json", fake_save)

    return storage


def test_register_student(fake_storage):
    manager.register_student(
        "Carol",
        "1003",
        "carol@example.com",
        [88, 90, 92],
    )

    assert "1003" in fake_storage


def test_register_duplicate_raises(fake_storage):
    with pytest.raises(DuplicateStudentError):
        manager.register_student(
            "Alice",
            "1001",
            "alice@example.com",
            [90],
        )


def test_register_invalid_email_raises(fake_storage):
    with pytest.raises(InvalidEmailError):
        manager.register_student(
            "Bad Email",
            "1004",
            "bad-email",
            [90],
        )


def test_register_invalid_grade_raises(fake_storage):
    with pytest.raises(InvalidGradeError):
        manager.register_student(
            "Bad Grade",
            "1005",
            "grade@example.com",
            [101],
        )


def test_update_grades(fake_storage):
    manager.update_grades("1001", [60, 70, 80])

    assert fake_storage["1001"]["grades"] == [60, 70, 80]


def test_update_missing_raises(fake_storage):
    with pytest.raises(StudentNotFoundError):
        manager.update_grades("9999", [80, 90])


def test_get_top_students_order(fake_storage):
    result = manager.get_top_students()

    assert result[0][0] == "Alice"


def test_get_top_students_count(fake_storage):
    result = manager.get_top_students(n=1)

    assert len(result) == 1


def test_delete_student(fake_storage):
    manager.delete_student("1001")

    assert "1001" not in fake_storage


def test_delete_missing_raises(fake_storage):
    with pytest.raises(StudentNotFoundError):
        manager.delete_student("9999")


def test_list_all_sorted(fake_storage):
    result = manager.list_all_students()

    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"


def test_export_to_json(tmp_path, sample_students):
    filepath = tmp_path / "students_export.json"

    export_to_json(sample_students, filepath)

    assert filepath.exists()

    with open(filepath, "r") as file:
        data = json.load(file)

    assert data == sample_students


def test_export_to_csv(tmp_path, sample_students):
    filepath = tmp_path / "students_export.csv"

    export_to_csv(sample_students, filepath)

    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert reader.fieldnames == [
        "name",
        "student_id",
        "email",
        "average_grade",
    ]
    assert len(rows) == 2


def test_validate_student_passes():
    validate_student(
        "Alice",
        "1001",
        "alice@example.com",
        [80, 90, 100],
    )


def test_custom_exception_hierarchy():
    assert issubclass(DuplicateStudentError, StudentSystemError)
    assert issubclass(StudentNotFoundError, StudentSystemError)
    assert issubclass(InvalidGradeError, StudentSystemError)
    assert issubclass(InvalidEmailError, StudentSystemError)
