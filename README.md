# PawPal+ (Module 2 Project)

A smart pet care scheduling app built with Python and Streamlit. Helps a pet owner plan daily care tasks across multiple pets with sorting, conflict detection, and recurring task support.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- **Add multiple pets** — Each pet has its own task list (name, species, age)
- **Schedule tasks** — Assign tasks to specific pets with a time, duration, priority, and frequency
- **Sorted schedule** — Tasks are displayed in chronological order using `Scheduler.sort_by_time()`
- **Conflict warnings** — If two tasks share the same time slot, the app surfaces a `st.warning()` message
- **Recurring tasks** — Daily and weekly tasks automatically reschedule themselves when marked complete (via `timedelta`)
- **Mark complete** — Tasks can be marked done from the UI; recurring tasks advance their due date automatically
- **Filter by pet or status** — Backend supports filtering tasks by pet name or completion state

## Smarter Scheduling

The `Scheduler` class provides four algorithmic features:

| Method | What it does |
|--------|-------------|
| `sort_by_time()` | Sorts all tasks by `HH:MM` string — lexicographic sort works correctly for zero-padded times |
| `filter_by_status(completed)` | Returns only complete or incomplete tasks |
| `filter_by_pet(pet_name)` | Returns tasks for a single named pet |
| `detect_conflicts()` | Scans all tasks for duplicate time slots and returns human-readable warning strings |

Recurring task logic lives in `Task.mark_complete()`: calling it on a `daily` or `weekly` task resets `completed` to `False` and advances `due_date` by the appropriate `timedelta` — no separate scheduler pass needed.

## Project Structure

```
pawpal_system.py   # Backend logic: Task, Pet, Owner, Scheduler
app.py             # Streamlit UI
main.py            # CLI demo script
tests/
  test_pawpal.py   # Automated test suite (8 tests)
uml_draft.md       # Initial Mermaid.js UML diagram
uml_final.md       # Final UML after implementation
reflection.md      # Design decisions and reflections
```

## Getting Started

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the CLI demo:
```bash
python main.py
```

Run the Streamlit app:
```bash
streamlit run app.py
```

## Testing PawPal+

Run the full test suite:
```bash
python -m pytest
```

Tests cover:
- **Task completion** — `mark_complete()` sets `completed=True` for one-time tasks
- **Task count** — Adding a task increases the pet's task list length
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order regardless of insertion order
- **Daily recurrence** — Completing a daily task advances `due_date` by 1 day and resets `completed`
- **Weekly recurrence** — Completing a weekly task advances `due_date` by 7 days
- **Conflict detection (positive)** — Two tasks at 08:00 trigger a conflict warning
- **Conflict detection (negative)** — Tasks at different times produce no warnings
- **Status filtering** — `filter_by_status(False)` returns only incomplete tasks

**Confidence level: ★★★★☆**
The core scheduling behaviors are well-covered. Edge cases not yet tested: multiple pets with the same task time, tasks spanning midnight, or an owner with no pets.

## 📸 Demo

*(Screenshot to be added after final UI review)*
