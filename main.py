from database import initialize_db, get_section_id
from models import Section
from grade_management import grade_management
from incentives import incentives
from rankings import ranking
from class_record import class_record
from missing_compliance import missing_compliance

def pick_section():
    print("\n╔══════════════════════════════╗")
    print("║      CLASS RECORD SYSTEM     ║")
    print("╚══════════════════════════════╝")
    print("\n  Select a section:")
    print("  1. Section 1208")
    print("  2. Section 1209")
    print("  3. Section 1210")

    section_map = {"1": "1208", "2": "1209", "3": "1210"}

    while True:
        choice = input("\n  Enter choice: ").strip()
        if choice in section_map:
            section_name = section_map[choice]
            section_id   = get_section_id(section_name)
            return Section(section_id, section_name)
        print("  Invalid choice. Please enter 1, 2, or 3.")

def main_menu(section: Section):
    while True:
        print(f"\n╔══════════════════════════════╗")
        print(f"║  Section {section.section_name} — Main Menu     ║")
        print(f"╚══════════════════════════════╝")
        print("  1. Grade Management System")
        print("  2. Adding Incentives")
        print("  3. Ranking Students")
        print("  4. Class Record Tracker")
        print("  5. Missing Compliance")
        print("  6. Switch Section")
        print("  0. Exit")

        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            grade_management(section)
        elif choice == "2":
            incentives(section)
        elif choice == "3":
            ranking(section)
        elif choice == "4":
            class_record(section)
        elif choice == "5":
            missing_compliance(section)
        elif choice == "6":
            return "switch"
        elif choice == "0":
            print("\n  Goodbye!\n")
            return "exit"
        else:
            print("  Invalid choice. Please enter 0 - 6.")

def main():
    initialize_db()

    while True:
        section = pick_section()
        result  = main_menu(section)

        if result == "exit":
            break

if __name__ == "__main__":
    main()