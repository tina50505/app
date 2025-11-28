import streamlit as st
import random

# -------------------- CONFIG --------------------

st.set_page_config(page_title="Startup Teamwork Quest", page_icon="🚀")

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.step = "intro"    # "intro", "role", "s1"..."s5", "summary"
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


def show_role_badge():
    """Show role + points in a compact HUD in the top-right corner."""
    role = st.session_state.get("role")
    if not role:
        return

    morale = st.session_state.morale
    budget = st.session_state.budget
    reputation = st.session_state.reputation
    total = morale + budget + reputation

    _, col = st.columns([3, 1])
    with col:
        st.markdown(
            f"""
            <div style="
                text-align:right;
                background-color:#11111122;
                padding:0.6rem 0.8rem;
                border-radius:0.6rem;
                font-size:0.9rem;
                line-height:1.4;
            ">
            <b>{role}</b><br>
            💙 {morale} &nbsp;&nbsp; 💰 {budget} &nbsp;&nbsp; ⭐ {reputation}<br>
            <b>Total: {total}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )


# -------------------- INTRO PAGE --------------------

def page_intro():
    st.title("🚀 Startup Teamwork Quest")
    st.subheader("A teamwork & decision-making simulation")

    st.write("""
Welcome to **Startup Teamwork Quest** – a scenario game where 
your team has to juggle pressure, limited resources, and unexpected events.

### 🎯 Goal of the Game
Make decisions that balance:
- **Team Morale**  
- **Budget**  
- **Client Reputation**  

### 👥 Roles
You will be **assigned a role** with its own priorities  
(even if the others don’t know them 😉).

### 🧠 How it works
1. Get your role  
2. Go through several scenarios  
3. Make choices together  
4. See how your decisions affected the project in the final summary
""")

    if st.button("Assign my role ➜"):
        st.session_state.step = "role"
        st.rerun()


# -------------------- ROLE ASSIGNMENT --------------------

def page_role():
    show_role_badge()
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

    st.write(
        "You’ll keep this role for the whole game. "
        "Try to make decisions that fit your priorities, "
        "but remember you’re still part of a team."
    )

    if st.button("Start Scenario 1 ➜"):
        st.session_state.step = "s1"
        st.rerun()


# -------------------- SCENARIO 1 --------------------

def page_s1():
    show_role_badge()
    st.title("Scenario 1 – First Big Decision")
    show_stats()
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

    if st.button("Confirm Scenario 1 choice"):
        if choice == "Focus on a simple working prototype.":
            apply_deltas("Scenario 1", choice, 1, -1, 1)
        elif choice == "Focus on flashy marketing material.":
            apply_deltas("Scenario 1", choice, -1, -1, 2)
        else:
            apply_deltas("Scenario 1", choice, -2, -2, 2)

        st.session_state.step = "s2"
        st.rerun()


# -------------------- SCENARIO 2 --------------------

def page_s2():
    show_role_badge()
    st.title("Scenario 2 – Team Conflict")
    show_stats()
    st.write("---")

    st.write("""
Two key team members disagree strongly:
- **Developer**: “The timeline is impossible.”  
- **Marketing**: “We already promised these features.”  

Tension is rising and the rest of the team is watching how you handle it.
""")

    choice = st.radio("Make a choice:", [
        "Hold a mediation meeting and renegotiate scope.",
        "Let them resolve it on their own.",
        "Reassign one of them to another task.",
    ])

    if st.button("Confirm Scenario 2 choice"):
        if choice == "Hold a mediation meeting and renegotiate scope.":
            apply_deltas("Scenario 2", choice, 2, -1, 0)
        elif choice == "Let them resolve it on their own.":
            apply_deltas("Scenario 2", choice, -2, 0, -1)
        else:
            apply_deltas("Scenario 2", choice, -1, 0, 1)

        st.session_state.step = "s3"
        st.rerun()


# -------------------- SCENARIO 3 --------------------

def page_s3():
    show_role_badge()
    st.title("Scenario 3 – Last-Minute Client Request")
    show_stats()
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

    if st.button("Confirm Scenario 3 choice"):
        if choice == "Accept the request and squeeze it in.":
            apply_deltas("Scenario 3", choice, -2, -1, 2)
        elif choice == "Push back and protect the team.":
            apply_deltas("Scenario 3", choice, 1, 0, -1)
        else:
            apply_deltas("Scenario 3", choice, -1, 2, 1)

        st.session_state.step = "s4"
        st.rerun()


# -------------------- SCENARIO 4 --------------------

def page_s4():
    show_role_badge()
    st.title("Scenario 4 – Pivot or Commit?")
    show_stats()
    st.write("---")

    st.write("""
After some user tests, you discover that people use your app for a 
**slightly different purpose** than planned.

An investor suggests you **pivot** the product to match this new use case, 
but that means throwing away some of the work you already did.

What do you decide?
""")

    choice = st.radio("Your choice:", [
        "Commit to the original plan – no pivot.",
        "Full pivot to the new use case.",
        "Small pivot: keep core, adjust features gradually.",
    ])

    if st.button("Confirm Scenario 4 choice"):
        if choice == "Commit to the original plan – no pivot.":
            apply_deltas("Scenario 4", choice, 0, 1, -1)
        elif choice == "Full pivot to the new use case.":
            apply_deltas("Scenario 4", choice, -1, -2, 2)
        else:
            apply_deltas("Scenario 4", choice, 1, -1, 1)

        st.session_state.step = "s5"
        st.rerun()


# -------------------- SCENARIO 5 --------------------

def page_s5():
    show_role_badge()
    st.title("Scenario 5 – Burnout or Scale Up?")
    show_stats()
    st.write("---")

    st.write("""
The app is gaining traction. The client is happy and more requests are coming in.

However, the team is clearly tired. People are working late and small bugs 
keep slipping through.

You have the option to:
""")

    choice = st.radio("Your choice:", [
        "Push the current team harder to keep momentum.",
        "Slow down delivery to let the team recover.",
        "Hire freelancers/consultants and accept higher costs.",
    ])

    if st.button("Confirm Scenario 5 choice"):
        if choice == "Push the current team harder to keep momentum.":
            apply_deltas("Scenario 5", choice, -2, 0, 2)
        elif choice == "Slow down delivery to let the team recover.":
            apply_deltas("Scenario 5", choice, 2, 0, -1)
        else:
            apply_deltas("Scenario 5", choice, 0, -2, 1)

        st.session_state.step = "summary"
        st.rerun()


# -------------------- SUMMARY --------------------

def page_summary():
    show_role_badge()
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
            "Team morale ended up in a **medium zone** – small tweaks could have reduced stress."
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
            "The **budget** is borderline – next time you might define trade-offs earlier."
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
            "Client **reputation** is okay but not amazing – clearer expectations early on could help."
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
                "As **Marketing Manager**, you kept the client/front-facing side strong."
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
elif step == "summary":
    page_summary()
