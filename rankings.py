import pandas as pd
import numpy as np
from database import get_all_students_df
from models import Section

RANK_FIELDS = ["prelims", "lab_act1", "lab_act2", "midterms", "semestral_project", "finals", "final_grade"]
RANK_LABELS = {
    "prelims":           "Prelims",
    "lab_act1":          "Lab Act 1",
    "lab_act2":          "Lab Act 2",
    "midterms":          "Midterms",
    "semestral_project": "Semestral Project",
    "finals":            "Finals",
    "final_grade":       "Final Grade",
}

RANK_MENU = """
    Which one do you want to rank?
    1. Prelims
    2. Lab Act 1
    3. Lab Act 2
    4. Midterms
    5. Semestral Project
    6. Finals
    7. Final Grade
"""

def pick_rank_field():
    print(RANK_MENU)
    while True:
        choice = input("    Enter choice: ").strip()
        if choice in [str(i) for i in range(1, 8)]:
            return RANK_FIELDS[int(choice) - 1]
        print("    Invalid choice. Please enter a number from 1 to 7.")

def display_ranking(df: pd.DataFrame, field: str):
    label = RANK_LABELS[field]

    # keep only rows that have a score for this field
    ranked = df[["name", field]].copy()
    ranked = ranked[ranked[field].notna()]

    if ranked.empty:
        print(f"\n  No scores recorded for {label} yet.")
        return

    # sort descending using numpy argsort
    scores = ranked[field].to_numpy()
    sorted_indices = np.argsort(-scores)  # descending
    ranked = ranked.iloc[sorted_indices].reset_index(drop=True)

    print(f"\n  Ranking by {label}:\n")
    print(f"  {'Name':<25} {'Score':>8}")
    print(f"  {'-'*25} {'-'*8}")

    for _, row in ranked.iterrows():
        name  = row["name"]
        score = row[field]
        print(f"  {name:<25} {score:>8.2f}")

    # students with no score listed separately
    no_score = df[["name", field]][df[field].isna()]
    if not no_score.empty:
        print(f"\n  No score (not ranked):")
        for _, row in no_score.iterrows():
            print(f"    {row['name']}")

def ranking(section: Section):
    print("\n  [Ranking Students]")

    df = get_all_students_df(section.section_id)
    if df.empty:
        print("  No students found in this section.")
        return

    field = pick_rank_field()
    display_ranking(df, field)