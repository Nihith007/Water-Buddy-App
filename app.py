import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="WaterBuddy+",
    page_icon="💧",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .goal-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .progress-container {
        background-color: #f0f0f0;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
    }
    .progress-bar {
        background-color: #1f77b4;
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    .metric-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "input"
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 0
if 'show_reset_confirmation' not in st.session_state:
    st.session_state.show_reset_confirmation = False

def calculate_bmi(height, weight):
    """Calculate BMI given height in cm and weight in kg"""
    if height > 0:
        height_m = height / 100
        return weight / (height_m ** 2)
    return 0

def get_bmi_category(bmi):
    """Get BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight", -200
    elif 18.5 <= bmi < 25:
        return "Normal", 0
    elif 25 <= bmi < 30:
        return "Overweight", -100
    else:
        return "Obese", -200

def calculate_water_goal(age, height, weight, health_condition):
    """Calculate daily water goal based on user inputs"""
    # Base goal by age
    if age < 18:
        base_goal = 1700
    elif 18 <= age < 55:
        base_goal = 2000
    else:
        base_goal = 1800
    
    # BMI adjustment
    bmi = calculate_bmi(height, weight)
    bmi_category, bmi_adjustment = get_bmi_category(bmi)
    
    # Health condition adjustment
    health_adjustment = 0
    if health_condition == "Athlete / High Activity":
        health_adjustment = 300
    elif health_condition == "Pregnant / Breastfeeding":
        health_adjustment = 500
    elif health_condition == "Kidney Issues":
        health_adjustment = -300
    
    # Calculate final goal
    final_goal = base_goal + bmi_adjustment + health_adjustment
    
    return {
        "base_goal": base_goal,
        "bmi": bmi,
        "bmi_category": bmi_category,
        "bmi_adjustment": bmi_adjustment,
        "health_adjustment": health_adjustment,
        "final_goal": final_goal
    }

def input_page():
    """Display the input form page"""
    st.markdown('<div class="main-header">Welcome to WaterBuddy+</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your personalized hydration companion</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">Age (years)</div>', unsafe_allow_html=True)
    age = st.number_input("Enter your age", min_value=1, max_value=120, value=25, key="age_input")
    
    st.markdown('<div class="section-header">Height (cm)</div>', unsafe_allow_html=True)
    height = st.number_input("Enter your height", min_value=50, max_value=250, value=170, key="height_input")
    
    st.markdown('<div class="section-header">Weight (kg)</div>', unsafe_allow_html=True)
    weight = st.number_input("Enter your weight", min_value=10, max_value=300, value=70, key="weight_input")
    
    st.markdown('<div class="section-header">Health Condition</div>', unsafe_allow_html=True)
    health_condition = st.radio(
        "Select your health condition:",
        ["Normal / Healthy", "Athlete / High Activity", "Pregnant / Breastfeeding", "Kidney Issues"],
        index=0,
        key="health_radio"
    )
    
    st.markdown("---")
    
    if st.button("Calculate My Goal →", type="primary", use_container_width=True):
        # Store user data
        st.session_state.user_data = {
            "age": age,
            "height": height,
            "weight": weight,
            "health_condition": health_condition
        }
        
        # Calculate water goal
        calculation = calculate_water_goal(age, height, weight, health_condition)
        st.session_state.daily_goal = calculation["final_goal"]
        st.session_state.calculation_details = calculation
        
        # Move to results page
        st.session_state.page = "results"
        st.rerun()
    
    st.markdown("---")
    st.caption("No login required • All data stays private • Free forever")

def results_page():
    """Display the calculation results page"""
    st.markdown('<div class="main-header">Welcome to WaterBuddy+</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your personalized hydration companion</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">Your Personalized Profile</div>', unsafe_allow_html=True)
    
    # User profile in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div class="metric-box">**Age**<br>{st.session_state.user_data["age"]} years</div>', unsafe_allow_html=True)
        bmi = st.session_state.calculation_details["bmi"]
        st.markdown(f'<div class="metric-box">**BMI**<br>{bmi:.1f}<br>{st.session_state.calculation_details["bmi_category"]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="metric-box">**Height**<br>{st.session_state.user_data["height"]} cm</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-box">**Weight**<br>{st.session_state.user_data["weight"]} kg</div>', unsafe_allow_html=True)
    
    st.markdown("**Condition**")
    st.write(f"- **{st.session_state.user_data['health_condition']}**")
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">Goal Calculation</div>', unsafe_allow_html=True)
    
    # Goal calculation details
    st.markdown(f'**Base Goal (Age)**: {st.session_state.calculation_details["base_goal"]} ml')
    st.markdown(f'**BMI Adjustment ({st.session_state.calculation_details["bmi_category"]})**: {st.session_state.calculation_details["bmi_adjustment"]} ml')
    st.markdown(f'**Health Condition**: {st.session_state.calculation_details["health_adjustment"]} ml')
    
    st.markdown("---")
    
    # Final goal
    st.markdown(f'<div class="goal-box"><h2 style="text-align: center; margin: 0;">Your Daily Goal</h2><h1 style="text-align: center; color: #1f77b4; margin: 0;">{st.session_state.daily_goal} ml</h1></div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()
    
    with col2:
        if st.button("Start Tracking! →", type="primary", use_container_width=True):
            st.session_state.page = "tracking"
            st.rerun()

def tracking_page():
    """Display the water tracking page"""
    # Calculate progress
    progress_percent = (st.session_state.water_intake / st.session_state.daily_goal * 100) if st.session_state.daily_goal > 0 else 0
    remaining_water = max(0, st.session_state.daily_goal - st.session_state.water_intake)
    
    # Header
    st.markdown(f'<div class="main-header">Today\'s Goal {st.session_state.daily_goal} ml</div>', unsafe_allow_html=True)
    
    # Progress metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Progress", f"{progress_percent:.0f}%")
    
    with col2:
        st.metric("Remaining", f"{remaining_water:.0f} ml")
    
    # Progress message
    if progress_percent == 0:
        st.write("Let's Begin!")
    elif progress_percent < 30:
        st.write("Good Start! Keep drinking!")
    elif progress_percent < 70:
        st.write("You're doing great! Keep it up!")
    elif progress_percent < 100:
        st.write("Almost there! You can do it!")
    else:
        st.write("🎉 Congratulations! You've reached your goal!")
    
    # Progress bar
    st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {min(progress_percent, 100)}%;"></div></div>', unsafe_allow_html=True)
    
    # Progress text
    st.write(f"{st.session_state.water_intake:.0f} ml / {st.session_state.daily_goal:.0f} ml")
    st.write(f"{progress_percent:.0f}% Complete")
    
    # Hydration reminder
    if progress_percent < 100:
        st.checkbox("Time to hydrate!", value=False, key="reminder")
    
    st.markdown("---")
    
    # Water intake buttons
    st.markdown("### Add Water Intake")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("+250 ml\n1 cup", use_container_width=True):
            st.session_state.water_intake += 250
    
    with col2:
        if st.button("+500 ml\n2 cups", use_container_width=True):
            st.session_state.water_intake += 500
    
    with col3:
        custom_amount = st.number_input("Custom amount (ml)", min_value=0, max_value=5000, value=250, key="custom_ml")
        if st.button("Add", use_container_width=True):
            st.session_state.water_intake += custom_amount
    
    # Reset and tip buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset", use_container_width=True):
            st.session_state.show_reset_confirmation = True
    
    with col2:
        if st.button("Tip", use_container_width=True):
            tips = [
                "Staying hydrated keeps your skin healthy and glowing!",
                "Drink water before meals to help with digestion!",
                "Carry a water bottle with you throughout the day!",
                "Set reminders to drink water regularly!",
                "Eating water-rich foods like fruits also helps hydration!"
            ]
            st.info(tips[st.session_state.get('tip_index', 0) % len(tips)])
            st.session_state.tip_index = st.session_state.get('tip_index', 0) + 1
    
    # Reset confirmation dialog
    if st.session_state.show_reset_confirmation:
        st.markdown("---")
        st.warning("Start New Day?")
        st.write("This will clear your current progress and reset your daily water intake to 0 ml.")
        st.write(f"Current progress: {st.session_state.water_intake:.0f} ml / {st.session_state.daily_goal:.0f} ml ({progress_percent:.0f}%)")
        st.write("This action cannot be undone")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_reset_confirmation = False
                st.rerun()
        
        with col2:
            if st.button("Reset", type="primary", use_container_width=True):
                st.session_state.water_intake = 0
                st.session_state.show_reset_confirmation = False
                st.rerun()

# Main app logic
if st.session_state.page == "input":
    input_page()
elif st.session_state.page == "results":
    results_page()
elif st.session_state.page == "tracking":
    tracking_page()
