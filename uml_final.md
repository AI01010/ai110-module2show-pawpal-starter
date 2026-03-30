# PawPal+ UML Diagram (Final)

This matches the final implementation in `pawpal_system.py`.

```mermaid
classDiagram
    class Task {
        +str title
        +str time
        +int duration_minutes
        +str priority
        +str description
        +str frequency
        +bool completed
        +date due_date
        +mark_complete()
    }

    class Pet {
        +str name
        +str species
        +int age
        +list~Task~ tasks
        +add_task(task: Task)
        +get_tasks() list~Task~
    }

    class Owner {
        +str name
        +str contact_info
        +list~Pet~ pets
        +add_pet(pet: Pet)
        +get_all_tasks() list~Task~
    }

    class Scheduler {
        +Owner owner
        +get_all_tasks() list~Task~
        +sort_by_time() list~Task~
        +filter_by_status(completed: bool) list~Task~
        +filter_by_pet(pet_name: str) list~Task~
        +detect_conflicts() list~str~
        +generate_schedule() list~Task~
    }

    Owner "1" --> "many" Pet : owns
    Pet "1" --> "many" Task : has
    Scheduler "1" --> "1" Owner : manages via get_all_tasks()
```

## Changes from draft UML
- No structural changes required — the initial design held up through implementation.
- `mark_complete()` in `Task` now handles recurrence internally (advances `due_date` and resets `completed` for daily/weekly tasks), which was anticipated in the draft but not explicitly shown.
- `generate_schedule()` delegates to `filter_by_status(False)` rather than re-implementing sorting — a simplification discovered during implementation.
