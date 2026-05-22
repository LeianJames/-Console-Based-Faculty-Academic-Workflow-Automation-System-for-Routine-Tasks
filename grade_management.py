from models import Section

GRADE_FIELDS = ["prelims", "lab_act1", "lab_act2", "midterms", "semestral_project", "finals"]
GRADE_LABELS = ["Prelims", "Lab Act 1", "Lab Act 2", "Midterms", "Semestral Project", "Finals"]

NOTES = "(type 'exit' to leave, type 'b' to go back, type '\\0' if no score)"

def enter_grades_for_student(student):
    print(f"\n  Entering grades for: {student.student_number} - {student.name}")
    print(f"  {NOTES}\n")

    grades = student.get_grades()
    i = 0

    while i < len(GRADE_FIELDS):
        field = GRADE_FIELDS[i]
        label = GRADE_LABELS[i]

        raw = input(f"    {label}: ").strip()

        if raw.lower() == "exit":
            print("  Exiting grade entry...")
            return "exit"

        if raw.lower() == "b":
            if i == 0:
                print("  Already at the first field.")
            else:
                i -= 1
            continue

        if raw == "\\0":
            grades.update_field(field, None)
            i += 1
            continue

        try:
            value = float(raw)
            if value < 0 or value > 100:
                print("  Please enter a value between 0 and 100.")
                continue
            grades.update_field(field, value)
            i += 1
        except ValueError:
            print("  Invalid input. Please enter a number, '\\0', 'b', or 'exit'.")

    print(f"\n  Grades saved for {student.name}.")
    return "done"


def display_students(students):
    print(f"\n  {'#':<6} {'Name':<25}")
    print(f"  {'-'*6} {'-'*25}")
    for s in students:
        print(f"  {s.student_number:<6} {s.name:<25}")


def grade_management(section: Section):
    print("\n  [Grade Management]")
    print("  Would you like to:")
    print("  1. Choose a specific student")
    print("  2. Perform operation on each student (go through each student linearly)")

    choice = input("\n  Enter choice: ").strip()

    if choice == "1":
        students = section.get_students()
        if not students:
            print("  No students found in this section.")
            return

        print(f"\n  Students in Section {section.section_name}:")
        display_students(students)

        student_number = input("\n  Enter student number: ").strip()
        student = section.get_student_by_number(student_number)

        if not student:
            print("  Student not found.")
            return

        enter_grades_for_student(student)

    elif choice == "2":
        students = section.get_students()
        if not students:
            print("  No students found in this section.")
            return

        print(f"\n  Going through all {len(students)} student(s) in order...\n")
        i = 0

        while i < len(students):
            student = students[i]
            result = enter_grades_for_student(student)

            if result == "exit":
                break

            i += 1

        print("\n  Finished going through all students.")

    else:
        print("  Invalid choice.")