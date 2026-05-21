import pandas as pd
import numpy as np
from database import get_all_students_df
from models import Section

COMPLIANCE_FIELDS = ["prelims", "lab_act1", "lab_act2",
                     "midterms", "semestral_project", "finals", "final_grade"]

COMPLIANCE_LABELS = {
    "prelims":           "Prelims",
    "lab_act1":          "Lab Act 1",
    "lab_act2":          "Lab Act 2",
    "midterms":          "Midterms",
    "semestral_project": "Semestral Project",
    "finals":            "Finals",
    "final_grade":       "Final Grade",
}

COMPLIANCE_MENU = """
    Which one do you want to check for missing compliance?
    1. Prelims
    2. Lab Act 1
    3. Lab Act 2
    4. Midterms
    5. Semestral Project
    6. Finals
    7. Final Grade
"""

def pick_compliance_field():
    print(COMPLIANCE_MENU)
    while True:
        choice = input("    Enter choice: ").strip()
        if choice in [str(i) for i in range(1, 8)]:
            return COMPLIANCE_FIELDS[int(choice) - 1]
        print("    Invalid choice. Please enter a number from 1 to 7.")

def display_missing(df: pd.DataFrame, field: str):
    label = COMPLIANCE_LABELS[field]

    # use numpy to find rows where the field is NaN/null
    scores  = df[field].to_numpy()
    missing_mask = pd.isna(df[field]).to_numpy()
    missing_df   = df[missing_mask][["student_number", "name"]].reset_index(drop=True)

    total   = len(df)
    missing = int(np.sum(missing_mask))
    present = total - missing

    print(f"\n  Missing Compliance Report — {label}")
    print(f"  {'-'*40}")
    print(f"  Total students : {total}")
    print(f"  Submitted      : {present}")
    print(f"  Missing        : {missing}")
    print(f"  {'-'*40}")

    if missing_df.empty:
        print(f"\n  All students have submitted {label}.")
    else:
        print(f"\n  Students with no score in {label}:\n")
        print(f"  {'#':<6} {'Name':<25}")
        print(f"  {'-'*6} {'-'*25}")
        for _, row in missing_df.iterrows():
            print(f"  {row['student_number']:<6} {row['name']:<25}")

def missing_compliance(section: Section):
    print("\n  [Missing Compliance]")

    df = get_all_students_df(section.section_id)
    if df.empty:
        print("  No students found in this section.")
        return

    field = pick_compliance_field()
    display_missing(df, field)