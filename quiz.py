import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="Smart Quiz Pro", layout="centered")

# ---------- SOUND ----------
def play_sound(correct=True):
    sound_url = "https://www.soundjay.com/buttons/sounds/button-4.mp3" if correct else \
                "https://www.soundjay.com/buttons/sounds/button-10.mp3"

    st.markdown(f"""
    <audio autoplay style="display:none">
        <source src="{sound_url}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}
.glass {
    background: rgba(255,255,255,0.06);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

# ---------- INTRO ----------
if st.session_state.stage == "intro":
    st.title("🧠 Smart Quiz Pro")

    name = st.text_input("Enter your name 👇")

    if st.button("Start Quiz"):
        if name.strip() == "":
            st.warning("Please enter your name")
        else:
            st.session_state.user_name = name
            st.session_state.stage = "quiz"
            st.session_state.index = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.result = None
            st.session_state.result_time = None
            st.session_state.history = []
            st.session_state.leaderboard = []
            st.rerun()

# ---------- QUESTIONS ----------
questions = [
    {"q": "Capital of India?", "opt": ["Mumbai","Delhi","Chennai","Kolkata"], "ans": "Delhi"},
    {"q": "Python used for?", "opt": ["Web","AI","Data","All"], "ans": "All"},
    {"q": "CPU stands for?", "opt": ["Central Unit","Central Processing Unit","Control Unit","Computer Unit"], "ans": "Central Processing Unit"},
    {"q": "2+2=?", "opt": ["3","4","5","6"], "ans": "4"},
    {"q": "Sun rises from?", "opt": ["West","East","North","South"], "ans": "East"},
    {"q": "HTML is?", "opt": ["Language","Framework","DB","OS"], "ans": "Language"},
    {"q": "1 byte = ?", "opt": ["4 bits","8 bits","16 bits","32 bits"], "ans": "8 bits"},
    {"q": "Google is?", "opt": ["Search Engine","OS","Browser","App"], "ans": "Search Engine"},
    {"q": "India currency?", "opt": ["Dollar","Euro","Rupee","Yen"], "ans": "Rupee"},
    {"q": "Which is programming language?", "opt": ["Python","HTML","CSS","All"], "ans": "Python"},
]

# ---------- QUIZ ----------
if st.session_state.stage == "quiz":

    st.title("🧠 Smart Quiz Pro")

    # ✅ LEFT ALIGNED NAME
    st.markdown(f"""
    <div style="color:#94a3b8;margin-top:-5px;margin-bottom:15px;font-size:16px;">
        👤 <b>{st.session_state.user_name}</b> • Play Well 🚀
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.index >= len(questions):
        st.session_state.stage = "result"
        st.rerun()

    q = questions[st.session_state.index]

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    st.progress((st.session_state.index + 1) / len(questions))
    st.subheader(f"Q{st.session_state.index+1}: {q['q']}")

    # TIMER
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = 20 - elapsed
    st.write(f"⏱ Time Left: {max(0, remaining)} sec")

    # RESULT
    if st.session_state.result:
        if time.time() - st.session_state.result_time < 2:
            if st.session_state.result == "correct":
                st.success("🎉 Correct!")
                st.balloons()
                play_sound(True)
            else:
                st.error(f"❌ Wrong! Correct: {q['ans']}")
                play_sound(False)
        else:
            st.session_state.index += 1
            st.session_state.start_time = time.time()
            st.session_state.result = None
            st.session_state.result_time = None
            st.rerun()

    else:
        answer = st.radio("Choose answer:", q["opt"], index=None)

        if st.button("Submit"):
            if answer is None:
                st.warning("⚠ Please select an answer!")
            else:
                correct = answer == q["ans"]

                if correct:
                    st.session_state.score += 1
                    st.session_state.result = "correct"
                else:
                    st.session_state.result = "wrong"

                st.session_state.history.append({
                    "Question": q["q"],
                    "Your Answer": answer,
                    "Correct Answer": q["ans"],
                    "Status": "Correct" if correct else "Wrong"
                })

                st.session_state.result_time = time.time()
                st.rerun()

    # TIMEOUT
    if remaining <= 0 and not st.session_state.result:
        st.session_state.index += 1
        st.session_state.start_time = time.time()
        st.rerun()

    time.sleep(1)
    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- RESULT ----------
if st.session_state.stage == "result":

    total = len(questions)
    score = st.session_state.score
    percent = int((score / total) * 100)

    st.success(f"🎉 {st.session_state.user_name}, Quiz Completed!")
    st.subheader(f"Score: {score}/{total} ({percent}%)")

    # Leaderboard
    st.session_state.leaderboard.append({
        "Name": st.session_state.user_name,
        "Score": score
    })

    df_leader = pd.DataFrame(st.session_state.leaderboard)
    df_leader = df_leader.sort_values(by="Score", ascending=False)

    st.markdown("### 🏆 Leaderboard")
    st.dataframe(df_leader, use_container_width=True)

    # Analytics
    st.markdown("### 📊 Analytics")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    st.write(f"✅ Correct: {len(df[df['Status']=='Correct'])}")
    st.write(f"❌ Wrong: {len(df[df['Status']=='Wrong'])}")

    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()