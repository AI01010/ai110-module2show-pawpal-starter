"""Demo script: verify PawPal+ backend logic in the terminal."""

from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", contact_info="jordan@email.com")

mochi = Pet(name="Mochi", species="dog", age=3)
luna = Pet(name="Luna", species="cat", age=5)

owner.add_pet(mochi)
owner.add_pet(luna)

# --- Add tasks (intentionally out of order) ---
mochi.add_task(Task(title="Evening walk",   time="18:00", duration_minutes=30, priority="high",   frequency="daily"))
mochi.add_task(Task(title="Morning walk",   time="08:00", duration_minutes=20, priority="high",   frequency="daily"))
mochi.add_task(Task(title="Flea treatment", time="09:00", duration_minutes=5,  priority="medium", frequency="weekly"))
luna.add_task(Task( title="Feeding",        time="08:00", duration_minutes=10, priority="high",   frequency="daily"))
luna.add_task(Task( title="Grooming",       time="14:00", duration_minutes=15, priority="low",    frequency="weekly"))

scheduler = Scheduler(owner)

# --- Today's schedule (sorted) ---
print("=" * 45)
print(f"  PawPal+ Daily Schedule for {owner.name}")
print("=" * 45)
for task in scheduler.sort_by_time():
    status = "[done]" if task.completed else "[    ]"
    print(f"  {status}  {task.time}  {task.title:<20}  [{task.priority}]  ({task.frequency})")
print()

# --- Conflict detection ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("WARNING: Conflicts detected:")
    for c in conflicts:
        print(f"   {c}")
else:
    print("No scheduling conflicts.")
print()

# --- Mark Mochi's morning walk complete and show recurrence ---
morning_walk = mochi.tasks[1]
print(f"Marking '{morning_walk.title}' complete (frequency={morning_walk.frequency})...")
morning_walk.mark_complete()
print(f"  completed={morning_walk.completed}, next due={morning_walk.due_date}")
print()

# --- Filter by pet ---
print("Luna's tasks:")
for task in scheduler.filter_by_pet("Luna"):
    print(f"  {task.time}  {task.title}")
