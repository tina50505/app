import streamlit as st
import time

# -------------------- CONFIG --------------------

TIMER_SEC = 45   # seconds allowed per scenario

st.set_page_config(page_title="Startup Teamwork Quest", page_icon="🚀")

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.step = "intro"    # NEW: introduction page
    st.session_state.role = None
    st.session_state.morale = 5
    st.session_state.budget = 5
    st.session_state.reputation = 5
    st.session_state.history = []
    st.session_state.start_time = None


# -------------------- HELPERS --------------------

def start_timer():
    st.session_state.start_time = time.time()

def time_left():
    if st.session_state.start_time is None:
        return TIMER_SEC
    elapsed = time.time() - st.session_state.start_time
    remaining = TIMER_SEC - int(elapsed)
    return max(0, remaining)

def timer_expired():
    return time_left() <= 0

def apply_deltas(label, choice_text, dm, db, dr):
    st.session_state.morale += dm
    st.session_state.budget += db
    st.session_state.reputation += dr
    st.session_state.history.append({
        "scenario": label,
        "choice": choice_text,
        "Δ morale": dm,
        "Δ budget": db,
        "Δ reputation": dr,
    })


def show_stats():
    c1, c2, c3 = st.columns(3)
    c1.metric("Team Morale", st.session_state.morale)
    c2.metric("Budget", st.session_state.budget)
    c3.metric("Client Reputation", st.session_state.reputation)



# -------------------- INTRO PAGE --------------------

def page_intro():
    st.title("🚀 Startup Teamwork Quest")
    st.subheader("A teamwork & decision-making simulation")

    st.write("""
Welcome to **Startup Teamwork Quest** – a fast-paced scenario game where 
your team must handle pressure, limited time, and unexpected events.

### 🎯 Goal of the Game
Make decisions that balance:
- Team Morale  
- Budget  
- Client Reputation  

### ⏳ Time Pressure
Each scenario has a **45-second timer**.  
If time runs out → your team **loses the ability to choose** and the scenario auto-fails.

### 👥 Roles
You will be randomly assigned a role with its own priorities.

### 🧠 Instructions
1. Read the scenario  
2. Discuss briefly (optional)  
3. Choose fast  
4. Live with the consequences 😈  

Ready?
""")

    if st.button("Assign my role ➜"):
        st.session_state.step = "role"
        st.rerun()



# -------------------- ROLE ASSIGNMENT --------------------

import random

def page_role():
    st.title("🎲 Your Role")

    roles = {
        "Marketing Manager": {
            "focus": "Keep the client happy and grow visibility.",
            "secret": "You feel successful if Reputation ends high.",
        },
        "Tech Lead": {
            "focus": "Deliver a stable product without burning out the team.",
            "secret": "High morale = high success.",
        },
        "Finance Lead": {
            "focus": "Make sure the project stays within budget.",
            "secret": "Healthy budget is your priority.",
        },
    }

    if st.session_state.role is None:
        st.session_state.role = random.choice(list(roles.keys()))

    role = st.session_state.role
    info = roles[role]

    st.success(f"Your role is: **{role}**")
    st.info(f"**Focus:** {info['focus']}\n\n**Secret preference:** {info['secret']}")

    if st.button("Start Scenario 1 ➜"):
        start_timer()
        st.session_state.step = "s1"
        st.rerun()



# -------------------- SCENARIO TEMPLATE --------------------

def show_timer():
    remaining = time_left()
    if remaining == 0:
        st.error("⏳ Time's up! You did not choose in time.")
    else:
        st.warning(f"⏰ Time left: **{remaining} seconds**")


# -------------------- SCENARIO 1 --------------------

def page_s1():
    st.title("Scenario 1 – First Big Decision")
    show_stats()
    show_timer()
    st.write("---")

    st.write("""
Your startup has limited resources before the investor meeting.

Do you:
- Build a simple working prototype?
- Create flashy marketing material?
- Try doing both under pressure?
""")

    choice = st.radio("Make a choice:", [
        "Focus on a simple working prototype.",
        "Focus on flashy marketing material.",
        "Try to do both at the same time.",
    ])

    disabled = timer_expired()

    if st.button("Confirm Scenario 1 choice", disabled=disabled):
        if disabled:
            st.error("Too late! Timer expired.")
        elif choice == "Focus on a simple working prototype.":
            apply_deltas("Scenario 1", choice, 1, -1, 1)
        elif choice == "Focus on flashy marketing material.":
            apply_deltas("Scenario 1", choice, -1, -1, 2)
        else:
            apply_deltas("Scenario 1", choice, -2, -2, 2)

        start_timer()
        st.session_state.step = "s2"
        st.rerun()



# -------------------- SCENARIO 2 --------------------

def page_s2():
    st.title("Scenario 2 – Team Conflict")
    show_stats()
    show_timer()
    st.write("---")

    st.write("""
Two team members disagree strongly:
- Developer: The timeline is impossible  
- Marketing: Promised features must ship  

Tension is rising.
""")

    choice = st.radio("Make a choice:", [
        "Hold a mediation meeting and renegotiate scope.",
        "Let them resolve it on their own.",
        "Reassign one to another task.",
    ])

    disabled = timer_expired()

    if st.button("Confirm Scenario 2 choice", disabled=disabled):
        if disabled:
            st.error("Too late! Timer expired.")
        elif choice == "Hold a mediation meeting and renegotiate scope.":
            apply_deltas("Scenario 2", choice, 2, -1, 0)
        elif choice == "Let them resolve it on their own.":
            apply_deltas("Scenario 2", choice, -2, 0, -1)
        else:
            apply_deltas("Scenario 2", choice, -1, 0, 1)

        start_timer()
        st.session_state.step = "s3"
        st.rerun()



# -------------------- SCENARIO 3 --------------------

def page_s3():
    st.title("Scenario 3 – Last-Minute Client Request")
    show_stats()
    show_timer()
    st.write("---")

    st.write("""
Two days before the demo, the client asks for an extra feature 
that was never agreed upon.

What do you do?
""")

    choice = st.radio("Your choice:", [
        "Accept the request and squeeze it in.",
        "Push back and protect the team.",
        "Accept but charge extra and reduce something else.",
    ])

    disabled = timer_expired()

    if st.button("Confirm Scenario 3 choice", disabled=disabled):
        if disabled:
            st.error("Too late! Timer expired.")
        elif choice == "Accept the request and squeeze it in.":
            apply_deltas("Scenario 3", choice, -2, -1, 2)
        elif choice == "Push back and protect the team.":
            apply_deltas("Scenario 3", choice, 1, 0, -1)
        else:
            apply_deltas("Scenario 3", choice, -1, 2, 1)

        st.session_state.step = "summary"
        st.rerun()

# -------------------- SCENARIO 4 --------------------

def page_s4():
    st.title("Scenario 4 – Unexpected Bug Crisis")
    show_stats()
    show_timer()
    st.write("---")

    st.write("""
A critical bug appears during testing. It could delay the demo.

What do you do?
""")

    choice = st.radio("Your choice:", [
        "Pull an all-nighter to fix it before demo.",
        "Delay the demo and fix it properly.",
        "Patch it quickly and hope for the best."
    ])

    disabled = timer_expired()

    if st.button("Confirm Scenario 4 choice", disabled=disabled):
        if disabled:
            st.error("Too late! Timer expired.")
        elif choice == "Pull an all-nighter to fix it before demo.":
            apply_deltas("Scenario 4", choice, -2, 0, 2)
        elif choice == "Delay the demo and fix it properly.":
            apply_deltas("Scenario 4", choice, 1, -1, -1)
        else:
            apply_deltas("Scenario 4", choice, -1, 0, 1)

        start_timer()
        st.session_state.step = "s5"
        st.rerun()

# -------------------- SCENARIO 5 --------------------

def page_s5():
    st.title("Scenario 5 – Team Motivation Dip")
    show_stats()
    show_timer()
    st.write("---")

    st.write("""
Half of the team feels demotivated after several stressful weeks.

How do you respond?
""")

    choice = st.radio("Your choice:", [
        "Organize a team-building activity.",
        "Offer a small bonus to encourage them.",
        "Ignore it and push through the deadline."
    ])

    disabled = timer_expired()

    if st.button("Confirm Scenario 5 choice", disabled=disabled):
        if disabled:
            st.error("Too late! Timer expired.")
        elif choice == "Organize a team-building activity.":
            apply_deltas("Scenario 5", choice, 2, -1, 0)
        elif choice == "Offer a small bonus to encourage them.":
            apply_deltas("Scenario 5", choice, 1, -2, 1)
        else:
            apply_deltas("Scenario 5", choice, -2, 0, 0)

        start_timer()
        st.session_state.step = "s6"
        st.rerun()

# -------------------- SCENARIO 6 --------------------

def page_s6():
    st.title("Scenario 6 – Investor Pressure")
    show_stats()
    show_timer()
    st.write("---")

    st.write("""
Your main investor pressures you to commit to ambitious new features,
threatening to reduce funding if you refuse.

How do you react?
""")

    choice = st.radio("Your choice:", [
        "Agree to the new roadmap to secure funding.",
        "Push back and protect realistic planning.",
        "Negotiate a smaller feature set."
    ])

    disabled = timer_expired()

    if st.button("Confirm Scenario 6 choice", disabled=disabled):
        if disabled:
            st.error("Too late! Timer expired.")
        elif choice == "Agree to the new roadmap to secure funding.":
            apply_deltas("Scenario 6", choice, -2, 2, 1)
        elif choice == "Push back and protect realistic planning.":
            apply_deltas("Scenario 6", choice, 1, 0, -2)
        else:
            apply_deltas("Scenario 6", choice, 0, 1, 1)

        st.session_state.step = "summary"
        st.rerun()

# -------------------- SUMMARY --------------------

def page_summary():
    st.title("📊 Final Project Outcome")
    show_stats()
    st.write("---")

    morale = st.session_state.morale
    budget = st.session_state.budget
    reputation = st.session_state.reputation
    total = morale + budget + reputation
    role = st.session_state.get("role", "Team Member")

    # Overall ending text
    if total >= 18:
        ending = "High cohesion & sustainable success 🎉"
        overall = (
            "Your team managed to balance morale, money, and reputation. "
            "People would probably work with you again – and the client is happy."
        )
    elif total >= 12:
        ending = "Mixed outcome – some wins, some scars 😐"
        overall = (
            "You got through the project, but there were trade-offs. "
            "Some relationships or expectations may need repair before the next round."
        )
    else:
        ending = "Low cohesion – fragile success or quiet failure 😬"
        overall = (
            "Even if something was delivered, the way you worked together "
            "was not really sustainable. In a real startup, people might quit "
            "or clients might not return."
        )

    st.header(ending)
    st.write(overall)
    st.write("---")

    # --- Detailed feedback based on stats ---

    strengths = []
    improvements = []

    # Morale feedback
    if morale >= 7:
        strengths.append(
            "You protected **team morale** – people were likely to stay motivated and engaged."
        )
    elif morale <= 4:
        improvements.append(
            "Watch out for **morale** – some of your choices risked overloading or frustrating the team."
        )
    else:
        improvements.append(
            "Team morale ended up in a **medium zone** – consider where small changes "
            "could have reduced stress without breaking the project."
        )

    # Budget feedback
    if budget >= 7:
        strengths.append(
            "You kept the **budget under control**, which makes the project more sustainable long-term."
        )
    elif budget <= 4:
        improvements.append(
            "Your **budget** is under pressure – in reality this might limit future options or cause hard cuts."
        )
    else:
        improvements.append(
            "The **budget** is borderline – next time you might define trade-offs earlier "
            "so surprises hurt less."
        )

    # Reputation feedback
    if reputation >= 7:
        strengths.append(
            "You managed to build strong **client reputation**, which helps with trust and future projects."
        )
    elif reputation <= 4:
        improvements.append(
            "Your **client reputation** took some hits – think about how to communicate constraints "
            "without losing too much trust."
        )
    else:
        improvements.append(
            "Client **reputation** ended up okay but not amazing – clearer expectation setting early on "
            "could improve this."
        )

    # Role-based feedback
    if role == "Finance Lead":
        if budget >= max(morale, reputation):
            strengths.append(
                "As **Finance Lead**, you stayed true to your role by prioritising financial stability."
            )
        else:
            improvements.append(
                "As **Finance Lead**, you might want to keep a closer eye on the budget next time."
            )
    elif role == "Marketing Manager":
        if reputation >= max(morale, budget):
            strengths.append(
                "As **Marketing Manager**, you succeeded in keeping the client/front-facing side strong."
            )
        else:
            improvements.append(
                "As **Marketing Manager**, you could push a bit more on communication and client perception."
            )
    elif role == "Tech Lead":
        if morale >= max(budget, reputation):
            strengths.append(
                "As **Tech Lead**, you did well in protecting the team's capacity and avoiding burnout."
            )
        else:
            improvements.append(
                "As **Tech Lead**, you may want to watch for signs of overload or unrealistic plans earlier."
            )

    # Show strengths
    st.subheader("✅ What you did well")
    if strengths:
        for s in strengths:
            st.markdown(f"- {s}")
    else:
        st.write("No clear strengths were identified – this run was more of a warning scenario. 🙂")

    # Show improvements
    st.subheader("🛠 What you could improve next time")
    if improvements:
        for imp in improvements:
            st.markdown(f"- {imp}")
    else:
        st.write("You balanced everything very well – next time you could experiment with riskier choices.")

    st.write("---")
    st.write("### Your decisions during the game")
    for h in st.session_state.history:
        st.markdown(
            f"- **{h['scenario']}** – *{h['choice']}*  \n"
            f"  Δ morale: {h['Δ morale']} | "
            f"Δ budget: {h['Δ budget']} | "
            f"Δ reputation: {h['Δ reputation']}"
        )

    if st.button("Restart game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# -------------------- ROUTER --------------------

step = st.session_state.step

if step == "intro":
    page_intro()
elif step == "role":
    page_role()
elif step == "s1":
    page_s1()
elif step == "s2":
    page_s2()
elif step == "s3":
    page_s3()
elif step == "s4":
    page_s4()
elif step == "s5":
    page_s5()
elif step == "s6":
    page_s6()
elif step == "summary":
    page_summary()

