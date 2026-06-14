# ============================================
# PLACORA - Main Streamlit Dashboard
# File: dashboard/streamlit_app.py
# Run: streamlit run dashboard/streamlit_app.py
# ============================================

import streamlit as st
import sys
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Project root path set karo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.resume_parser   import extract_text_from_uploaded_file, extract_sections, calculate_ats_score, extract_contact_info
from app.skill_extractor import extract_skills, get_all_skills_flat, analyze_skill_gap
from app.predictor       import predict_placement, train_placement_model, get_improvement_suggestions
from app.recommender     import recommend_jobs, get_career_path
from app.chatbot         import get_career_guidance, generate_interview_questions, generate_learning_roadmap, analyze_resume_with_ai

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="Placora - AI Placement Mentor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #1f77b4; text-align: center; }
    .subtitle   { font-size: 1.1rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .metric-card { background: #f0f8ff; padding: 1rem; border-radius: 10px; text-align: center; border: 1px solid #ddd; }
    .success-box { background: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; }
    .warning-box { background: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; }
    .danger-box  { background: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545; }
    .info-box    { background: #d1ecf1; padding: 1rem; border-radius: 8px; border-left: 4px solid #17a2b8; }
</style>
""", unsafe_allow_html=True)


# ============================================
# Session State Initialize
# ============================================
if 'student_data' not in st.session_state:
    st.session_state.student_data = {}
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'ml_model' not in st.session_state:
    with st.spinner("ML Model load ho raha hai..."):
        model, scaler, acc, _ = train_placement_model(save_model=False)
        st.session_state.ml_model  = model
        st.session_state.ml_scaler = scaler


# ============================================
# Sidebar - Student Info
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=80)
    st.title("Placora")
    st.caption("AI Placement Mentor")
    st.divider()

    st.subheader("Student Profile")
    name   = st.text_input("Full Name",   placeholder="e.g. Rahul Sharma")
    email  = st.text_input("Email",       placeholder="rahul@gmail.com")
    cgpa   = st.slider("CGPA", 4.0, 10.0, 7.5, 0.1)
    branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EE", "ME", "CE", "Other"])
    college = st.text_input("College Name", placeholder="ABC Engineering College")

    st.divider()
    target_role = st.selectbox("Target Job Role", [
        "Data Scientist", "Data Analyst", "Software Engineer",
        "Web Developer", "ML Engineer", "AI Engineer",
        "Backend Developer", "Frontend Developer", "DevOps Engineer", "Business Analyst"
    ])

    st.divider()
    internship    = st.radio("Internship Experience?", ["No", "Yes"])
    communication = st.slider("Communication Skills (1-5)", 1, 5, 3)
    backlogs      = st.number_input("Number of Backlogs", 0, 10, 0)

    st.session_state.student_data = {
        'name': name, 'email': email, 'cgpa': cgpa,
        'branch': branch, 'college': college,
        'target_role': target_role,
        'internship': 1 if internship == "Yes" else 0,
        'communication': communication,
        'backlogs': backlogs
    }


# ============================================
# Main Content
# ============================================
st.markdown('<div class="main-title">🎓 Placora - AI Placement Mentor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Resume analyze karo · Placement predict karo · Career guidance pao</div>', unsafe_allow_html=True)

tabs = st.tabs(["📄 Resume Analysis", "📊 Placement Prediction", "💼 Job Recommendations", "🤖 AI Mentor", "📝 Interview Prep"])


# ============================================
# TAB 1: Resume Analysis
# ============================================
with tabs[0]:
    st.header("Resume Analyzer")
    uploaded = st.file_uploader("Apna Resume Upload karo (PDF only)", type=['pdf'])

    if uploaded:
        with st.spinner("Resume analyze ho raha hai..."):
            resume_text = extract_text_from_uploaded_file(uploaded)
            sections    = extract_sections(resume_text)
            contact     = extract_contact_info(resume_text)
            ats_score, breakdown, strengths, weaknesses = calculate_ats_score(resume_text, sections)
            skills_dict = extract_skills(resume_text)
            flat_skills = get_all_skills_flat(skills_dict)

            # Save to session
            st.session_state.student_data['skills']    = flat_skills
            st.session_state.student_data['ats_score'] = ats_score
            st.session_state.student_data['resume_text'] = resume_text
            st.session_state.analysis_done = True

        # ATS Score Display
        col1, col2, col3 = st.columns(3)
        with col1:
            color = "green" if ats_score >= 70 else "orange" if ats_score >= 50 else "red"
            st.metric("ATS Score", f"{ats_score}/100")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=ats_score,
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': color},
                       'steps': [{'range': [0, 50], 'color': '#ffcccc'},
                                 {'range': [50, 70], 'color': '#fff3cc'},
                                 {'range': [70, 100], 'color': '#ccffcc'}]},
                title={'text': "ATS Score"}
            ))
            fig.update_layout(height=250, margin=dict(t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Contact Info")
            st.write(f"📧 {contact.get('email','Not found')}")
            st.write(f"📞 {contact.get('phone','Not found')}")
            st.write(f"💼 {contact.get('linkedin','Not found')}")
            st.write(f"🐙 {contact.get('github','Not found')}")

        with col3:
            st.subheader("Score Breakdown")
            bd_df = pd.DataFrame({
                'Section': list(breakdown.keys()),
                'Score': list(breakdown.values())
            })
            fig2 = px.bar(bd_df, x='Score', y='Section', orientation='h', color='Score',
                          color_continuous_scale='RdYlGn')
            fig2.update_layout(height=250, margin=dict(t=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)

        # Strengths & Weaknesses
        col4, col5 = st.columns(2)
        with col4:
            st.subheader("✅ Strengths")
            for s in strengths:
                st.success(s)
        with col5:
            st.subheader("❌ Weaknesses")
            for w in weaknesses:
                st.warning(w)

        # Skills Found
        st.subheader("🔧 Skills Found in Resume")
        if flat_skills:
            skill_html = " ".join([f'<span style="background:#e3f2fd;padding:4px 10px;border-radius:15px;margin:3px;display:inline-block;font-size:0.9rem">{s}</span>' for s in flat_skills])
            st.markdown(skill_html, unsafe_allow_html=True)

        # Skill Gap
        st.subheader(f"📊 Skill Gap Analysis for {target_role}")
        target = st.session_state.student_data.get('target_role', 'Data Analyst')
        present, missing, match_pct = analyze_skill_gap(flat_skills, target)
        col6, col7 = st.columns(2)
        with col6:
            st.metric("Match Percentage", f"{match_pct}%")
            for p in present:
                st.success(f"✅ {p}")
        with col7:
            st.write("**Missing Skills:**")
            for m in missing:
                st.error(f"❌ {m}")

        # AI Resume Feedback
        if st.button("🤖 Get AI Resume Feedback"):
            with st.spinner("ChatGPT AI analyze kar raha hai..."):
                feedback = analyze_resume_with_ai(resume_text, target)
                st.info(feedback)


# ============================================
# TAB 2: Placement Prediction
# ============================================
with tabs[1]:
    st.header("Placement Probability Predictor")

    data      = st.session_state.student_data
    skills    = data.get('skills', [])
    ats_score = data.get('ats_score', 50)

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"CGPA: {data.get('cgpa', 7.5)}")
        st.info(f"Skills Count: {len(skills)}")
        st.info(f"ATS Score: {ats_score}")
        st.info(f"Backlogs: {data.get('backlogs', 0)}")
    with col2:
        st.info(f"Internship: {'Yes' if data.get('internship',0) else 'No'}")
        st.info(f"Communication: {data.get('communication', 3)}/5")
        st.info(f"Target Role: {data.get('target_role','N/A')}")

    if st.button("🔮 Predict Placement Probability", type="primary"):
        with st.spinner("ML Model predict kar raha hai..."):
            prob, pred, conf = predict_placement(
                cgpa=data.get('cgpa', 7.0),
                skills_count=len(skills),
                projects_count=min(len(skills)//3, 8),
                certifications_count=min(len(skills)//5, 6),
                internship=data.get('internship', 0),
                communication=data.get('communication', 3),
                backlogs=data.get('backlogs', 0),
                ats_score=ats_score,
                model=st.session_state.ml_model,
                scaler=st.session_state.ml_scaler
            )

            st.session_state.student_data['placement_probability'] = prob

        if prob is not None:
            col1, col2, col3 = st.columns(3)
            col1.metric("Placement Probability", f"{prob}%")
            col2.metric("Prediction", pred)
            col3.metric("Confidence", conf)

            # Progress bar
            st.progress(int(prob) / 100)

            color = "green" if prob >= 70 else "orange" if prob >= 50 else "red"
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prob,
                delta={'reference': 60},
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': color},
                       'steps': [{'range': [0, 40], 'color': '#ffcccc'},
                                 {'range': [40, 70], 'color': '#fff3cc'},
                                 {'range': [70, 100], 'color': '#ccffcc'}],
                       'threshold': {'line': {'color': 'black', 'width': 4}, 'thickness': 0.75, 'value': 60}},
                title={'text': "Placement Probability (%)"}
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Improvement suggestions
            priority, suggestions = get_improvement_suggestions(
                cgpa=data.get('cgpa', 7.0),
                skills_count=len(skills),
                projects_count=min(len(skills)//3, 8),
                certifications_count=min(len(skills)//5, 6),
                internship=data.get('internship', 0),
                communication=data.get('communication', 3),
                backlogs=data.get('backlogs', 0),
                ats_score=ats_score,
                probability=prob
            )
            st.subheader("📝 Improvement Suggestions")
            st.info(priority)
            for sug in suggestions:
                st.warning(f"**{sug['area']}:** {sug['fix']}")


# ============================================
# TAB 3: Job Recommendations
# ============================================
with tabs[2]:
    st.header("Job Recommendations")

    skills = st.session_state.student_data.get('skills', [])
    if not skills:
        st.warning("Pehle Resume Analysis tab mein resume upload karo!")
    else:
        recommendations = recommend_jobs(skills, top_n=6)
        cols = st.columns(2)
        for i, job in enumerate(recommendations):
            with cols[i % 2]:
                color = "🟢" if job['match_score'] >= 70 else "🟡" if job['match_score'] >= 40 else "🔴"
                with st.expander(f"{color} {job['role']} — {job['match_score']}% match"):
                    st.metric("Match Score", f"{job['match_score']}%")
                    st.write(f"💰 **Salary:** {job['avg_salary']}")
                    st.write(f"📈 **Growth:** {job['growth']}")
                    st.write(f"🏢 **Companies:** {', '.join(job['companies'][:3])}")
                    if job['missing_skills']:
                        st.write(f"❌ **Missing:** {', '.join(job['missing_skills'][:4])}")
                    else:
                        st.success("You have all required skills!")

        # Top recommendation career path
        if recommendations:
            top = recommendations[0]
            st.subheader(f"🗺️ Career Path for {top['role']}")
            path = get_career_path(top['role'])
            st.info(f"**Next Step:** {path['next']}")
            for step in path['steps']:
                st.write(f"  ➡️ {step}")


# ============================================
# TAB 4: AI Career Mentor Chatbot
# ============================================
with tabs[3]:
    st.header("🤖 AI Career Mentor")
    st.caption("Apne career ke baare mein kuch bhi poochho!")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Quick questions
    st.subheader("Quick Questions:")
    qcols = st.columns(3)
    quick_qs = [
        "Mujhe kaunsi skills seekhni chahiye?",
        "Mera resume improve kaise karo?",
        "Interview ke liye kaise prepare karoon?"
    ]
    for i, q in enumerate(quick_qs):
        if qcols[i].button(q):
            st.session_state.pending_question = q

    user_question = st.text_input("Apna question yahan likho:", key="user_q",
                                   placeholder="e.g. Mujhe Data Scientist banne ke liye kya karna chahiye?")

    if st.button("Ask AI Mentor 🤖", type="primary") or hasattr(st.session_state, 'pending_question'):
        question = getattr(st.session_state, 'pending_question', user_question)
        if hasattr(st.session_state, 'pending_question'):
            del st.session_state.pending_question

        if question:
            with st.spinner("AI soch raha hai..."):
                response = get_career_guidance(st.session_state.student_data, question)
            st.session_state.chat_history.append({"q": question, "a": response})

    for chat in reversed(st.session_state.chat_history[-5:]):
        st.markdown(f"**You:** {chat['q']}")
        st.info(chat['a'])
        st.divider()

    # Learning Roadmap
    st.subheader("📅 Generate Learning Roadmap")
    skills    = st.session_state.student_data.get('skills', [])
    target    = st.session_state.student_data.get('target_role', 'Data Analyst')
    _, missing, _ = analyze_skill_gap(skills, target)
    months    = st.slider("Kitne months mein seekhna hai?", 1, 6, 3)

    if st.button("Generate Roadmap 🗺️"):
        with st.spinner("Roadmap ban raha hai..."):
            roadmap = generate_learning_roadmap(missing, target, months)
            st.success(roadmap)


# ============================================
# TAB 5: Interview Preparation
# ============================================
with tabs[4]:
    st.header("📝 Interview Preparation")

    col1, col2 = st.columns(2)
    with col1:
        role_for_interview = st.selectbox("Interview Role:", [
            "Data Scientist", "Data Analyst", "Software Engineer",
            "Web Developer", "ML Engineer", "AI Engineer", "Business Analyst"
        ])
    with col2:
        difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard"])

    if st.button("Generate Interview Questions 🎯", type="primary"):
        with st.spinner("ChatGPT AI questions generate kar raha hai..."):
            questions = generate_interview_questions(role_for_interview, difficulty)

        if questions.get('technical'):
            st.subheader("💻 Technical Questions")
            for i, q in enumerate(questions['technical'], 1):
                with st.expander(f"Q{i}: {q[:60]}..."):
                    st.write(q)
                    st.caption("💡 Iska answer prepare karke rakho aur mock interview mein practice karo!")

        if questions.get('hr'):
            st.subheader("🧑 HR Questions")
            for i, q in enumerate(questions['hr'], 1):
                with st.expander(f"HR Q{i}: {q[:60]}..."):
                    st.write(q)

        if questions.get('tips'):
            st.subheader("✨ Interview Tips")
            for tip in questions['tips']:
                st.info(f"💡 {tip}")

    # Interview Tips
    st.divider()
    st.subheader("📌 General Interview Tips")
    tips = [
        "Research the company thoroughly before interview",
        "STAR method use karo (Situation, Task, Action, Result)",
        "Technical concepts clearly explain karo with examples",
        "Projects ke baare mein confidently bolo",
        "Koi baat nahi pata to honestly bolo - 'I don't know but I can learn'",
        "Body language positive rakho, eye contact maintain karo"
    ]
    for tip in tips:
        st.success(f"✅ {tip}")


# Footer
st.divider()
st.markdown('<div style="text-align:center;color:#888;font-size:0.8rem">Placora - AI Placement Mentor | Built with Python, Streamlit & ChatGPT (OpenAI)</div>', unsafe_allow_html=True)
