import sys
from timetable_system.models import init_db, SessionLocal
from timetable_system.repositories.timetable_manager import TimetableManager
from timetable_system.services.scheduler import TimetableScheduler
from timetable_system.services.input_service import InputService
from timetable_system.utils.logger import logger

def collect_class_subjects(class_name: str, allowed_subjects: list, periods: int) -> list:
    print(f"\n--- Entering subjects for {class_name} ---")
    print(f"Allowed: {', '.join(allowed_subjects)}")
    
    result = []
    while len(result) < periods:
        remaining = periods - len(result)
        logger.info(f"Remaining periods to fill: {remaining}")
        
        sub = InputService.get_valid_choice("Subject > ", allowed_subjects)
        count = InputService.get_valid_int(f"No. of periods for {sub} > ", min_val=1, max_val=remaining)
        
        result.extend([sub] * count)
        
    return result

def create_timetable_flow(tm: TimetableManager):
    periods = InputService.get_valid_int("Total periods per day > ", min_val=1, max_val=12)
    
    sci_subjects = ["MATH", "PHY", "CHEM", "BIO", "ENG", "CS", "PT", "LIB"]
    arts_subjects = ["MATH", "ACC", "BST", "ECO", "ENG", "IP", "PT", "LIB"]
    
    # Hardcoded classes for now, can be dynamic later
    classes = {
        "12A": sci_subjects,
        "12B": sci_subjects,
        "11A": arts_subjects,
        "11B": arts_subjects
    }
    
    data = {}
    for cls, subjects in classes.items():
        data[cls] = collect_class_subjects(cls, subjects, periods)
        
    logger.info("Generating timetable...")
    scheduler = TimetableScheduler(data, periods)
    schedule = scheduler.solve()
    
    if schedule:
        print("\n--- Generated Timetable ---")
        for i in range(periods):
            row = [schedule[cls][i] for cls in classes]
            print(f"Period {i+1}: {row} (Classes: {list(classes.keys())})")
            
        save = InputService.get_valid_choice("Save this timetable? (Y/N) > ", ["Y", "N"])
        if save == "Y":
            name = input("Enter unique name for timetable > ")
            try:
                tm.create_timetable(name, schedule, periods)
                logger.info(f"Timetable '{name}' saved successfully.")
            except ValueError as e:
                logger.error(str(e))
    else:
        logger.error("Failed to generate a conflict-free timetable. Try reducing constraints.")

def list_timetables_flow(tm: TimetableManager):
    timetables = tm.get_all_timetables()
    if not timetables:
        print("No timetables found.")
        return
    
    print("\n--- Saved Timetables ---")
    for t in timetables:
        print(f"ID: {t.id} | Name: {t.name} | Created: {t.created_at}")

def view_timetable_flow(tm: TimetableManager):
    name = input("Enter timetable name to view > ")
    t = tm.get_timetable_by_name(name)
    if not t:
        print("Timetable not found.")
        return
        
    # Organize by period
    # We need to reconstruct the grid. 
    # Logic: Find max period, then iterate.
    if not t.entries:
        print("Empty timetable.")
        return

    max_period = max(e.period_index for e in t.entries)
    classes = sorted(list(set(e.class_name for e in t.entries)))
    
    print(f"\n--- Timetable: {t.name} ---")
    header = f"{'Period':<8} | " + " | ".join([f"{c:<8}" for c in classes])
    print(header)
    print("-" * len(header))
    
    grid = {p: {c: "" for c in classes} for p in range(max_period + 1)}
    for entry in t.entries:
        grid[entry.period_index][entry.class_name] = entry.subject
        
    for p in range(max_period + 1):
        row = f"{p+1:<8} | "
        for c in classes:
            row += f"{grid[p][c]:<8} | "
        print(row)

def delete_timetable_flow(tm: TimetableManager):
    name = input("Enter timetable name to delete > ")
    if tm.delete_timetable(name):
        logger.info(f"Timetable '{name}' deleted.")
    else:
        logger.error("Timetable not found.")

def main():
    init_db()
    db = SessionLocal()
    tm = TimetableManager(db)
    
    while True:
        print("\n=== Timetable Management System ===")
        print("1. Create New Timetable")
        print("2. List Timetables")
        print("3. View Timetable")
        print("4. Delete Timetable")
        print("5. Exit")
        
        choice = input("Select option > ")
        
        if choice == "1":
            create_timetable_flow(tm)
        elif choice == "2":
            list_timetables_flow(tm)
        elif choice == "3":
            view_timetable_flow(tm)
        elif choice == "4":
            delete_timetable_flow(tm)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
