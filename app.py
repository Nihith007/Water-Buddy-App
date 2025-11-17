import streamlit as st
from PIL import Image, ImageDraw
from datetime import datetime

# ---------- Page Config ----------
st.set_page_config(page_title="WaterBuddy+", page_icon="💧", layout="centered")

# ---------- Design System CSS ----------
st.markdown("""
<style>
:root {
  --primary-blue: #3B82F6;
  --primary-cyan:  #06B6D4;
  --error-red:     #EF4444;
}
.huge-number { font-size: 42px; font-weight: 700; color: var(--primary-blue); }
.header-lg   { font-size: 28px; font-weight: 600; color: #0F172A; }
.header-md   { font-size: 22px; font-weight: 600; color: #0F172A; }
.caption     { font-size: 12px; color: #64748B; }
.card { padding: 1rem; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); background: #FFFFFF; }
[data-testid="stProgress"] div div { background: linear-gradient(90deg, var(--primary-blue), var(--primary-cyan)); }
</style>
""", unsafe_allow_html=True)

# ---------- Core Routines ----------
def compute_bmi(height_cm: float, weight_kg: float):
    """BMI + category + adjustment (-200, 0, +200)."""
    if height_cm <= 0 or weight_kg <= 0:
        return 0.0, "Invalid", 0
    h_m = height_cm / 100.0
    bmi = weight_kg / (h_m ** 2)
    if bmi < 18.5:
        return bmi, "Underweight", -200
    elif bmi <= 25:
        return bmi, "Normal", 0
    else:
        return bmi, "Overweight", 200

def age_base_goal(age: int) -> int:
    if 4 <= age <= 8: return 1200
    elif 9 <= age <= 13: return 1700
    elif 14 <= age <= 64: return 2000
    else: return 1700

def condition_adjustment(condition: str) -> int:
    return {
        "None": 0,
        "Athlete": 300,
        "Hot climate": 200,
        "Pregnant": 250,
        "Diabetic": 150,
        "Kidney/Heart": -300,
    }.get(condition, 0)

def personalized_goal(age: int, height: float, weight: float, condition: str):
    base = age_base_goal(age)
    bmi_val, bmi_cat, bmi_adj = compute_bmi(height, weight)
    cond_adj = condition_adjustment(condition)
    goal = max(500, base + bmi_adj + cond_adj)
    return {
        "goal": goal,
        "base": base,
        "bmi": round(bmi_val, 1),
        "bmi_cat": bmi_cat,
        "bmi_adj": bmi_adj,
        "cond_adj": cond_adj,
    }

def mascot(progress_pct: int):
    if progress_pct >= 100: return "🎉", "Amazing! You've reached your goal!"
    elif progress_pct >= 75: return "💪", "Almost there! Keep it up!"
    elif progress_pct >= 50: return "👍", "Great progress! You're halfway!"
    elif progress_pct >= 25: return "🌊", "Good start! Keep drinking!"
    else: return "💧", "Time to hydrate!"

def draw_bottle(progress_pct: float, width=220, height=420):
    """Simple water bottle with fill level using PIL."""
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    margin, neck_h = 20, 50
    top, bottom = margin, height - margin
    left, right = margin, width - margin
    # Neck
    neck_left, neck_right = width//2 - 35, width//2 + 35
    draw.rounded_rectangle([(neck_left, top), (neck_right, top + neck_h)],
                           radius=15, outline="#0ea5e9", width=3, fill=(255,255,255,255))
    # Body
    body_top = top + neck_h
    draw.rounded_rectangle([(left, body_top), (right, bottom)],
                           radius=30, outline="#0ea5e9", width=3, fill=(255,255,255,255))
    # Fill
    p = max(0, min(100, int(progress_pct)))
    fill_h = int((p / 100.0) * (bottom - body_top))
    fill_top = bottom - fill_h
    draw.rectangle([(left+3, fill_top), (right-3, bottom-3)], fill=(59,130,246,200))
    draw.line([(left+10, fill_top+12), (right-10, fill_top+12)], fill="#06b6d4", width=2)
    return img

# ---------- State ----------
if "profile" not in st.session_state:
    st.session_state.profile = {"age": 25, "height": 170.0, "weight": 65.0, "condition": "None"}
if "intake" not in st.session_state: st.session_state.intake = 0
if "tip_index" not in st.session_state: st.session_state.tip_index = 0
if "day" not in st.session_state: st.session_state.day = datetime.now().date()
if st.session_state.day != datetime.now().date():
    st.session_state.intake = 0
    st.session_state.day = datetime.now().date()

TIPS = [
    "Sip water regularly instead of chugging.",
    "Keep a bottle within reach to build the habit.",
    "Add slices of lemon or cucumber for flavour.",
    "Hydrate before and after exercise.",
    "Coffee/tea count, but plain water is best.",
    "Set mini-goals every hour to stay on track.",
]

# ---------- Header ----------
st.markdown("""
<div class="card" style="background:linear-gradient(135deg,#3B82F6,#06B6D4);color:white">
  <div class="header-lg">💧 WaterBuddy+</div>
  <div class="caption" style="color:#E0F2FE">Personalized Hydration with Age + BMI + Health Conditions</div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar Inputs ----------
st.sidebar.title("Profile")
age = st.sidebar.number_input("Age (years)", min_value=4, max_value=120, value=int(st.session_state.profile["age"]), step=1)
height = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=240.0, value=float(st.session_state.profile["height"]), step=0.5)
weight = st.sidebar.number_input("Weight (kg)", min_value=10.0, max_value=250.0, value=float(st.session_state.profile["weight"]), step=0.5)
condition = st.sidebar.selectbox("Health condition",
    ["None", "Athlete", "Hot climate", "Pregnant", "Diabetic", "Kidney/Heart"],
    index=["None", "Athlete", "Hot climate", "Pregnant", "Diabetic", "Kidney/Heart"].index(st.session_state.profile["condition"])
)
st.session_state.profile.update({"age": age, "height": height, "weight": weight, "condition": condition})

# ---------- Calculation ----------
calc = personalized_goal(age, height, weight, condition)
progress_pct = int(min(100, (st.session_state.intake / calc['goal']) * 100)) if calc['goal'] else 0

# ---------- Layout ----------
col1, col2 = st.columns([1,1])
with col1:
    st.markdown("<div class='header-md'>🎯 Personalized Daily Goal</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='huge-number'>{calc['goal']} ml</div>", unsafe_allow_html=True)
    st.progress(min(1.0, st.session_state.intake / calc['goal']))
    st.write("**Breakdown**")
    st.write(f"Base (age): **{calc['base']} ml**")
    st.write(f"BMI: {calc['bmi']} ({calc['bmi_cat']}) ➜ **{calc['bmi_adj']} ml**")
    st.write(f"Condition ({condition}): **{calc['cond_adj']} ml**")

with col2:
    st.image(draw_bottle(progress_pct), caption=f"Progress: {progress_pct}%", use_column_width=True)

# ---------- Metrics ----------
remaining = max(0, calc['goal'] - st.session_state.intake)
m1, m2, m3 = st.columns(3)
m1.metric("Intake", f"{st.session_state.intake} ml")
m2.metric("Remaining", f"{remaining} ml")
m3.metric("Progress", f"{progress_pct}%")

# ---------- Intake Actions ----------
a1, a2, a3 = st.columns([1,1,2])
if a1.button("➕ +250 ml"): st.session_state.intake = min(calc['goal'], st.session_state.intake + 250)
if a2.button("➕ +500 ml"): st.session_state.intake = min(calc['goal'], st.session_state.intake + 500)
with a3:
    custom = st.number_input("Custom amount (ml)", min_value=0, max_value=5000, value=0, step=50)
    if st.button("Add custom") and custom > 0:
        st.session_state.intake = min(calc['goal'], st.session_state.intake + int(custom))

# ---------- Mascot + Celebration ----------
emoji, msg = mascot(progress_pct)
st.success(f"{emoji} {msg}")
if progress_pct >= 100: st.balloons()

# ---------- Tips ----------
with st.expander("💡 Daily hydration tip"):
    tip = TIPS[st.session_state.tip_index % len(TIPS)]
    st.info(tip)
    c1, c2 = st.columns(2)
    if c1.button("Next tip"): st.session_state.tip_index += 1
    if c2.button("Previous tip"): st.session_state.tip_index = (st.session_state.tip_index - 1) % len(TIPS)

# ---------- Reset ----------
st.markdown("---")
r1, r2 = st.columns([2,2])
with r1:
    st.markdown("<div class='header-md'>🔄 New Day / Reset</div>", unsafe_allow_html=True)
    st.caption("Resets intake to 0. Your profile stays unchanged.")
with r2:
    confirm = st.checkbox("Confirm reset")
    if st.button("Reset now"):
        if confirm:
            st.session_state.intake = 0
            st.session_state.tip_index = 0
            st.toast("✅ Reset complete. New day—time to hydrate!", icon="💧")
        else:
            st.warning("Please tick 'Confirm reset' before resetting.")

# ---------- Disclaimer ----------
st.markdown("""
<div class="card" style="border-left: 6px solid var(--error-red)">
  <div class="header-md">⚕️ Medical disclaimer</div>
  <div class="body">If you have kidney or heart conditions—or any medical concerns—consult a qualified healthcare professional for individualized hydration guidance. This app provides general recommendations only.</div>
</div>
""", unsafe_allow_html=True)
