import streamlit as st
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Water Buddy",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS based on MedTimer design system
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Root variables matching MedTimer color scheme */
    :root {
        --primary-blue: #488FDB;
        --blue-50: #EBF3FB;
        --blue-100: #D6E7F7;
        --blue-500: #488FDB;
        --blue-600: #3A7BC4;
        --blue-700: #2E63A0;
        --green-50: #F0F9F4;
        --green-500: #52C189;
        --green-600: #42A575;
        --orange-50: #FEF5E7;
        --orange-400: #F5A447;
        --orange-500: #F39C12;
        --yellow-400: #F7DC6F;
        --gray-50: #FAFBFC;
        --gray-200: #E5E7EB;
        --gray-300: #D1D5DB;
        --gray-500: #6B7280;
        --gray-600: #4B5563;
        --gray-700: #374151;
        --gray-900: #111827;
    }
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        padding: 1rem;
        max-width: 28rem;
        margin: 0 auto;
    }
    
    /* Custom title */
    .app-title {
        font-size: 2.25rem;
        font-weight: 600;
        color: var(--gray-900);
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--blue-500), var(--blue-700));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .app-subtitle {
        text-align: center;
        color: var(--gray-500);
        font-size: 0.875rem;
        margin-bottom: 2rem;
    }
    
    /* Progress container */
    .progress-container {
        background: linear-gradient(135deg, var(--yellow-400), var(--orange-400));
        border-radius: 1.5rem;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .progress-text {
        color: white;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .progress-amount {
        color: white;
        text-align: center;
        font-size: 3rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .progress-goal {
        color: white;
        text-align: center;
        font-size: 0.875rem;
        opacity: 0.9;
    }
    
    /* Action buttons */
    .stButton button {
        width: 100%;
        background-color: var(--blue-500);
        color: white;
        border: none;
        border-radius: 0.75rem;
        padding: 1rem;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.2s;
        margin-bottom: 0.75rem;
    }
    
    .stButton button:hover {
        background-color: var(--blue-600);
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Stats cards */
    .stats-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 2px solid var(--blue-200);
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .stats-title {
        color: var(--gray-700);
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .stats-value {
        color: var(--blue-600);
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* History item */
    .history-item {
        background: var(--blue-50);
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .history-time {
        color: var(--gray-600);
        font-size: 0.875rem;
    }
    
    .history-amount {
        color: var(--blue-700);
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Input fields */
    .stNumberInput input {
        border-radius: 0.75rem;
        border: 2px solid var(--gray-200);
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stNumberInput input:focus {
        border-color: var(--blue-400);
        outline: none;
    }
    
    /* Quick add buttons */
    .quick-add-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-bottom: 2rem;
    }
    
    .quick-add-btn {
        background: var(--blue-100);
        color: var(--blue-700);
        border: 2px solid var(--blue-200);
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-add-btn:hover {
        background: var(--blue-500);
        color: white;
        border-color: var(--blue-500);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = []
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 2000
if 'today_total' not in st.session_state:
    st.session_state.today_total = 0

def add_water(amount):
    """Add water intake to today's log"""
    now = datetime.now()
    st.session_state.water_intake.append({
        'amount': amount,
        'time': now.strftime('%I:%M %p'),
        'date': now.strftime('%Y-%m-%d')
    })
    calculate_today_total()

def calculate_today_total():
    """Calculate total water intake for today"""
    today = datetime.now().strftime('%Y-%m-%d')
    st.session_state.today_total = sum(
        entry['amount'] for entry in st.session_state.water_intake 
        if entry['date'] == today
    )

def get_today_entries():
    """Get today's water intake entries"""
    today = datetime.now().strftime('%Y-%m-%d')
    return [entry for entry in st.session_state.water_intake if entry['date'] == today]

# Calculate today's total on load
calculate_today_total()

# App header
st.markdown('<h1 class="app-title">💧 Water Buddy</h1>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Stay hydrated, stay healthy!</p>', unsafe_allow_html=True)

# Progress display
today_total = st.session_state.today_total
daily_goal = st.session_state.daily_goal
progress_percent = min(100, (today_total / daily_goal) * 100)

st.markdown(f"""
<div class="progress-container">
    <div class="progress-text">Today's Hydration</div>
    <div class="progress-amount">{today_total} ml</div>
    <div class="progress-goal">Goal: {daily_goal} ml ({progress_percent:.0f}%)</div>
</div>
""", unsafe_allow_html=True)

# Quick add buttons
st.markdown("### Quick Add")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💧 250ml"):
        add_water(250)
        st.rerun()

with col2:
    if st.button("🥤 500ml"):
        add_water(500)
        st.rerun()

with col3:
    if st.button("🍶 1000ml"):
        add_water(1000)
        st.rerun()

# Custom amount
st.markdown("### Add Custom Amount")
custom_amount = st.number_input(
    "Enter amount (ml)",
    min_value=0,
    max_value=5000,
    value=250,
    step=50,
    key="custom_amount"
)

if st.button("➕ Add Custom Amount"):
    if custom_amount > 0:
        add_water(custom_amount)
        st.success(f"Added {custom_amount}ml to your daily intake!")
        st.rerun()

# Statistics
st.markdown("### Today's Stats")
col1, col2 = st.columns(2)

today_entries = get_today_entries()
num_drinks = len(today_entries)
avg_drink = today_total / num_drinks if num_drinks > 0 else 0

with col1:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-title">Drinks Today</div>
        <div class="stats-value">{num_drinks}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-title">Avg per Drink</div>
        <div class="stats-value">{avg_drink:.0f} ml</div>
    </div>
    """, unsafe_allow_html=True)

# History
st.markdown("### Today's History")
if today_entries:
    for entry in reversed(today_entries[-5:]):  # Show last 5 entries
        st.markdown(f"""
        <div class="history-item">
            <div class="history-time">🕐 {entry['time']}</div>
            <div class="history-amount">{entry['amount']} ml</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No water intake recorded yet today. Start tracking!")

# Settings
st.markdown("---")
st.markdown("### Settings")
new_goal = st.number_input(
    "Daily Goal (ml)",
    min_value=500,
    max_value=5000,
    value=st.session_state.daily_goal,
    step=100,
    key="goal_input"
)

if st.button("💾 Save Goal"):
    st.session_state.daily_goal = new_goal
    st.success(f"Daily goal updated to {new_goal}ml!")
    st.rerun()

# Reset button
if st.button("🔄 Reset Today's Data"):
    today = datetime.now().strftime('%Y-%m-%d')
    st.session_state.water_intake = [
        entry for entry in st.session_state.water_intake 
        if entry['date'] != today
    ]
    st.session_state.today_total = 0
    st.success("Today's data has been reset!")
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6B7280; font-size: 0.875rem;'>💙 Stay healthy, drink water regularly!</p>",
    unsafe_allow_html=True
)
