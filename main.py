import streamlit as st
import datetime
import json
import time  # Add at top
from ai import ask_ai, get_macros
from profiles import create_profile, get_notes, get_profile
from form_submit import update_personal_info, add_note, delete_note

st.title("Workout Planner")

@st.fragment()
def personal_data_form():
    if "profile" not in st.session_state:
        st.error("Profile not loaded yet.")
        return

    with st.form("personal_data"):
        st.header("Enter Personal Details")

        profile = st.session_state.profile
        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input("Age", min_value=1, max_value=120, step=1, value=profile["general"]["age"])
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, step=0.1, value=float(profile["general"]["weight"]))
        height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, step=0.1, value=float(profile["general"]["height"]))
        genders = ["Male", "Female", "Other"]
        gender = st.radio("Gender", genders, genders.index(profile["general"].get("gender", "Male")))
        activities = ("Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active")
        activity_level = st.selectbox("Activity Level", activities, index=activities.index(profile["general"].get("activity_level", "Sedentary")))

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                        profile,
                        "general",
                        name=name,
                        weight=weight,
                        height=height,
                        gender=gender,
                        age=age,
                        activity_level=activity_level,
                    )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all of the data!")

@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goals = st.multiselect("Select your Goals", ["Muscle Gain", "Fat Loss", "Stay Active"], default=profile.get("goals", ["Muscle Gain"]))

        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(profile, "goals", goals=goals)
                    st.success("Goals updated")
            else:
                st.warning("Please select at least one goal.")

@st.fragment()
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    if nutrition.button("Generate with AI"):
        try:
            result = get_macros(profile.get("general"), profile.get("goals"))
            profile["nutrition"] = result
            nutrition.success("AI has generated the results.")
        except Exception as e:
            st.error(f"Error generating macros: {e}")

    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories = st.number_input("Calories", min_value=0, step=1, value=profile["nutrition"].get("calories", 0))
        with col2:
            protein = st.number_input("Protein", min_value=0, step=1, value=profile["nutrition"].get("protein", 0))
        with col3:
            fat = st.number_input("Fat", min_value=0, step=1, value=profile["nutrition"].get("fat", 0))
        with col4:
            carbs = st.number_input("Carbs", min_value=0, step=1, value=profile["nutrition"].get("carbs", 0))

        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state.profile = update_personal_info(
                    profile,
                    "nutrition",
                    protein=protein,
                    calories=calories,
                    fat=fat,
                    carbs=carbs,
                )
                st.success("Information saved")

@st.fragment()
def notes_section():
    st.subheader("Add Notes: ")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=i):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()

    new_note = st.text_input("Add a new note:(Example: Any medical condition, etc) ")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()

@st.fragment()
def ask_ai_func():
    st.subheader('Ask AI')
    user_question = st.text_input("Ask AI a question:")

    if st.button("Ask AI"):
        with st.spinner("Thinking... This may take a while..."):
            try:
                def make_json_safe(obj):
                    if isinstance(obj, dict):
                        return {k: make_json_safe(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [make_json_safe(item) for item in obj]
                    elif isinstance(obj, datetime.datetime):
                        return obj.isoformat()
                    else:
                        return obj

                full_profile = st.session_state.profile
                minimal_profile = {
                    "general": full_profile.get("general", {}),
                    "goals": full_profile.get("goals", []),
                    "nutrition": full_profile.get("nutrition", {})
                }
                safe_profile = make_json_safe(minimal_profile)

                # -- HERE: No retries, just directly call and wait
                st.write("Sending to AI...")

                result = ask_ai(safe_profile, user_question)

                st.success("Got response from AI!")
                st.write(result)

            except Exception as e:
                st.error(f"Error while asking AI: {e}")


def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        notes = get_notes(st.session_state.profile_id)

        # --- Make notes JSON safe ---
        for note in notes:
            if "injected" in note and isinstance(note["injected"], datetime.datetime):
                note["injected"] = note["injected"].isoformat()

        st.session_state.notes = notes

    personal_data_form()
    goals_form()
    macros()
    notes_section()
    ask_ai_func()

if __name__ == "__main__":
    forms()
