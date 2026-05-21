import pandas as pd
import numpy as np
from database import get_all_students_df
from models import Section

DISPLAY_COLUMNS = ["student_number", "name", "prelims", "lab_act1", "lab_act2",
                   "midterms", "semestral_project", "finals", "final_grade"]

COLUMN_LABELS = {
    "student_number":    "#",
    "name":              "Name",
    "prelims":           "Prelims",
    "lab_act1":          "Lab Act 1",
    "lab_act2":          "Lab Act 2",
    "midterms":          "Midterms",
    "semestral_project": "Semestral Project",
    "finals":            "Finals",
    "final_grade":       "Final Grade",
}

def format_score(value):
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "No score"
    return f"{value:.2f}"

def display_single_student(section: Section):
    students = section.get_students()
    if not students:
        print("  No students found in this section.")
        return

    student_number = input("\n  Enter student number: ").strip()
    student = section.get_student_by_number(student_number)

    if not student:
        print("  Student not found.")
        return

    grades = student.get_grades()
    if not grades:
        print("  No grade record found.")
        return

    print(f"\n  Student {student.student_number} - {student.name}")
    print(f"  {'-'*40}")

    fields = ["prelims", "lab_act1", "lab_act2",
              "midterms", "semestral_project", "finals", "final_grade"]

    for field in fields:
        label = COLUMN_LABELS[field]
        value = grades.data.get(field)
        print(f"  {label:<20}: {format_score(value)}")

def display_all_students(section: Section):
    df = get_all_students_df(section.section_id)

    if df.empty:
        print("  No students found in this section.")
        return