import streamlit as st

# -------------------- INITIAL SETUP --------------------

st.set_page_config(page_title="Startup Teamwork Quest", page_icon="🚀")

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.step = "role"   # "role", "s1", "s2", "s3", "summary"
    st.session_state.role = None
    st.session_state.morale = 5
    st.session_state.budget = 5
    st.session_state.reputation = 5
    st.session_state.history = []


# -------------------- HELPERS --------------------

def apply_deltas(label, choice_text, dm, db, dr):
    st.session_state.morale += dm
    st.session_state.budget += db
    st.session_state.reputation += dr

    st.session_state.history.append(
        {
            "scenario": label,
            "choice": choice_text,
            "Δ morale": dm,
            "Δ budget": db,
            "Δ reputation": dr,
        }
    )


def show_stats():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Team Morale", st.session_state.morale)
    with c2:
        st.metric("Budget", st.session_state.budget)
    with c3:
        st.metric("Client Reputation", st.session_state.reputation)


# -------------------- ROLE SELECTION --------------------

def page_role():
    st.title("🚀 Startup Teamwork Quest")
    st.subheader("Choose your role")

    st.write(
        "You’re part of a small startup building a new sustainability app. "
        "Each player takes a role with slightly different priorities."
    )

    roles = {
        "Marketing Manager": {
            "focus": "Keep the client happy and grow visibility.",
            "secret": "You feel successful if Reputation ends high.",
        },
        "Tech Lead": {
            "focus": "Deliver a working product without burning out the team.",
            "secret": "You care a lot about Morale and realistic workload.",
        },
        "Finance Lead": {
            "focus": "Make sure the project doesn’t blow the budget.",
            "secret": "You feel responsible for keeping Budget healthy.",
        },
    }

    role = st.radio("Select your role:", list(roles.keys()))

    if role is not None:
        info = roles[role]
        st.info(
            f"**{role}**\n\n"
            f"- Main focus: {info['focus']}\n"
            f"- Secret preference: {info['secret']}"
        )

    st.write("---")

    if st.button("Start the project ➜"):
        if role is None:
            st.warning("Please select a role before starting.")
        else:
            st.session_state.role = role
            st.session_state.step = "s1"
            st.rerun()


# -------------------- SCENARIO 1 --------------------

def page_s1():
    st.title("Scenario 1 – The First Big Decision")
    show_stats()
    st.write("---")

    st.write(
        "The startup has limited time and money before the next investor meeting.\n\n"
        "You can either:\n"
        "- Build a basic prototype and test it with a few users, **or**\n"
        "- Invest more in marketing and visuals to impress the client."
    )

    choice = st.radio(
        "What do you decide?",
        [
            "Focus on a simple working prototype.",
            "Focus on flashy marketing material.",
            "Try to do both at the same time.",
        ],
        key="s1_choice",
    )

    if st.button("Confirm decision for Scenario 1"):
        if st.session_state.get("s1_answered", False):
            st.warning("You already locked this decision.")
            return

        if choice == "Focus on a simple working prototype.":
            apply_deltas("Scenario 1", choice, dm=1, db=-1, dr=1)
        elif choice == "Focus on flashy marketing material.":
            apply_deltas("Scenario 1", choice, dm=-1, db=-1, dr=2)
        else:
            apply_deltas("Scenario 1", choice, dm=-2, db=-2, dr=2)

        st.session_state.s1_answered = True
        st.session_state.step = "s2"
        st.rerun()


# -------------------- SCENARIO 2 --------------------

def page_s2():
    st.title("Scenario 2 – Team Conflict")
    show_stats()
    st.write("---")

    st.write(
        "Two key team members disagree:\n\n"
        "- The developer says the current plan is unrealistic.\n"
        "- The marketing person insists the promised features must be delivered.\n\n"
        "The atmosphere is getting tense and deadlines are approaching."
    )

    choice = st.radio(
        "How do you handle this conflict?",
        [
            "Hold a mediation meeting and renegotiate scope.",
            "Let them resolve it on their own.",
            "Reassign one of them to another task.",
        ],
        key="s2_choice",
    )

    if st.button("Confirm decision for Scenario 2"):
        if st.session_state.get("s2_answered", False):
            st.warning("You already locked this decision.")
            return

        if choice == "Hold a mediation meeting and renegotiate scope.":
            apply_deltas("Scenario 2", choice, dm=2, db=-1, dr=0)
        elif choice == "Let them resolve it on their own.":
            apply_deltas("Scenario 2", choice, dm=-2, db=0, dr=-1)
        else:
            apply_deltas("Scenario 2", choice, dm=-1, db=0, dr=1)

        st.session_state.s2_answered = True
        st.session_state.step = "s3"
        st.rerun()


# -------------------- SCENARIO 3 --------------------

def page_s3():
    st.title("Scenario 3 – Last-Minute Client Request")
    show_stats()
    st.write("---")

    st.write(
        "Two days before the demo, the client asks for an extra feature that "
        "was never part of the original scope.\n\n"
        "It would really impress them, but it will put pressure on the team."
    )

    choice = st.radio(
        "What do you decide?",
        [
            "Accept the request and squeeze it in.",
            "Push back and protect the team.",
            "Accept, but charge extra and reduce something else.",
        ],
        key="s3_choice",
    )

    if st.button("Confirm decision for Scenario 3"):
        if st.session_state.get("s3_answered", False):
            st.warning("You already locked this decision.")
            return

        if choice == "Accept the request and squeeze it in.":
            apply_deltas("Scenario 3", choice, dm=-2, db=-1, dr=2)
        elif choice == "Push back and protect the team.":
            apply_deltas("Scenario 3", choice, dm=1, db=0, dr=-1)
        else:
            apply_deltas("Scenario 3", choice, dm=-1, db=2, dr=1)

        st.session_state.s3_answered = True
        st.session_state.step = "summary"
        st.rerun()


# -------------------- SUMMARY / ENDING --------------------

def page_summary():
    st.title("📊 Project Outcome")
    show_stats()
    st.write("---")

    total = (
        st.session_state.morale
        + st.session_state.budget
        + st.session_state.reputation
    )

    if total >= 18:
        ending = "High cohesion & sustainable success 🎉"
    elif total >= 12:
        ending = "Mixed outcome – some wins, some scars 😐"
    else:
        ending = "Low cohesion – fragile success or quiet failure 😬"

    st.subheader(ending)

    st.write("### Your decisions along the way:\n")
    for h in st.session_state.history:
        st.markdown(
            f"- **{h['scenario']}** – *{h['choice']}*  \n"
            f"  Δ morale: {h['Δ morale']}, "
            f"Δ budget: {h['Δ budget']}, "
            f"Δ reputation: {h['Δ reputation']}"
        )

    st.write("---")

    if st.button("Restart game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# -------------------- ROUTER --------------------

step = st.session_state.step

if step == "role":
    page_role()
elif step == "s1":
    page_s1()
elif step == "s2":
    page_s2()
elif step == "s3":
    page_s3()
elif step == "summary":
    page_summary()
