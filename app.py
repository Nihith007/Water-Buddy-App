import streamlit as st

st.set_page_config(
    page_title="WaterBuddy+ Blueprint",
    page_icon="💧",
    layout="wide"
)

if "current_view" not in st.session_state:
    st.session_state.current_view = "blueprint"
if "age_group" not in st.session_state:
    st.session_state.age_group = ""
if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 2000
if "total_intake" not in st.session_state:
    st.session_state.total_intake = 0

st.markdown(
    """
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:15px;">
      <div style="width:45px;height:45px;background:linear-gradient(to bottom right,#3b82f6,#06b6d4);border-radius:50%;display:flex;align-items:center;justify-content:center;">
        💧
      </div>
      <div>
        <h2 style="color:#1e3a8a;margin:0;">WaterBuddy+ Blueprint</h2>
        <p style="color:#475569;font-size:13px;margin:0;">Personalized Hydration with Age + BMI + Health Conditions</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    if st.button("📋 Blueprint View", use_container_width=True):
        st.session_state.current_view = "blueprint"
with col2:
    if st.button("🎮 Live Demo", use_container_width=True):
        st.session_state.current_view = "demo"

st.markdown("---")

if st.session_state.current_view == "blueprint":
    tabs = st.tabs(["🔍 Research", "⚙️ Logic Flow", "🎨 Storyboard", "📋 Deliverables"])
  
    with tabs[0]:
        st.header("Stage 1: Research 🔍")
        st.write("""
        - Study hydration patterns across different age groups.
        - Identify challenges like forgetting to drink water.
        - Define app’s unique value (simple, motivating, and private).
        """)

    with tabs[1]:
        st.header("Stage 2: Logic Flow ⚙️")
        st.image("https://placehold.co/800x400?text=Flowchart+Diagram", caption="Input → Logic → Output")

    with tabs[2]:
        st.header("Stage 3: Storyboard 🎨")
        st.image("https://placehold.co/800x400?text=Storyboard+Screens", caption="Storyboard mockups for app screens")

    with tabs[3]:
        st.header("Stage 4: Deliverables 📋")

        deliverables = [
            ("Storyboard", "All screens with labeled notes and annotations"),
            ("Flowchart / Data Logic Diagram", "Input → Logic → Output flow clearly mapped"),
            ("Research Annotations", "Hydration importance, age groups, and value proposition"),
            ("Feature List", "5 compulsory features clearly implemented"),
            ("Avatar / Mascot Reactions", "Visual reactions at 50%, 75%, and 100% progress"),
        ]

        for title, desc in deliverables:
            st.success(f"✅ {title}: {desc}")

        st.info("""
        **🎯 Project Summary**

        WaterBuddy is a user-friendly hydration tracking app designed to solve real-world problems 
        like forgetting to drink water due to busy schedules. Unlike complex existing apps, 
        WaterBuddy offers a simple, private, and motivating experience with age-based personalization.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Target Users:** All ages (4–65+)")
        with col2:
            st.markdown("**Core Innovation:** Age-specific guidance + motivation")

else:
    st.header("🎮 WaterBuddy Demo")

    if not st.session_state.age_group:
        st.subheader("Welcome to WaterBuddy!")
        st.write("Select your age group to personalize your hydration goal:")

        st.session_state.age_group = st.selectbox(
            "Choose Age Group:",
            ["", "4–12", "13–18", "19–35", "36–50", "51+"],
            index=0
        )

        if st.session_state.age_group:
            st.session_state.daily_goal = st.number_input(
                "Set your daily water goal (ml):",
                min_value=500,
                max_value=5000,
                value=2000,
                step=100
            )
            st.success("✅ Age group and goal set! Click 'Live Demo' again to begin tracking.")
    else:
        st.subheader(f"Hydration Tracker for Age Group: {st.session_state.age_group}")
        st.write(f"**Daily Goal:** {st.session_state.daily_goal} ml")

        add = st.number_input("Add water intake (ml):", min_value=0, max_value=1000, step=100)
        if st.button("Add Intake"):
            st.session_state.total_intake += add

        st.progress(min(st.session_state.total_intake / st.session_state.daily_goal, 1.0))
        st.write(f"💧 **Total Intake:** {st.session_state.total_intake} ml")

        if st.button("Reset"):
            st.session_state.age_group = ""
            st.session_state.total_intake = 0
            st.experimental_rerun()
