import sqlite3

DB_NAME = "class_record.db"

students = {
    "1208": ["Harry", "Hermione", "Ron", "Draco", "Neville"],
    "1209": ["Leian Santos", "Hollie Morados", "Karl Tenorio", "Martin Magsanga", "Nawaf Didato", "Jandee Enriquez"],
    "1210": ["Gregory", "Blaise", "Anthony", "Pansy", "Pavarti"],
}

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for section_name, names in students.items():
    cursor.execute("SELECT section_id FROM sections WHERE section_name = ?", (section_name,))
    row = cursor.fetchone()
    if not row:
        print(f"Section {section_name} not found. Run main.py first to initialize the DB.")
        conn.close()
        exit(1)
    section_id = row[0]

    for i, name in enumerate(names, start=1):
        student_number = str(i).zfill(2)
        cursor.execute("""
            INSERT OR IGNORE INTO students (student_number, name, section_id)
            VALUES (?, ?, ?)
        """, (student_number, name, section_id))
        student_id = cursor.lastrowid

        if student_id:
            cursor.execute("INSERT OR IGNORE INTO grades (student_id) VALUES (?)", (student_id,))

    print(f"Seeded {len(names)} students into Section {section_name}.")

conn.commit()
conn.close()
print("Done.")