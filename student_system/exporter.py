import json
import csv


def export_to_json(students, filepath):
    with open(
        filepath,
        "w",
    ) as file:
        json.dump(students, file, indent=2)


def export_to_csv(students, filepath):
    with open(filepath, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["name", "student_id", "email", "average_grade"],
        )

        writer.writeheader()

        for student_id, details in students.items():
            average = round(sum(details["grades"]) / len(details["grades"]), 2)

            writer.writerow(
                {
                    "name": details["name"],
                    "student_id": student_id,
                    "email": details["email"],
                    "average_grade": average,
                }
            )
