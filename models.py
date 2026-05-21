import sqlite3
from database import get_connection, update_final_grade

class Section:
    def __init__(self, section_id, section_name):
        self.section_id   = section_id
        self.section_name = section_name

    def get_students(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, student_number, name
            FROM students
            WHERE section_id = ?
            ORDER BY CAST(student_number AS INTEGER)
        """, (self.section_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Student(sid, snum, name, self.section_id) for sid, snum, name in rows]

    def get_student_count(self):
        return len(self.get_students())

    def add_student(self, name):
        students = self.get_students()
        next_number = str(len(students) + 1).zfill(2)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (student_number, name, section_id)
            VALUES (?, ?, ?)
        """, (next_number, name, self.section_id))
        student_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO grades (student_id) VALUES (?)
        """, (student_id,))

        conn.commit()
        conn.close()
        return Student(student_id, next_number, name, self.section_id)

    def get_student_by_number(self, student_number):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT student_id, student_number, name
            FROM students
            WHERE section_id = ? AND student_number = ?
        """, (self.section_id, student_number.zfill(2)))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Student(row[0], row[1], row[2], self.section_id)
        return None


class Student:
    def __init__(self, student_id, student_number, name, section_id):
        self.student_id     = student_id
        self.student_number = student_number
        self.name           = name
        self.section_id     = section_id

    def get_grades(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT prelims, lab_act1, lab_act2,
                   midterms, semestral_project, finals, final_grade
            FROM grades
            WHERE student_id = ?
        """, (self.student_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            keys = ["prelims", "lab_act1", "lab_act2",
                    "midterms", "semestral_project", "finals", "final_grade"]
            return Grades(self.student_id, dict(zip(keys, row)))
        return None

    def display_info(self):
        grades = self.get_grades()
        print(f"\n  Student {self.student_number} - {self.name}")
        if grades:
            grades.display()
        else:
            print("  No grade record found.")


class Grades:
    FIELDS = ["prelims", "lab_act1", "lab_act2",
              "midterms", "semestral_project", "finals"]

    LABELS = {
        "prelims":           "Prelims",
        "lab_act1":          "Lab Act 1",
        "lab_act2":          "Lab Act 2",
        "midterms":          "Midterms",
        "semestral_project": "Semestral Project",
        "finals":            "Finals",
        "final_grade":       "Final Grade",
    }

    def __init__(self, student_id, data: dict):
        self.student_id = student_id
        self.data       = data

    def update_field(self, field, value):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE grades SET {field} = ? WHERE student_id = ?
        """, (value, self.student_id))
        conn.commit()
        conn.close()
        self.data[field] = value
        update_final_grade(self.student_id)

    def add_incentive(self, field, amount):
        current = self.data.get(field)
        if current is None:
            new_value = amount
        else:
            new_value = current + amount
        self.update_field(field, new_value)

    def display(self):
        all_fields = self.FIELDS + ["final_grade"]
        for field in all_fields:
            label = self.LABELS[field]
            value = self.data.get(field)
            display_val = f"{value}" if value is not None else "No score"
            print(f"    {label:<20}: {display_val}")