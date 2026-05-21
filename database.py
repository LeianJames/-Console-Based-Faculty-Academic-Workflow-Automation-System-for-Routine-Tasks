import sqlite3
import pandas as pd

DB_NAME = "class_record.db"

GRADE_WEIGHTS = {
    "prelims": 0.20,
    "lab_act1": 0.10,
    "lab_act2": 0.10,
    "midterms": 0.20,
    "semestral_project": 0.15,
    "finals": 0.25,
}

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            section_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            section_name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number TEXT NOT NULL,
            name           TEXT NOT NULL,
            section_id     INTEGER NOT NULL,
            FOREIGN KEY (section_id) REFERENCES sections(section_id),
            UNIQUE (student_number, section_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id           INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id         INTEGER UNIQUE NOT NULL,
            prelims            REAL,
            lab_act1           REAL,
            lab_act2           REAL,
            midterms           REAL,
            semestral_project  REAL,
            finals             REAL,
            final_grade        REAL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    for section in ("1208", "1209", "1210"):
        cursor.execute(
            "INSERT OR IGNORE INTO sections (section_name) VALUES (?)", (section,)
        )

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def get_section_id(section_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT section_id FROM sections WHERE section_name = ?", (section_name,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def compute_final_grade(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT prelims, lab_act1, lab_act2, midterms, semestral_project, finals
        FROM grades WHERE student_id = ?
    """, (student_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    keys = list(GRADE_WEIGHTS.keys())
    total_weight = 0.0
    weighted_sum = 0.0

    for i, key in enumerate(keys):
        score = row[i]
        if score is not None:
            weighted_sum += score * GRADE_WEIGHTS[key]
            total_weight += GRADE_WEIGHTS[key]

    if total_weight == 0:
        return None

    return round(weighted_sum / total_weight, 2)

def update_final_grade(student_id):
    final = compute_final_grade(student_id)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE grades SET final_grade = ? WHERE student_id = ?",
        (final, student_id)
    )
    conn.commit()
    conn.close()

def get_all_students_df(section_id):
    conn = get_connection()
    query = """
        SELECT s.student_number, s.name,
               g.prelims, g.lab_act1, g.lab_act2,
               g.midterms, g.semestral_project, g.finals, g.final_grade
        FROM students s
        LEFT JOIN grades g ON s.student_id = g.student_id
        WHERE s.section_id = ?
        ORDER BY CAST(s.student_number AS INTEGER)
    """
    df = pd.read_sql_query(query, conn, params=(section_id,))
    conn.close()
    return df