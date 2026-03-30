"""PawPal+ Streamlit UI — connects to pawpal_system.py backend."""

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("PawPal+")
st.caption("Smart pet care scheduling assistant")

# ── Session state ─────────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None
if "show_schedule" not in st.session_state:
    st.session_state.show_schedule = False

# ── Owner setup ───────────────────────────────────────────────────────────────
with st.expander("Owner Setup", expanded=st.session_state.owner is None):
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name", value="Jordan")
        contact    = st.text_input("Contact info (optional)")
        if st.form_submit_button("Save owner") and owner_name:
            st.session_state.owner = Owner(name=owner_name, contact_info=contact)
            st.session_state.show_schedule = False
            st.success(f"Owner '{owner_name}' saved!")

if st.session_state.owner is None:
    st.info("Enter owner info above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
st.divider()

# ── Add a pet ─────────────────────────────────────────────────────────────────
st.subheader("Pets")
with st.form("pet_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        age = st.number_input("Age (years)", min_value=0, max_value=30, value=2)
    if st.form_submit_button("Add pet") and pet_name:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name} the {species}!")

if owner.pets:
    st.write("Pets: " + ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add a task ────────────────────────────────────────────────────────────────
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

        if st.form_submit_button("Add task") and task_title:
            task = Task(
                title=task_title,
                time=task_time,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
            )
            next(p for p in owner.pets if p.name == target_pet).add_task(task)
            st.session_state.show_schedule = False   # reset so schedule refreshes
            st.success(f"Task '{task_title}' added to {target_pet}!")

st.divider()

# ── Schedule ──────────────────────────────────────────────────────────────────
st.subheader("Today's Schedule")

col_btn, col_hide = st.columns([2, 1])
with col_btn:
    if st.button("Show / Refresh Schedule"):
        st.session_state.show_schedule = True
with col_hide:
    if st.button("Hide Schedule"):
        st.session_state.show_schedule = False

if st.session_state.show_schedule and owner.pets:
    scheduler = Scheduler(owner)
    pairs = scheduler.get_tasks_with_pets()   # [(task, pet_name), ...]

    if not pairs:
        st.info("No tasks yet. Add some above.")
    else:
        # ── Filters ───────────────────────────────────────────────────────────
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            pet_filter = st.selectbox(
                "Filter by pet", ["All"] + [p.name for p in owner.pets], key="pet_filter"
            )
        with fcol2:
            status_filter = st.selectbox(
                "Filter by status", ["All", "Pending", "Completed"], key="status_filter"
            )

        # Apply filters
        filtered = pairs
        if pet_filter != "All":
            filtered = [(t, pn) for t, pn in filtered if pn == pet_filter]
        if status_filter == "Pending":
            filtered = [(t, pn) for t, pn in filtered if not t.completed]
        elif status_filter == "Completed":
            filtered = [(t, pn) for t, pn in filtered if t.completed]

        # ── Progress bar ──────────────────────────────────────────────────────
        done, total = scheduler.completion_progress()
        st.progress(done / total if total else 0, text=f"{done} / {total} tasks completed")

        # ── Conflict warnings ─────────────────────────────────────────────────
        for c in scheduler.detect_conflicts():
            st.warning(c)

        # ── Schedule table ────────────────────────────────────────────────────
        if filtered:
            rows = [
                {
                    "Time":     t.time,
                    "Pet":      pn,
                    "Task":     t.title,
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority,
                    "Freq":     t.frequency,
                    "Status":   "Done" if t.completed else "Pending",
                }
                for t, pn in filtered
            ]
            st.table(rows)
        else:
            st.info("No tasks match the current filters.")

        st.divider()

        # ── Actions ───────────────────────────────────────────────────────────
        all_task_pairs = scheduler.get_tasks_with_pets()

        # Label helper: "08:00 — Morning walk (Mochi)"
        def label(task, pet_name):
            return f"{task.time} — {task.title} ({pet_name})"

        acol1, acol2 = st.columns(2)

        with acol1:
            st.markdown("**Mark complete**")
            incomplete = [(t, pn) for t, pn in all_task_pairs if not t.completed]
            if incomplete:
                chosen_complete = st.selectbox(
                    "Task to complete",
                    [label(t, pn) for t, pn in incomplete],
                    key="complete_sel",
                )
                if st.button("Mark complete"):
                    for t, pn in incomplete:
                        if label(t, pn) == chosen_complete:
                            t.mark_complete()
                            break
            else:
                st.success("All tasks done!")

        with acol2:
            st.markdown("**Delete task**")
            if all_task_pairs:
                chosen_delete = st.selectbox(
                    "Task to delete",
                    [label(t, pn) for t, pn in all_task_pairs],
                    key="delete_sel",
                )
                if st.button("Delete task"):
                    for t, pn in all_task_pairs:
                        if label(t, pn) == chosen_delete:
                            scheduler.delete_task(t)
                            break
            else:
                st.info("No tasks to delete.")
