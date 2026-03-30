# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Core features: enter basic info of owner and their pet, add/edit tasks, and generate a schedule of activities for the pet. 
    Represent pet care tasks (what needs to happen, how long it takes, priority)
    Represent the pet and the owner (basic info and preferences)
    Build a plan/schedule for a day that chooses and orders tasks based on constraints
    Explain the plan (why each task was chosen and when it happens)
- Briefly describe your initial UML design.  Allow user info input for the owener, then allow adding pets with name, type, and preferences.  Allow adding tasks with name, duration, priority, and pet.  Generate a schedule that orders tasks based on priority and time constraints.
- What classes did you include, and what responsibilities did you assign to each?
    - **Task** (dataclass): Holds a single care activity — title, time (HH:MM), duration, priority, frequency, and completion state. Responsible only for representing and marking itself done.
    - **Pet** (dataclass): Holds pet info (name, species, age) and owns a list of Tasks. Responsible for adding and returning its own tasks.
    - **Owner**: Manages multiple Pet objects and exposes a flattened view of all tasks across all pets.
    - **Scheduler**: The "brain" — it holds a reference to the Owner and provides all sorting, filtering, conflict detection, and schedule generation logic. All algorithmic behavior lives here so the data classes stay clean.

**b. Design changes**

- Did your design change during implementation?
    Yes. Initially the plan was to put schedule generation logic inside `Owner`, but after drafting the UML it was clear that mixing data management and algorithmic logic in the same class would make the code harder to test and extend. Moving all scheduling algorithms into a dedicated `Scheduler` class keeps `Owner` and `Pet` as simple data containers and isolates the "smart" behavior in one place.
- If yes, describe at least one change and why you made it.
    Moved `sort_by_time`, `filter_by_status`, `filter_by_pet`, and `detect_conflicts` entirely into `Scheduler`. `Owner.get_all_tasks()` becomes a simple helper that flattens all pet tasks into one list — `Scheduler` calls it and then does all the work. This separation makes each class easier to test independently.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)? 
    time and priority
- How did you decide which constraints mattered most? 
    time matters the most since some things are timesenstive like feeding, and priority matters for when theres overlap or for things that are less time-sensitive but still important, like playtime or grooming.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes. 
    In my scheduler, if two tasks overlap, it prioritizes the one with higher priority.
- Why is that tradeoff reasonable for this scenario?
    This tradeoff is reasonable because it ensures that the most important tasks get done, even if it means some less important tasks might be delayed or skipped. For example, feeding the pet is more critical than playtime, so if they overlap, feeding will take precedence to ensure the pet's basic needs are met.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    I used AI for implementation and debugging. I used it to help me write code for the scheduling logic and to debug issues that came up during testing.
- What kinds of prompts or questions were most helpful?
    Implement this or that function with description functionality, explain this error message, how can I fix this bug, how can I optimize this code, take it task by task/step by step,etc.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    When implementing conflict detection, AI suggested raising an exception when two tasks share a time slot. I changed it to return a list of warning strings instead, because crashing the program for a scheduling conflict is too disruptive — users should be informed and still be able to continue using the app.
- How did you evaluate or verify what the AI suggested?
    If the output met the requirements and made sense in the context of the project, I would accept it. 
    If it seemed off or didn't fully meet the requirements, I would review the code and make adjustments as needed. 
    I also tested the code to make sure it worked and didn't make new bugs.
    I also cehcked for good UI

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test? 
    I tested that the scheduler correctly generates a schedule based on the tasks and their priorities, that it handles overlapping tasks appropriately, and that it respects time constraints. I also tested the user interface to ensure that users can input their information and tasks correctly.
- Why were these tests important?
    These tests were important to ensure that the core functionality of the scheduler works and that users can use the system without issues. 
    Testing the scheduling logic is important to verify that it correctly prioritizes tasks and handles constraints. 
    testing the UI ensures a good user experience.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Pretty confident in the core logic — all 8 tests pass and the CLI demo works as expected. The main uncertainty is around edge cases that aren't tested yet, like what happens when all tasks for a pet are completed, or when two pets have tasks at the exact same time with the same priority.
- What edge cases would you test next if you had more time?
    time and time overlap with same priortiy or adding more features and tesing there ovelap

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    The separation between the data classes and the Scheduler. Keeping Task and Pet as simple dataclasses and putting all the logic in Scheduler made the code a lot cleaner and easier to test. Each class has one clear job and they don't step on each other.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    I'd improve the conflict detection to handle time ranges instead of just exact start times — two tasks that overlap but don't start at the same minute would be missed right now. I'd also add priority-based resolution so when there is a conflict, the scheduler automatically recommends keeping the higher-priority task.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    AI is really good at scaffolding and filling in boilerplate fast, but you still have to be the one who decides the architecture. The AI doesn't know your project's constraints or what tradeoffs matter — you have to give it direction and then review what it produces. Being the "lead architect" means knowing what you want before you ask.
