import streamlit as st
import datetime
import json
import os
import pandas as pd
import altair as alt

import streamlit as st

css = r"""
@custom-variant dark (&:is(.dark *));

:root {
  --font-size: 16px;
  --background: #ffffff;
  --foreground: oklch(0.145 0 0);
  --card: #ffffff;
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: #22c55e;
  --primary-foreground: oklch(1 0 0);
  --secondary: oklch(0.95 0.0058 264.53);
  --secondary-foreground: #030213;
  --muted: #ececf0;
  --muted-foreground: #717182;
  --accent: #e9ebef;
  --accent-foreground: #030213;
  --destructive: #d4183d;
  --destructive-foreground: #ffffff;
  --border: rgba(0, 0, 0, 0.1);
  --input: transparent;
  --input-background: #f3f3f5;
  --switch-background: #cbced4;
  --font-weight-medium: 500;
  --font-weight-normal: 400;
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --radius: 0.625rem;
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: #030213;
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.145 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.396 0.141 25.723);
  --destructive-foreground: oklch(0.637 0.237 25.331);
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);
  --chart-1: oklch(0.488 0.243 264.376);
  --chart-2: oklch(0.696 0.17 162.48);
  --chart-3: oklch(0.769 0.188 70.08);
  --chart-4: oklch(0.627 0.265 303.9);
  --chart-5: oklch(0.645 0.246 16.439);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(0.269 0 0);
  --sidebar-ring: oklch(0.439 0 0);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-input-background: var(--input-background);
  --color-switch-background: var(--switch-background);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);
}

@layer base {
  * {
    @apply border-border outline-ring/50;
  }

  body {
    @apply bg-background text-foreground;
  }
}

@layer base {
  :where(:not(:has([class*=' text-']), :not(:has([class^='text-'])))) {
    h1 {
      font-size: var(--text-2xl);
      font-weight: var(--font-weight-medium);
      line-height: 1.5;
    }

    h2 {
      font-size: var(--text-xl);
      font-weight: var(--font-weight-medium);
      line-height: 1.5;
    }

    h3 {
      font-size: var(--text-lg);
      font-weight: var(--font-weight-medium);
      line-height: 1.5;
    }

    h4 {
      font-size: var(--text-base);
      font-weight: var(--font-weight-medium);
      line-height: 1.5;
    }

    p {
      font-size: var(--text-base);
      font-weight: var(--font-weight-normal);
      line-height: 1.5;
    }

    label {
      font-size: var(--text-base);
      font-weight: var(--font-weight-medium);
      line-height: 1.5;
    }

    button {
      font-size: var(--text-base);
      font-weight: var(--font-weight-medium);
      line-height: 1.5;
    }

    input {
      font-size: var(--text-base);
      font-weight: var(--font-weight-normal);
      line-height: 1.5;
    }
  }
}

html {
  font-size: var(--font-size);
}
"""

st.markdown("""
    <style>

    /* Global page width */
    .main {
        max-width: 420px;      /* iPhone width */
        margin: 0 auto;
        padding-top: 20px;
    }

    /* Uniform card container */
    .water-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 22px;
        box-shadow: 0px 4px 22px rgba(0,0,0,0.08);
        margin-bottom: 30px;
    }

    /* Page title style */
    h1 {
        font-size: 28px !important;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 25px;
        font-weight: 700;
    }

    /* Subtitles */
    h2, h3 {
        text-align: center;
        margin-bottom: 10px;
    }

    /* Inputs consistent width */
    .stNumberInput, .stSelectbox {
        width: 100% !important;
    }

    /* Buttons full width */
    button[kind="secondary"], button[kind="primary"] {
        width: 100% !important;
        border-radius: 12px;
        height: 48px;
        font-size: 18px;
    }

    /* Progress bar height */
    .stProgress > div > div {
        height: 16px !important;
        border-radius: 10px !important;
    }

    /* Metrics sizing */
    .stMetric {
        text-align: center !important;
        font-size: 20px !important;
    }

    /* Remove Streamlit padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }

    </style>
""", unsafe_allow_html=True)

# --------------------------
# Persistent Storage
# --------------------------
DATA_FILE = "water_state.json"

def load():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE, "r"))
    return {
        "page": 1,
        "age": None,
        "height": None,
        "weight": None,
        "bmi": None,
        "condition": None,
        "goal": None,
        "intake": {},
    }

def save(state):
    json.dump(state, open(DATA_FILE, "w"), indent=4)

state = load()

# --------------------------
# Helpers
# --------------------------
def calc_bmi(h, w):
    return round(w / ((h / 100) ** 2), 2)

def base_water_requirement(bmi):
    """Default requirement using BMI."""
    if bmi < 18.5:
        return 2500
    elif bmi < 25:
        return 3000
    else:
        return 3500

def apply_condition_adjustment(ml, condition):
    adj = {
        "Normal / Healthy": 0,
        "Athletic": +800,
        "Summer / Hot Climate": +600,
        "Pregnancy / Nursing": +700,
        "Heart / Kidney Issues": -500,
        "Diabetic": +300,
    }
    return max(1200, ml + adj.get(condition, 0))

def today_key():
    return str(datetime.date.today())

def record_intake(amount):
    day = today_key()
    if day not in state["intake"]:
        state["intake"][day] = 0
    state["intake"][day] += amount
    save(state)

# --------------------------
# PAGE 1 — Welcome
# --------------------------
if state["page"] == 1:
    st.title("💧 Welcome to Water Buddy")
    st.subheader("Track your hydration, personalised using BMI + health factors.")

    st.write("Enter your **age**, then click next →")

    age = st.number_input("Age", min_value=5, max_value=100, value=state.get("age") or 18)

    if st.button("Next"):
        state["age"] = age
        state["page"] = 2
        save(state)
        st.rerun()

# --------------------------
# PAGE 2 — Enter Height & Weight
# --------------------------
elif state["page"] == 2:
    st.title("📏 Body Metrics")

    height = st.number_input("Height (cm)", value=state.get("height") or 170)
    weight = st.number_input("Weight (kg)", value=state.get("weight") or 65)

    if st.button("Calculate BMI"):
        bmi = calc_bmi(height, weight)
        state["height"] = height
        state["weight"] = weight
        state["bmi"] = bmi
        state["page"] = 3
        save(state)
        st.rerun()

# --------------------------
# PAGE 3 — Health Condition
# --------------------------
elif state["page"] == 3:
    st.title("❤️ Health Profile")

    conditions = [
        "Normal / Healthy",
        "Athletic",
        "Summer / Hot Climate",
        "Pregnancy / Nursing",
        "Heart / Kidney Issues",
        "Diabetic"
    ]

    condition = st.selectbox("Select Health Condition:", conditions)

    if st.button("Next →"):
        # Compute water goal
        base = base_water_requirement(state["bmi"])
        final = apply_condition_adjustment(base, condition)

        state["condition"] = condition
        state["goal"] = final
        state["page"] = 4
        save(state)
        st.rerun()

# --------------------------
# PAGE 4 — Water Tracker
# --------------------------
elif state["page"] == 4:
    st.title("🚰 Daily Water Tracker")

    goal = state["goal"]
    today = today_key()
    current = state["intake"].get(today, 0)

    st.metric("Daily Goal", f"{goal} ml")
    st.metric("Consumed", f"{current} ml")
    st.metric("Remaining", f"{max(goal - current, 0)} ml")

    st.progress(min(current / goal, 1.0))

    add = st.number_input("Add Water (ml)", value=250, step=50)

    if st.button("Add"):
        record_intake(add)
        st.rerun()

    if current >= goal:
        st.success("🎉 GOAL REACHED!")
        st.balloons()

    if st.button("View Weekly History →"):
        state["page"] = 5
        save(state)
        st.rerun()

    if st.button("Reset App"):
        os.remove(DATA_FILE)
        st.rerun()

# --------------------------
# PAGE 5 — Weekly History
# --------------------------
elif state["page"] == 5:
    st.title("📊 Weekly History")

    today = datetime.date.today()
    rows = []

    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        s = str(d)
        rows.append({"date": s, "water": state["intake"].get(s, 0)})

    df = pd.DataFrame(rows)

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="date:T",
            y="water:Q"
        )
    )
    st.altair_chart(chart, use_container_width=True)

    if st.button("Back to Tracker"):
        state["page"] = 4
        save(state)
        st.rerun()
