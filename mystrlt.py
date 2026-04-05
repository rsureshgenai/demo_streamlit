import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Calorie App", layout="wide")

# ======================
# 🎨 CSS
# ======================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}

.sidebar-title {
    padding-left: 18px;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 15px;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left;
    padding: 10px 16px;
    background: transparent;
    color: #e5e7eb;
    border: none;
    border-radius: 10px;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #111827;
}

section[data-testid="stSidebar"] .stButton > button:focus {
    background-color: #1f2937;
}

section[data-testid="stSidebar"] button p {
    display: inline;
}
</style>
""", unsafe_allow_html=True)

# ======================
# 📌 SIDEBAR
# ======================
st.sidebar.markdown('<div class="sidebar-title">🔥 Calorie App</div>', unsafe_allow_html=True)

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

def nav(label, key):
    if st.sidebar.button(label):
        st.session_state.menu = key

nav("➕ Add Food", "Add Food")
nav("🏠 Dashboard", "Dashboard")
nav("📜 History", "History")
nav("📊 Analytics", "Analytics")
nav("⚙️ Settings", "Settings")

menu = st.session_state.menu

# ======================
# 📦 INIT DATA
# ======================
if "history" not in st.session_state:
    food_list = ["Idli", "Dosa", "Biryani", "Pongal", "Chapati"]

    data = []
    for i in range(60):
        date = (datetime.today() - timedelta(days=i)).date()

        for _ in range(random.randint(1, 3)):
            food = random.choice(food_list)
            calories = random.randint(80, 400)

            data.append({
                "Date": date,
                "Food": food,
                "Count": f"{random.randint(1,3)} serving",
                "Calories": calories
            })

    st.session_state.history = data

if "total" not in st.session_state:
    st.session_state.total = sum([x["Calories"] for x in st.session_state.history if x["Date"] == datetime.today().date()])

# ======================
# 🧠 HEADER
# ======================
st.markdown("# 🔥 Smart Food Calorie Tracker")
st.markdown("### 👋 Hi Suresh")
st.caption("Stay consistent with your fitness goals 🚀")

# ======================
# 👤 PROFILE
# ======================
col1, col2, col3, col4, col5 = st.columns(5)

age = col1.number_input("Age", 10, 80, 25)
gender = col2.selectbox("Gender", ["Male", "Female"])
weight = col3.number_input("Weight (kg)", 30, 150, 70)
height = col4.number_input("Height (cm)", 120, 220, 170)
activity = col5.selectbox("Activity", ["Sedentary", "Moderate", "Active"])

# ======================
# 🔥 CALC
# ======================
activity_map = {"Sedentary": 1.2, "Moderate": 1.55, "Active": 1.725}

bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)
goal = int(bmr * activity_map[activity])

today = datetime.today().date()
df_all = pd.DataFrame(st.session_state.history)

today_df = df_all[df_all["Date"] == today]
consumed = today_df["Calories"].sum()

remaining = max(goal - consumed, 0)
progress = min(consumed / goal if goal else 0, 1.0)

# ======================
# ➕ ADD FOOD
# ======================
if menu == "Add Food":

    df = pd.DataFrame([
        {"Food": "Idli", "Calories": 58, "Unit": "piece"},
        {"Food": "Dosa", "Calories": 168, "Unit": "piece"},
        {"Food": "Biryani", "Calories": 300, "Unit": "plate"},
    ])

    food = st.selectbox("Select Food", df["Food"])
    qty = st.number_input("Quantity", 1, 10, 1)

    selected = df[df["Food"] == food].iloc[0]
    total_cal = selected["Calories"] * qty

    st.metric("Calories", total_cal)

    if st.button("➕ Add Food"):
        st.session_state.history.append({
            "Date": today,
            "Food": food,
            "Count": f"{qty} {selected['Unit']}",
            "Calories": total_cal
        })
        st.success("Added for Today ✅")

# ======================
# 📊 DASHBOARD
# ======================
elif menu == "Dashboard":

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🔥 Goal", goal)
    c2.metric("🍽 Today Consumed", consumed)
    c3.metric("⚡ Remaining", remaining)
    c4.metric("📊 Progress", f"{int(progress*100)}%")

    st.progress(progress)

# ======================
# 📜 HISTORY
# ======================
elif menu == "History":

    df = df_all.sort_values("Date", ascending=False)

    st.dataframe(df, use_container_width=True)

    st.markdown(f"### 🔥 Total Calories: {df['Calories'].sum()} kcal")

# ======================
# 📈 ANALYTICS
# ======================
elif menu == "Analytics":

    st.subheader("📅 Last 60 Days Calories Trend")

    daily = df_all.groupby("Date")["Calories"].sum().reset_index()
    daily = daily.sort_values("Date")

    st.line_chart(daily.set_index("Date"))

    st.subheader("🍛 Food Distribution")
    food_dist = df_all.groupby("Food")["Calories"].sum()
    st.bar_chart(food_dist)

# ======================
# ⚙️ SETTINGS
# ======================
elif menu == "Settings":

    if st.button("🔄 Reset Data"):
        st.session_state.history = []
        st.success("Reset Done ✅")