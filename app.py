import streamlit as st
from datetime import datetime
from PIL import Image, ImageDraw

# ---------------------------------------------------------------------
# Page config + global CSS (rounded cards, gradients, pill badges, etc.)
# ---------------------------------------------------------------------
st.set_page_config(page_title="WaterBuddy+", page_icon="💧", layout="centered")

st.markdown("""
<style>
:root{
  --blue:#3B82F6; --cyan:#06B6D4; --teal:#14B8A6;
  --green:#22C55E; --red:#EF4444; --orange:#F97316;
  --indigo:#6366F1; --purple:#A855F7; --gray:#64748B;
  --text:#0F172A; --muted:#94A3B8; --border:#E5E7EB;
}
body{color:var(--text);}
.card{border-radius:18px; background:#fff; border:1px solid var(--border);
      box-shadow:0 10px 30px rgba(0,0,0,.06); padding:18px;}
.card-soft{border-radius:18px; background:linear-gradient(135deg,#EBF5FF,#F0FDFA); padding:18px; border:1px solid var(--border);}
.pill{display:inline-block; border-radius:999px; padding:.3rem .8rem; border:1px solid #DCE7F7; background:#fff; color:#2563EB; font-weight:600;}
.huge{font-size:42px; font-weight:800; color:#0F172A;}
.h1{font-size:28px; font-weight:700;}
.h2{font-size:22px; font-weight:600;}
.kpi{font-size:16px; color:#0F172A;}
.kpi-val{font-weight:700;}
.kpi-blue{color:#2563EB;}
.kpi-green{color:#16A34A;}
.kpi-red{color:#DC2626;}
.btn-row button{height:54px; border-radius:14px; font-weight:700;}
.btn-blue{background:#2563EB; color:#fff; border:none;}
.btn-gray{background:#EEF2F7; color:#0F172A; border:none;}
.btn-teal{background:#06B6D4; color:#fff; border:none;}
input, .stNumberInput input{height:48px !important; border-radius:12px !important;}
.metric-sep{height:1px; background:#EEF2F7; margin:8px 0 16px;}
.mascot{border-radius:999px; width:72px; height:72px; background:#F1F5FB; display:flex; align-items:center; justify-content:center; margin:auto; box-shadow:0 10px 30px rgba(0,0,0,.06);}
.banner{margin-top:-14px; text-align:center;}
.gradient-card{border-radius:22px; border:1px solid #E4ECF7; padding:16px;
  background:linear-gradient(135deg,#E7F3FF,#E8FFF9);}
.bottle-frame{border-radius:22px; border:3px solid #2E66F0; padding:14px; background:#fff;}
.badge-note{background:#F8FAFF; color:#2563EB; border:1px solid #DCE7F7; border-radius:999px; padding:.4rem .9rem; display:inline-block;}
.tip{border-radius:12px; background:#F8F5FF; color:#7C3AED; padding:12px; border:1px solid #E9D5FF;}
.warning{border-radius:12px; background:#FEF2F2; color:#DC2626; padding:12px; border:1px solid #FECACA;}
.reset-dialog{padding:0;}
.reset-head{color:#DC2626; font-weight:800; font-size:22px; text-align:center;}
.reset-row{display:flex; gap:12px;}
.reset-cancel{flex:1; background:#EEF2F7; border:none; border-radius:12px; padding:12px; font-weight:700;}
.reset-go{flex:1; background:#DC2626; color:#fff; border:none; border-radius:12px; padding:12px; font-weight:800;}
/* progress bar color */
[data-testid="stProgress"] div div{background:linear-gradient(90deg,#3B82F6,#06B6D4);}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Hydration calculations (Age + BMI + Condition)
# ---------------------------------------------------------------------
def compute_bmi(height_cm: float, weight_kg: float):
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
        "Normal / Healthy": 0,
        "Athlete / High Activity": 300,
        "Hot Climate": 200,
        "Pregnant": 250,
        "Diabetic": 150,
        "Kidney / Heart": -300,
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
    if progress_pct >= 100: return "🎉", "Amazing!"
    elif progress_pct >= 75: return "💪", "Almost there!"
    elif progress_pct >= 50: return "👍", "Great progress!"
    elif progress_pct >= 25: return "😊", "Good Start!"
    else: return "😐", "Let's Begin!"

# ---------------------------------------------------------------------
# Bottle drawing (PIL) — compatible shapes (no rounded_rectangle needed)
# ---------------------------------------------------------------------
def draw_bottle(progress_pct: float, width=220, height=360):
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    margin, neck_h = 16, 32
    top, bottom = margin, height - margin
    left, right = margin, width - margin
    # Neck + body (rects)
    neck_left, neck_right = width//2 - 28, width//2 + 28
    d.rectangle([(neck_left, top), (neck_right, top+neck_h)], outline="#2E66F0", width=3, fill=(255,255,255,255))
    body_top = top + neck_h
    d.rectangle([(left, body_top), (right, bottom)], outline="#2E66F0", width=3, fill=(255,255,255,255))
    # Fill
    p = max(0, min(100, int(progress_pct)))
    fill_h = int((p / 100.0) * (bottom - body_top))
    fill_top = bottom - fill_h
    # gradient-ish fill (two stripes)
    d.rectangle([(left+4, fill_top), (right-4, bottom-4)], fill=(64,150,255,210))
    wave_y = fill_top + 12
    d.line([(left+12, wave_y), (right-12, wave_y)], fill="#06B6D4", width=3)
    # Droplet icon (simple circle + triangle)
    cx, cy = width//2, body_top + (bottom-body_top)//2
    d.ellipse([(cx-16, cy-16), (cx+16, cy+16)], fill=(70,160,255,255), outline=None)
    d.polygon([(cx, cy-26), (cx-10, cy), (cx+10, cy)], fill=(70,160,255,255))
    return img

# ---------------------------------------------------------------------
# App state
# ---------------------------------------------------------------------
if "screen" not in st.session_state:      st.session_state.screen = "welcome"    # welcome | summary | tracker
if "profile" not in st.session_state:     st.session_state.profile = {"age": 13, "height": 165.0, "weight": 45.0, "condition": "Normal / Healthy"}
if "intake" not in st.session_state:      st.session_state.intake = 0
if "tip_index" not in st.session_state:   st.session_state.tip_index = 0
if "show_reset" not in st.session_state:  st.session_state.show_reset = False
if "day" not in st.session_state:         st.session_state.day = datetime.now().date()

# auto-new-day reset
if st.session_state.day != datetime.now().date():
    st.session_state.intake = 0
    st.session_state.day = datetime.now().date()

TIPS = [
    "Staying hydrated keeps your skin healthy and glowing!",
    "Sip water regularly—small sips beat big gulps.",
    "Carry a bottle so water is always within reach.",
    "Hydrate before and after exercise.",
    "Add lemon or cucumber for a tasty boost.",
]

# =====================================================================
# WELCOME SCREEN (like your onboarding screenshot)
# =====================================================================
def welcome_screen():
    st.markdown('<div class="card-soft">', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:42px;">💧</div>', unsafe_allow_html=True)
    st.markdown('<div class="h1" style="text-align:center;">Welcome to WaterBuddy+</div>', unsafe_allow_html=True)
    st.caption("Your personalized hydration companion")

    # Inputs in pastel cards
    age = st.number_input("Age (years)", min_value=4, max_value=120, value=int(st.session_state.profile["age"]))
    height = st.number_input("Height (cm)", min_value=50.0, max_value=240.0, value=float(st.session_state.profile["height"]), step=0.5)
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=250.0, value=float(st.session_state.profile["weight"]), step=0.5)
    condition = st.selectbox("Health Condition", [
        "Normal / Healthy", "Athlete / High Activity", "Hot Climate", "Pregnant", "Diabetic", "Kidney / Heart"
    ], index=["Normal / Healthy", "Athlete / High Activity", "Hot Climate", "Pregnant", "Diabetic", "Kidney / Heart"].index(st.session_state.profile["condition"]))
    adj = condition_adjustment(condition)
    st.caption(f"Adjustment: {adj:+d} ml")

    st.session_state.profile.update({"age": age, "height": height, "weight": weight, "condition": condition})

    # CTA
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("Calculate My Goal →", use_container_width=True, type="primary"):
            st.session_state.screen = "summary"
    st.markdown("</div>", unsafe_allow_html=True)  # card-soft

    st.markdown('<div style="text-align:center;margin-top:10px;color:#2563EB;">'
                '💡 No login required • All data stays private • Free forever</div>', unsafe_allow_html=True)

# =====================================================================
# SUMMARY SCREEN (like your profile & goal breakdown screenshot)
# =====================================================================
def summary_screen():
    p = st.session_state.profile
    calc = personalized_goal(p["age"], p["height"], p["weight"], p["condition"])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:42px;">💧</div>', unsafe_allow_html=True)
    st.markdown('<div class="h1" style="text-align:center;">Welcome to WaterBuddy+</div>', unsafe_allow_html=True)
    st.caption("Your personalized hydration companion")

    st.markdown('<div class="card" style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<div class="h2">Your Personalized Profile</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Age", f"{p['age']} years")
        st.metric("Height", f"{int(p['height'])} cm")
    with c2:
        st.metric("BMI", f"{calc['bmi']}", help=f"{calc['bmi_cat']}")
        st.metric("Weight", f"{int(p['weight'])} kg")
    st.caption(f"Condition: {p['condition']}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:10px;background:#F0FFF4;border-color:#DCFCE7;">', unsafe_allow_html=True)
    st.markdown('<div class="h2">Goal Calculation</div>', unsafe_allow_html=True)
    st.write(f"Base Goal (Age): **{calc['base']} ml**")
    st.write(f"BMI Adjustment ({calc['bmi_cat']}): **{calc['bmi_adj']:+d} ml**")
    st.write(f"Health Condition: **{calc['cond_adj']:+d} ml**")
    st.markdown('<div style="text-align:center;margin-top:10px;">', unsafe_allow_html=True)
    st.markdown(f'<div class="huge">{calc["goal"]} ml</div>', unsafe_allow_html=True)
    st.caption("Your Daily Goal")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    b1, b2 = st.columns([1,1])
    if b1.button("← Back", use_container_width=True):
        st.session_state.screen = "welcome"
    if b2.button("Start Tracking! →", use_container_width=True, type="primary"):
        st.session_state.screen = "tracker"
        st.session_state.intake = 0  # start fresh

    st.markdown("</div>", unsafe_allow_html=True)  # outer card

# =====================================================================
# TRACKER SCREEN (matches your tracking screenshots)
# =====================================================================
def tracker_screen():
    p = st.session_state.profile
    calc = personalized_goal(p["age"], p["height"], p["weight"], p["condition"])
    goal = calc["goal"]
    progress_pct = int(min(100, (st.session_state.intake / goal) * 100)) if goal else 0
    remaining = max(0, goal - st.session_state.intake)
    emoji, title_msg = mascot(progress_pct)

    # KPI row
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown('<div class="kpi">Today\'s Goal<br><span class="kpi-blue kpi-val">'
                    f'{goal} ml</span></div>', unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="kpi">Progress<br><span class="kpi-green kpi-val">'
                    f'{progress_pct}%</span></div>', unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="kpi">Remaining<br><span class="kpi-red kpi-val">'
                    f'{remaining} ml</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-sep"></div>', unsafe_allow_html=True)

    # Mascot + banner
    st.markdown(f'<div class="mascot">{emoji}</div>', unsafe_allow_html=True)
    banner = "💧 Time to hydrate!" if progress_pct == 0 else "🌊 Good start! Keep drinking!"
    st.markdown(f'<div class="banner"><span class="pill">{banner}</span></div>', unsafe_allow_html=True)

    # Bottle card + progress
    st.markdown('<div class="gradient-card">', unsafe_allow_html=True)
    st.markdown('<div class="bottle-frame">', unsafe_allow_html=True)
    st.image(draw_bottle(progress_pct), use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center;margin-top:8px;">'
                f'<b>{st.session_state.intake} ml / {goal} ml</b></div>', unsafe_allow_html=True)
    st.progress(min(1.0, st.session_state.intake / goal))
    st.caption(f"{progress_pct}% Complete")
    st.markdown('</div>', unsafe_allow_html=True)

    # Motivational line
    msg_line = "💧 Time to hydrate!" if progress_pct == 0 else "🌊 Good start! Keep drinking!"
    st.markdown(f'<div class="card" style="border-color:#CFE8FF;color:#2563EB;">{msg_line}</div>', unsafe_allow_html=True)

    # Add water buttons
    colA, colB = st.columns(2)
    if colA.button("+250 ml\n1 cup", use_container_width=True):
        st.session_state.intake = min(goal, st.session_state.intake + 250)
    if colB.button("+500 ml\n2 cups", use_container_width=True):
        st.session_state.intake = min(goal, st.session_state.intake + 500)

    # Custom amount
    c1, c2 = st.columns([3,1])
    with c1:
        custom = st.number_input("Custom amount (ml)", min_value=0, max_value=5000, value=0, step=50)
    if c2.button("Add", use_container_width=True):
        if custom > 0:
            st.session_state.intake = min(goal, st.session_state.intake + int(custom))

    # Reset + Tip buttons
    r1, r2 = st.columns(2)
    if r1.button("🧊 Reset", use_container_width=True):
        st.session_state.show_reset = True
    if r2.button("💡 Tip", use_container_width=True):
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(TIPS)

    # Tip card
    st.markdown(f'<div class="card" style="border-color:#E4ECF7;">'
                f'💡 {TIPS[st.session_state.tip_index]}</div>', unsafe_allow_html=True)

    # Celebration at 100%
    if progress_pct >= 100:
        st.balloons()

    # Reset Confirmation (custom dialog)
    if st.session_state.show_reset:
        st.markdown('<div class="card reset-dialog">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;font-size:36px;">⚠️</div>', unsafe_allow_html=True)
        st.markdown('<div class="reset-head">Start New Day?</div>', unsafe_allow_html=True)
        st.caption("This will clear your current progress and reset your daily water intake to 0 ml.")
        st.markdown('<div class="card" style="border-color:#CFE8FF;">', unsafe_allow_html=True)
        st.write(f"Current progress: **{st.session_state.intake} ml / {goal} ml ({progress_pct}%)**")
        st.progress(min(1.0, st.session_state.intake / goal))
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="warning">⚠️ This action cannot be undone</div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns([1,1])
        with cc1:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_reset = False
        with cc2:
            if st.button("Reset", use_container_width=True, type="primary"):
                st.session_state.intake = 0
                st.session_state.show_reset = False

# ---------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------
if st.session_state.screen == "welcome":
    welcome_screen()
elif st.session_state.screen == "summary":
    summary_screen()
else:
    tracker_screen()
