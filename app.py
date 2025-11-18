import streamlit as st

# --- Helper functions ---

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    if height_m == 0:
        return 0
    return round(weight / (height_m ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#B07124"
    elif 18.5 <= bmi < 25:
        return "Normal weight", "#228B22"
    elif 25 <= bmi < 30:
        return "Overweight", "#FF8C00"
    else:
        return "Obese", "#B22222"

def base_goal_by_age(age):
    if age <= 8:
        return 1200
    elif 9 <= age <= 13:
        return 1700
    elif 14 <= age <= 18:
        return 2200
    elif 19 <= age <= 50:
        return 2500
    else:
        return 2000

def health_condition_adjustment(condition):
    adjustments = {
        "Normal / Healthy": 0,
        "Athlete / High Activity": 300,
        "Pregnant": 200,
        "Breastfeeding": 500,
    }
    return adjustments.get(condition, 0)

def bmi_adjustment(category):
    adjustments = {
        "Underweight": -200,
        "Normal weight": 0,
        "Overweight": 100,
        "Obese": 200,
    }
    return adjustments.get(category, 0)

def emoji_for_progress(percentage):
    if percentage == 0:
        return "😐", "💧 Let's Begin!"
    elif percentage < 20:
        return "🙂", "🌊 Good Start!"
    elif percentage < 40:
        return "😊", "👍 Keep Going!"
    elif percentage < 60:
        return "😀", "💦 Halfway There!"
    elif percentage < 80:
        return "😄", "👏 Almost Done!"
    elif percentage < 100:
        return "🏅", "🎉 Excellent!"
    else:
        return "🏆", "🥳 Goal Achieved!"

# --- Initialize session state ---

if "step" not in st.session_state:
    st.session_state.step = "input"

for var in ["age", "height", "weight", "condition", "water_intake", "goal", "show_tip"]:
    if var not in st.session_state:
        if var == "condition":
            st.session_state[var] = "Normal / Healthy"
        elif var in ["water_intake", "goal"]:
            st.session_state[var] = 0
        elif var == "show_tip":
            st.session_state[var] = False
        else:
            st.session_state[var] = None

# --- UI Header ---
st.markdown("<h1 style='text-align:center; color:#1f3e82;'>💧</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center; color:#1f3e82;'>Welcome to WaterBuddy+</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Your personalized hydration companion</p>", unsafe_allow_html=True)

def show_input_page():
    st.markdown("""
        <style>
        .age-box {background:#e8f1fa; padding:15px; border-radius:12px; margin-bottom:20px;}
        .height-box {background:#faf2ff; padding:15px; border-radius:12px; margin-bottom:20px;}
        .weight-box {background:#ecfbee; padding:15px; border-radius:12px; margin-bottom:20px;}
        .condition-box {background:#fff7e8; padding:15px; border-radius:12px; margin-bottom:12px;}
        .adjustment {font-size:14px; color:#c1440e;}
        .footer {background:#d7e2fd; border-radius:8px; color:#193688; padding:10px; font-size:14px; margin-top:30px; text-align:center;}
        </style>
    """, unsafe_allow_html=True)

    with st.form("input_form"):
        st.markdown('<div class="age-box"><label style="color:#193688;font-weight:bold;">Age (years)</label></div>', unsafe_allow_html=True)
        age = st.number_input("", min_value=1, max_value=120, value=st.session_state.age or 25, step=1, format="%d", help="Enter your age")

        st.markdown('<div class="height-box"><label style="color:#5a2a85;font-weight:bold;">Height (cm)</label></div>', unsafe_allow_html=True)
        height = st.number_input("", min_value=1, max_value=300, value=st.session_state.height or 170, step=1, format="%d", help="Enter your height")

        st.markdown('<div class="weight-box"><label style="color:#1f6521;font-weight:bold;">Weight (kg)</label></div>', unsafe_allow_html=True)
        weight = st.number_input("", min_value=1, max_value=500, value=st.session_state.weight or 65, step=1, format="%d", help="Enter your weight")

        st.markdown('<div class="condition-box"><label style="color:#a85d00;font-weight:bold;">Health Condition</label></div>', unsafe_allow_html=True)
        condition = st.selectbox("", options=["Normal / Healthy", "Athlete / High Activity", "Pregnant", "Breastfeeding"],
                                index=["Normal / Healthy", "Athlete / High Activity", "Pregnant", "Breastfeeding"].index(st.session_state.condition),
                                help="Select your health condition")

        bmi = calculate_bmi(weight, height)
        category, _ = bmi_category(bmi)
        base = base_goal_by_age(age)
        bmi_adj = bmi_adjustment(category)
        cond_adj = health_condition_adjustment(condition)
        adjustment_ml = bmi_adj + cond_adj
        adj_text = f"{'+' if adjustment_ml >= 0 else ''}{adjustment_ml} ml"
        adj_color = "#c1440e" if adjustment_ml < 0 else "#d16f00" if adjustment_ml > 0 else "#333"

        st.markdown(f'<p class="adjustment" style="color:{adj_color};">Adjustment: {adj_text}</p>', unsafe_allow_html=True)

        submitted = st.form_submit_button("Calculate My Goal →")

        if submitted:
            st.session_state.age = age
            st.session_state.height = height
            st.session_state.weight = weight
            st.session_state.condition = condition
            st.session_state.bmi = bmi
            st.session_state.bmi_cat = category
            st.session_state.water_intake = 0
            st.session_state.goal = base + adjustment_ml
            st.session_state.step = "summary"
            st.session_state.show_tip = False

    st.markdown('<div class="footer">💡 No login required &bull; All data stays private &bull; Free forever</div>', unsafe_allow_html=True)

def show_summary():
    st.markdown("""
    <style>
    .profile-box {background:#e8f1fa; border-radius:12px; padding:15px; margin-bottom:20px; border:1.5px solid #a3c0ff;}
    .profile-title {font-weight:bold; text-align:center; margin-bottom:12px; font-size:18px;}
    .profile-data {display:flex; gap:15px; justify-content:center; flex-wrap: wrap;}
    .profile-item {background:#fff; border-radius:12px; padding:15px 20px; min-width:90px; text-align:center; box-shadow:0 0 6px #d0d9f2; font-weight:600; font-size:14px;}
    .profile-key {font-size:14px; color:#1f3e82; margin-bottom:6px;}
    .profile-value {font-size:20px; font-weight:700; color:#1f3e82;}
    .bmi-value {font-size:26px; font-weight:700; color:#800080; margin-bottom:0;}
    .bmi-category {font-size:14px; font-weight:600; color:#a96216;}
    .condition {font-weight:600; margin-top:15px; color:#a85d00; font-size:16px; text-align:center;}
    .goal-box {background:#ecfbee; border-radius:12px; padding:20px 15px; box-shadow:0 1px 3px #a4d09c; margin-bottom:20px;}
    .goal-row {display:flex; justify-content:space-between; padding:8px 12px; background:#fff; margin:6px 0; border-radius:8px; align-items:center; font-weight:600; font-size:14px;}
    .goal-label {margin:0; color:#193688;}
    .goal-value {font-weight:700; font-size:16px;}
    .goal-base {color:#193688;}
    .goal-bmi-adjustment {color:#800080;}
    .goal-condition {color:#d16f00;}
    .final-goal {background:#0e8a1b; color:#fff; padding:15px 0; text-align:center; border-radius:8px; font-weight:900; font-size:30px; margin-top:15px;}
    .btn-back, .btn-start {font-weight:700; padding:12px 0; border-radius:8px; cursor:pointer; border:none; font-size:16px; width:48%;}
    .btn-back {background:#babfc5; color:#555c69;}
    .btn-start {background:#1850f5; color:#fff;}
    .btn-block {display:flex; justify-content:space-between; gap:12px;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-box">', unsafe_allow_html=True)
    st.markdown('<p class="profile-title">Your Personalized Profile</p>', unsafe_allow_html=True)
    st.markdown('<div class="profile-data">', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-item"><div class="profile-key">Age</div><div class="profile-value">{st.session_state.age} years</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-item"><div class="profile-key">BMI</div><div class="bmi-value">{st.session_state.bmi}</div><div class="bmi-category">{st.session_state.bmi_cat}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-item"><div class="profile-key">Height</div><div class="profile-value" style="color:#1f6521;">{st.session_state.height} cm</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-item"><div class="profile-key">Weight</div><div class="profile-value" style="color:#1f6521;">{st.session_state.weight} kg</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="condition">🏃 {st.session_state.condition}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    base = base_goal_by_age(st.session_state.age)
    bmi_adj = bmi_adjustment(st.session_state.bmi_cat)
    cond_adj = health_condition_adjustment(st.session_state.condition)
    total = base + bmi_adj + cond_adj

    st.markdown('<div class="goal-box">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight:bold; font-size:17px; padding-bottom: 10px;">Goal Calculation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="goal-row"><p class="goal-label">Base Goal (Age)</p><p class="goal-value goal-base">{base} ml</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="goal-row"><p class="goal-label">BMI Adjustment<br><small style="color:#a96216;">({st.session_state.bmi_cat})</small></p><p class="goal-value goal-bmi-adjustment">{bmi_adj} ml</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="goal-row"><p class="goal-label">Health Condition</p><p class="goal-value goal-condition">{cond_adj:+d} ml</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="final-goal">Your Daily Goal<br><span style="font-size:36px;">{total} ml</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", key="back_from_summary"):
            st.session_state.step = "input"
    with col2:
        if st.button("Start Tracking! →", key="start_tracking"):
            st.session_state.goal = total
            st.session_state.water_intake = 0
            st.session_state.step = "tracking"
            st.session_state.show_tip = False

def show_tracking():
    st.markdown("""
    <style>
    .stats {
        display: flex;
        justify-content: space-around;
        font-weight: 600;
        padding: 10px 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 15px;
    }
    .stat-label {font-size: 14px; color: #193688;}
    .stat-value {font-weight: 700; font-size: 16px;}
    .stat-progress {color: #208028;}
    .stat-remaining {color: #d45c13;}
    .drop-container {
        background-color: #d9f0ff;
        border-radius: 12px;
        padding: 25px 10px 16px 10px;
        margin: 0 auto 20px auto;
        width: 160px;
        text-align: center;
        box-shadow: 0 0 30px #b5d5ff80;
        position: relative;
        min-height: 200px;
    }
    .drop-emoji {
        font-size: 48px;
        margin-bottom: 8px;
    }
    .drop-bubble {
        font-weight: bold;
        font-size: 14px;
        color: #193688;
        margin-bottom: 10px;
    }
    .water-container {
        border: 3px solid #439eff;
        border-radius: 15px;
        width: 90px;
        height: 170px;
        margin: 0 auto;
        position: relative;
        box-shadow: inset 0 8px 10px -6px #439eff99;
        background: #e3f7ff;
        overflow: hidden;
    }
    .water-fill {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #2e95f6;
        border-radius: 0 0 15px 15px;
        transition: height 0.4s ease-in-out;
        box-shadow: inset 0 5px 6px #9fdbff;
    }
    .water-drop-icon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 48px;
        user-select: none;
        pointer-events: none;
        color: #58a6ff;
    }
    .progress-text {
        font-weight: 700;
        margin-top: 10px;
        color: #193688;
    }
    .percent-text {
        font-weight: 600;
        font-size: 12px;
        color: #5d5d5d;
        margin-bottom: 6px;
    }
    .prompt-box {
        background-color: #d9f0ff;
        border-radius: 12px;
        padding: 15px 20px;
        font-weight: 600;
        font-size: 18px;
        color: #193688;
        margin-bottom: 15px;
        text-align: center;
        border: 2px solid #439eff;
    }
    .btn-ml {
        border-radius: 12px;
        background-color: #1850f5;
        color: white;
        font-weight: 700;
        font-size: 16px;
        padding: 15px;
        cursor: pointer;
        width: 45%;
        margin: 5px 2.5%;
        border: none;
    }
    .input-ml {
        border-radius: 10px;
        border: 2px solid #55c6ff;
        padding: 10px 12px;
        width: 180px;
        font-size: 14px;
    }
    .btn-reset {
        background-color: #babfc5;
        color: #555c69;
        border: none;
        padding: 12px 15px;
        margin-top: 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
    }
    .btn-tip {
        background-color: #faf2ff;
        border: 2px solid #ad84ff;
        color: #7318ff;
        padding: 12px 15px;
        font-weight: 700;
        border-radius: 8px;
        margin-top: 20px;
        cursor: pointer;
    }
    .tip-box {
        background-color: #faf2ff;
        border: 2px solid #ad84ff;
        color: #7318ff;
        border-radius: 12px;
        padding: 15px;
        margin-top: 10px;
        font-weight: 500;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    goal = st.session_state.goal
    intake = st.session_state.water_intake
    percent = int(min((intake / goal) * 100, 100)) if goal > 0 else 0
    remaining = max(goal - intake, 0)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<p class="stat-label">Today\'s Goal</p><p class="stat-value">{goal} ml</p>', unsafe_allow_html=True)
    col2.markdown(f'<p class="stat-label">Progress</p><p class="stat-value stat-progress">{percent}%</p>', unsafe_allow_html=True)
    col3.markdown(f'<p class="stat-label">Remaining</p><p class="stat-value stat-remaining">{remaining} ml</p>', unsafe_allow_html=True)

    emoji, label = emoji_for_progress(percent)
    with st.container():
        st.markdown('<div class="drop-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="drop-emoji" aria-label="progress emoji">{emoji}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="drop-bubble" aria-label="progress label">{label}</div>', unsafe_allow_html=True)

        fill_percent = percent
        fill_height = f"{fill_percent}%" if fill_percent > 0 else "0%"

        st.markdown(f'''
        <div class="water-container" aria-label="water container">
            <div class="water-fill" style="height:{fill_height};"></div>
            <div class="water-drop-icon">💧</div>
        </div>''', unsafe_allow_html=True)

        st.markdown(f'<div class="progress-text" aria-label="progress">{intake} ml / {goal} ml</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="percent-text">{percent}% Complete</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="prompt-box">💧 Time to hydrate!</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("+250 ml\n1 cup", key="add_250"):
        st.session_state.water_intake += 250
        st.session_state.show_tip = False
    if col2.button("+500 ml\n2 cups", key="add_500"):
        st.session_state.water_intake += 500
        st.session_state.show_tip = False

    col_custom, col_btn = st.columns([4, 1])
    with col_custom:
        amount_str = st.text_input("Custom amount (ml)", key="custom_amount_input")
    with col_btn:
        if st.button("Add", key="add_custom"):
            try:
                amt = int(amount_str)
                if amt > 0:
                    st.session_state.water_intake += amt
                    st.session_state.show_tip = False
                    st.session_state["custom_amount_input"] = ""
            except Exception:
                st.warning("Enter a valid positive integer")

    col_reset, col_tip = st.columns(2)
    if col_reset.button("🔄 Reset", key="reset_tracking"):
        st.session_state.step = "reset_confirm"
    if col_tip.button("💡 Tip", key="tip_click"):
        st.session_state.show_tip = True

    if st.session_state.show_tip:
        st.markdown('<div class="tip-box">💡 Staying hydrated keeps your skin healthy and glowing!</div>', unsafe_allow_html=True)

def show_reset_confirmation():
    st.markdown("""
        <style>
        .warning-emoji {font-size: 80px; text-align: center; margin-bottom: 10px;}
        .warning-text {text-align: center; color: #841c1c; font-weight: 700; font-size: 22px; margin-bottom: 15px;}
        .explanation {font-size: 16px; color: #454851; text-align: center; margin-bottom: 20px;}
        .progress-box {
            background-color: #d7e2fd;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
            font-weight: 600;
            text-align:center;
            color: #193688;
        }
        .danger-zone {
            background-color: #f9d7d3;
            border-radius: 12px;
            padding: 12px;
            color: #841c1c;
            font-weight: 700;
            margin-bottom: 25px;
            text-align:center;
        }
        .btn-cancel {
            background-color: #babfc5;
            color: #555c69;
            padding: 12px 25px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            border: none;
            margin-right: 20px;
            font-size: 16px;
        }
        .btn-reset {
            background-color: #b91f1f;
            color: white;
            padding: 12px 25px;
            border-radius: 10px;
            font-weight: 700;
            cursor: pointer;
            border: none;
            font-size: 16px;
        }
        .btn-container {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="warning-emoji">⚠️</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-text">Start New Day?</div>', unsafe_allow_html=True)
    st.markdown('<div class="explanation">This will clear your current progress and reset your daily water intake to 0 ml.</div>', unsafe_allow_html=True)

    progress_percent = int(min((st.session_state.water_intake / st.session_state.goal) * 100, 100)) if st.session_state.goal else 0
    water = st.session_state.water_intake
    goal = st.session_state.goal

    st.markdown(
        f'<div class="progress-box"><strong>Current progress:</strong><br>{water} ml / {goal} ml ({progress_percent}%)<br><progress value="{water}" max="{goal}" style="width: 100%; height: 20px;"></progress></div>',
        unsafe_allow_html=True)

    st.markdown('<div class="danger-zone">⚠️ This action cannot be undone</div>', unsafe_allow_html=True)

    col_cancel, col_reset = st.columns([1, 1])
    with col_cancel:
        if st.button("Cancel", key="cancel_reset"):
            st.session_state.step = "tracking"
    with col_reset:
        if st.button("Reset", key="confirm_reset"):
            st.session_state.water_intake = 0
            st.session_state.step = "tracking"
            st.session_state.show_tip = False

# --- Main app ---

if st.session_state.step == "input":
    show_input_page()
elif st.session_state.step == "summary":
    show_summary()
elif st.session_state.step == "tracking":
    show_tracking()
elif st.session_state.step == "reset_confirm":
    show_reset_confirmation()
