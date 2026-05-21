from models import Section

GRADE_FIELDS = ["prelims", "lab_act1", "lab_act2", "midterms", "semestral_project", "finals"]

GRADE_MENU = """
    Where do you want to add the incentives?
    1. Prelims
    2. Lab Act 1
    3. Lab Act 2
    4. Midterms
    5. Semestral Project
    6. Finals
"""

def pick_grade_field():
    print(GRADE_MENU)
    while True:
        choice = input("    Enter choice: ").strip()
        if choice in [str(i) for i in range(1, 7)]:
            return GRADE_FIELDS[int(choice) - 1]
        print("    Invalid choice. Please enter a number from 1 to 6.")

def pick_incentive_amount():
    while True:
        raw = input("    Enter amount of incentive: ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("    Please enter a positive number.")
                continue
            return amount
        except ValueError:
            print("    Invalid input. Please enter a number.")

def apply_and_confirm(student, field, amount):
    grades = student.get_grades()
    grades.add_incentive(field, amount)
    print(f"\n  Successfully added {amount} incentive to {field.replace('_', ' ').title()} for {student.name}.")

def ask_add_more():
    while True:
        again = input("\n  Successfully added incentives, do you want to add more? Y/N: ").strip().upper()
        if again in ("Y", "N"):
            return again == "Y"
        print("  Please enter Y or N.")

def incentives(section: Section):
    print("\n  [Adding Incentives]")
    students = section.get_students()
    if not students:
        print("  No students found in this section.")
        return

    for s in students:
        print(f"    {s.student_number} - {s.name}")

    student_number = input("\n  Enter student number: ").strip()
    student = section.get_student_by_number(student_number)

    if not student:
        print("  Student not found.")
        return

    while True:
        field = pick_grade_field()
        amount = pick_incentive_amount()
        apply_and_confirm(student, field, amount)

        if not ask_add_more():
            break