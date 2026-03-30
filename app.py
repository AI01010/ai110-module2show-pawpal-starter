"""PawPal+ Streamlit UI — connects to pawpal_system.py backend."""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("PawPal+")
st.caption("Smart pet care scheduling assistant")

# ── Session state: persist Owner across reruns ───────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Step 1: Owner setup ───────────────────────────────────────────────────────
with st.expander("Owner Setup", expanded=st.session_state.owner is None):
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value="Jordan")
        contact    = st.text_input("Contact info (optional)")
        submitted  = st.form_submit_button("Save owner")
        if submitted and owner_name:
            st.session_state.owner = Owner(name=owner_name, contact_info=contact)
            st.success(f"Owner '{owner_name}' saved!")

if st.session_state.owner is None:
    st.info("Enter owner info above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
st.divider()

# ── Step 2: Add a pet ─────────────────────────────────────────────────────────
st.subheader("Pets")
with st.form("pet_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species  = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        age      = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
    add_pet = st.form_submit_button("Add pet")
    if add_pet and pet_name:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    st.write(f"Pets: {', '.join(pet_names)}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Step 3: Add a task ────────────────────────────────────────────────────────
st.subheader("Schedule a Task")
if not owner.pets:
    st.warning("Add at least one pet before scheduling tasks.")
else:
    with st.form("task_form"):
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
            task_time  = st.text_input("Time (HH:MM)", value="08:00")
            duration   = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col2:
            priority   = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            frequency  = st.selectbox("Frequency", ["once", "daily", "weekly"])
            target_pet = st.selectbox("Assign to pet", [p.name for p in owner.pets])

        add_task = st.form_submit_button("Add task")
        if add_task and task_title:
            task = Task(
                title=task_title,
                time=task_time,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
            )
            pet = next(p for p in owner.pets if p.name == target_pet)
            pet.add_task(task)
            st.success(f"Task '{task_title}' added to {target_pet}!")

st.divider()

# ── Step 4: Generate schedule ─────────────────────────────────────────────────
st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    all_tasks = scheduler.sort_by_time()

    if not all_tasks:
        st.info("No tasks yet. Add some above.")
    else:
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for c in conflicts:
                st.warning(c)

        rows = [
            {
                "Time":     t.time,
                "Task":     t.title,
                "Priority": t.priority,
                "Freq":     t.frequency,
                "Done":     "Yes" if t.completed else "No",
            }
            for t in all_tasks
        ]
        st.table(rows)

    # Mark complete
    incomplete = [t for t in scheduler.get_all_tasks() if not t.completed]
    if incomplete:
        st.markdown("**Mark a task complete:**")
        task_to_complete = st.selectbox(
            "Select task", [t.title for t in incomplete], key="complete_select"
        )
        if st.button("Mark complete"):
            for t in incomplete:
                if t.title == task_to_complete:
                    t.mark_complete()
                    st.success(f"'{task_to_complete}' marked complete!")
                    break
