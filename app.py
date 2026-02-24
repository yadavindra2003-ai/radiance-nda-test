import streamlit as st
import time

# Radiance Classes Branding
st.set_page_config(page_title="NDA Mock Test - Radiance", page_icon="⏱️")
st.title("⚔️ Radiance Defence Academy")
st.subheader("Timed NDA Mock Test | Faculty: Indra Yadav")

# 1. Timer Logic & Student Details
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

with st.sidebar:
    st.header("📋 Student Portal")
    name = st.text_input("Student Name")
    phone = st.text_input("Mobile Number")
    
    # Set Time Limit (e.g., 20 minutes for this mini-test)
    TIME_LIMIT_MINS = 20 
    
    if name and phone and st.session_state.start_time is None:
        if st.button("🚀 Start Test"):
            st.session_state.start_time = time.time()
            st.rerun()

# 2. Timer Display
if st.session_state.start_time:
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = max(0, (TIME_LIMIT_MINS * 60) - elapsed_time)
    
    mins, secs = divmod(int(remaining_time), 60)
    timer_text = f"⏳ Time Remaining: {mins:02d}:{secs:02d}"
    
    if remaining_time > 0:
        st.sidebar.subheader(timer_text)
        if remaining_time < 300: # Last 5 minutes warning
            st.sidebar.warning("⚠️ Hurry Up! Less than 5 mins left.")
    else:
        st.sidebar.error("⏰ Time's Up!")
        st.session_state.time_over = True

# 3. Question Bank
questions = [
    {"q": "What is the value of log₂ (log₃ 81)?", "options": ["2", "3", "4", "9"], "a": "2"},
    {"q": "Derivative of tan x is:", "options": ["sec²x", "cosec²x", "sec x", "cos²x"], "a": "sec²x"},
    {"q": "If sin θ + cos θ = √2, then sin θ . cos θ is:", "options": ["1/2", "1", "√2", "2"], "a": "1/2"},
    {"q": "The value of i¹⁰⁰ is:", "options": ["1", "-1", "i", "-i"], "a": "1"},
    {"q": "Equation of a line passing through origin is:", "options": ["y = mx", "y = mx + c", "x = a", "y = b"], "a": "y = mx"}
]

# 4. Test Interface
if not name or not phone:
    st.info("👋 Enter details and click 'Start Test' to begin.")
elif st.session_state.start_time:
    with st.form("nda_timed_test"):
        user_ans = []
        for i, item in enumerate(questions):
            st.markdown(f"**Q{i+1}. {item['q']}**")
            choice = st.radio("Select answer:", item["options"], key=f"q_{i}", index=None)
            user_ans.append(choice)
        
        submitted = st.form_submit_button("Submit Test")

    if submitted or remaining_time <= 0:
        correct = sum(1 for i, q in enumerate(questions) if user_ans[i] == q["a"])
        score = (correct * 2.5) - ((len(user_ans)-correct) * 0.83)
        
        st.success(f"### Result for {name}")
        st.metric("Final Marks", f"{score:.2f}")
        st.balloons()
      
