"""PawPal+ backend logic: Owner, Pet, Task, Scheduler."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    time: str                        # "HH:MM" format
    duration_minutes: int
    priority: str                    # "low" | "medium" | "high"
    description: str = ""
    frequency: str = "once"          # "once" | "daily" | "weekly"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self):
        """Mark this task done and advance due_date for recurring tasks."""
        self.completed = True
        if self.frequency == "daily":
            self.due_date = self.due_date + timedelta(days=1)
            self.completed = False
        elif self.frequency == "weekly":
            self.due_date = self.due_date + timedelta(weeks=1)
            self.completed = False


@dataclass
class Pet:
    """Stores pet details and its associated task list."""

    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Append a Task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list:
        """Return all tasks assigned to this pet."""
        return self.tasks


class Owner:
    """Manages a collection of pets and provides a unified task view."""

    def __init__(self, name: str, contact_info: str = ""):
        self.name = name
        self.contact_info = contact_info
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a Pet to the owner's roster."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of every task across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across all of an owner's pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted chronologically by time (HH:MM)."""
        return sorted(self.get_all_tasks(), key=lambda t: t.time)

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completion status."""
        return [t for t in self.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks belonging to the named pet."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for any two tasks scheduled at the same time."""
        seen: dict[str, str] = {}   # time -> first task title
        warnings = []
        for task in self.get_all_tasks():
            if task.time in seen:
                warnings.append(
                    f"Conflict at {task.time}: '{seen[task.time]}' and '{task.title}'"
                )
            else:
                seen[task.time] = task.title
        return warnings

    def generate_schedule(self) -> list[Task]:
        """Return today's incomplete tasks sorted by time, with conflicts noted."""
        return self.filter_by_status(completed=False)
