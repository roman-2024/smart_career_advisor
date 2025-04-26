import streamlit as st
import pickle
import numpy as np



# end open ai code
# Page Config
# ----------------------
st.set_page_config(page_title="Smart Career Advisor", layout="wide")

# ----------------------
# Load Model & Encoder
# ----------------------
model = pickle.load(open('F:\\PROJECT_PIPELINE_MLOPS\\SMART_CARRER_ADVISOR\\models\\logistic_regression_model.pkl', 'rb'))
label_encoder = pickle.load(open('F:\\PROJECT_PIPELINE_MLOPS\\SMART_CARRER_ADVISOR\\models\\label_encoder.pkl', 'rb'))

# ----------------------
# Mappings
# ----------------------
degree_mapping = {'BA': 0, 'BSc': 1, 'Diploma': 2, 'HSC': 3, 'MA': 4, 'MSc': 5, 'SSC': 6}
skills_mapping = {
    'Adobe Illustrator, Photoshop, UI/UX Design': 0,
    'AutoCAD, SolidWorks, Mathematical Modeling': 1,
    'Classroom Management, Communication, Lesson Planning': 2,
    'Data Analysis, Process Improvement, Project Management': 3,
    'Excel, Financial Analysis, QuickBooks': 4,
    'HTML/CSS, JavaScript, React': 5,
    'Machine Learning, Deep Learning, Python': 6,
    'Patient Care, Medical Knowledge, Communication Skills': 7,
    'Python, Machine Learning, Data Visualization': 8,
    'SEO, Social Media Marketing, Content Creation': 9
}
area_mapping = {
    'AI': 0, 'Business': 1, 'Data Science': 2, 'Design': 3,
    'Engineering': 4, 'Finance': 5, 'Healthcare': 6,
    'Marketing': 7, 'Teaching': 8, 'Web Development': 9
}
hobby_mapping = {
    'Drawing': 0, 'Gaming': 1, 'Music': 2,
    'Photography': 3, 'Reading': 4,
    'Traveling': 5, 'Writing': 6
}
subject_mapping = {
    'Artificial Intelligence, ICT': 0,
    'Bangla, English': 1,
    'Business Strategy, Economics': 2,
    'Engineering, Physics': 3,
    'Healthcare, Biology': 4,
    'ICT, Designing': 5,
    'Marketing, Digital Advertising': 6,
    'Mathematics, Accounting': 7,
    'Mathematics, Data Analysis': 8,
    'Web Development, ICT': 9
}
background_mapping = {'nontech': 0, 'tech': 1}

# ----------------------
# Career Guidelines
# ----------------------
career_guidelines = {
    "Data Scientist": {
        "Getting Started": "Python, Statistics, Excel, SQL",
        "Intermediate": "Pandas, Scikit-learn, Data Visualization, Machine Learning",
        "Mastery": "Deep Learning, NLP, Big Data (Spark/Hadoop), MLOps",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Nurse": {
        "Getting Started": "Basic Life Support, Patient Care, Anatomy",
        "Intermediate": "Nursing Procedures, Medical Equipment, Ethics",
        "Mastery": "Specializations (ICU, Pediatrics, etc.), Clinical Practice",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "AI Engineer": {
        "Getting Started": "Python, Linear Algebra, Basic ML",
        "Intermediate": "Deep Learning (CNN, RNN), TensorFlow/PyTorch",
        "Mastery": "Deploying AI Models, Research, Reinforcement Learning",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Graphic Designer": {
        "Getting Started": "Adobe Photoshop, Illustrator, Basic Design Principles",
        "Intermediate": "UI/UX Design, Typography, Portfolio Building",
        "Mastery": "3D Design, Motion Graphics, Branding Strategy",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Mechanical Engineer": {
        "Getting Started": "Engineering Drawing, AutoCAD, Physics",
        "Intermediate": "Thermodynamics, SolidWorks, Machine Design",
        "Mastery": "Robotics, Simulation Software, Advanced Materials",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Digital Marketer": {
        "Getting Started": "SEO, Content Writing, Social Media",
        "Intermediate": "Google Ads, Analytics, Email Marketing",
        "Mastery": "Growth Hacking, Funnel Building, Marketing Strategy",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Web Developer": {
        "Getting Started": "HTML, CSS, JavaScript",
        "Intermediate": "React/Vue, Backend (Node.js, Django), APIs",
        "Mastery": "Full-stack Projects, DevOps, Security",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Teacher": {
        "Getting Started": "Subject Knowledge, Communication Skills",
        "Intermediate": "Lesson Planning, Classroom Management",
        "Mastery": "Education Psychology, EdTech Tools, Research",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Business Analyst": {
        "Getting Started": "Excel, Business Fundamentals, Communication",
        "Intermediate": "SQL, Tableau/Power BI, Requirement Gathering",
        "Mastery": "Data Analysis, Stakeholder Management, Agile/Scrum",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    },
    "Accountant": {
        "Getting Started": "Basic Accounting, Excel, Tally",
        "Intermediate": "Taxation, Financial Statements, QuickBooks",
        "Mastery": "Auditing, Financial Planning, International Standards (IFRS)",
        "Institute": "<span style='color:#FF6347'><b>Daffodil International Professional Training Institute (DIPTI)</b></span>"
    }
}

# ----------------------
# UI Layout
# ----------------------
col1, col2, col3 = st.columns([1.2, 1.5, 1.3])

# -----------------------------------------
# 🎯 LEFT COLUMN - User Input Form
# -----------------------------------------
with col1:
    st.markdown("### 🎯 Smart Career Advisor")

    age = st.slider("Your Age:", 15, 60, 25)
    degree = st.selectbox("Select your Degree:", list(degree_mapping.keys()))
    skill = st.selectbox("Select your Skillset:", list(skills_mapping.keys()))
    experience = st.slider("Years of Experience:", 0, 40, 1)
    area = st.selectbox("Interested Area:", list(area_mapping.keys()))
    hobby = st.selectbox("Select your Hobby:", list(hobby_mapping.keys()))
    subject = st.selectbox("Subjects skilled in:", list(subject_mapping.keys()))
    background = st.radio("Your Background:", list(background_mapping.keys()))

    if st.button("🔮 Predict Career"):
        user_input = [[
            age,
            degree_mapping[degree],
            skills_mapping[skill],
            experience,
            area_mapping[area],
            hobby_mapping[hobby],
            subject_mapping[subject],
            background_mapping[background]
        ]]
        st.session_state['user_input'] = user_input
        st.session_state['predict_now'] = True

# -----------------------------------------
# 📊 MIDDLE COLUMN - Prediction Result
# -----------------------------------------
with col2:
    st.markdown("### 📊 Prediction Result")

    if st.session_state.get('predict_now', False):
        probs = model.predict_proba(np.array(st.session_state['user_input']))[0]
        top_2_indices = np.argsort(probs)[-2:][::-1]
        top_2_careers = label_encoder.inverse_transform(top_2_indices)

        st.success("🎉 Your Top 2 Recommended Career Paths:")
        st.markdown(f"""<h3 style='color: green'>1️⃣ {top_2_careers[0]}</h3>""", unsafe_allow_html=True)
        st.markdown(f"""<h3 style='color: blue'>2️⃣ {top_2_careers[1]}</h3>""", unsafe_allow_html=True)

        for i, career in enumerate(top_2_careers):
            if career in career_guidelines:
                guideline = career_guidelines[career]
                with st.expander(f"📘 Guideline for {career}"):
                    st.markdown(f"""<b>🚀 Getting Started:</b> {guideline["Getting Started"]}""", unsafe_allow_html=True)
                    st.markdown(f"""<b>📈 Intermediate:</b> {guideline["Intermediate"]}""", unsafe_allow_html=True)
                    st.markdown(f"""<b>🎓 Mastery:</b> {guideline["Mastery"]}""", unsafe_allow_html=True)
                    st.markdown(f"""<b>🏫 Suggested Institute:</b> {guideline["Institute"]}""", unsafe_allow_html=True)

# -----------------------------------------
# 🤖 RIGHT COLUMN - ChatBot Placeholder
# 🤖 RIGHT COLUMN - ChatBot Interface (Simple placeholder)
# 🤖 RIGHT COLUMN - ChatBot Interface (Simple placeholder)
# -----------------------------------------
with col3:
    st.header("🤖 Career ChatBot (Demo)")
    
    st.write("This is a demo chatbot interface. Ask something below:")
    user_query = st.text_input("You:", key="chat")
    
    if user_query:
        st.write("Bot: Sorry! I am just a demo for now. More features coming soon 😉")


