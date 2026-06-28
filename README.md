# internship_day6_project
# Student Management System

## Description

This project is a command-line Student Management System written in Python. It allows users to manage student records stored in a JSON file.

Features include:

* Register a new student
* Update student grades
* Delete a student
* View a student's information
* List all students
* Display the top students based on average grade
* Export student data to JSON or CSV

---

## Install Dependencies

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

**Linux/macOS**

```bash
source .venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the Program

From the project root, run:

```bash
python main.py
```

---

## Run the Tests

Run all tests with:

```bash
pytest
```

To check formatting and linting:

```bash
black .
flake8 .
```
