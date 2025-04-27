import streamlit as st
import pickle
import numpy as np
import re


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
with col3:
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🤖 Career ChatBot (Demo)</h2>", unsafe_allow_html=True)
    
    # Additional styling for the chatbot section
    st.markdown("""
        <style>
            .chat-box {
                padding: 20px;
                border-radius: 10px;
                background-color: #f1f1f1;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .user-input {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                width: 100%;
                font-size: 16px;
                margin-bottom: 10px;
            }
            .bot-response {
                background-color: #dcdcdc;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
                font-weight: bold;
            }
            .ask-button {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                cursor: pointer;
                width: 100%;
            }
            .ask-button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)

    st.write("This is a demo chatbot interface. Ask something below:")

    # Input text field with customized style
    user_query = st.text_input("You:", key="chat", placeholder="Ask your career-related query here...", label_visibility="collapsed")

    if user_query:
        # Styled response area
        st.markdown(f"""<div class="bot-response">Bot: Sorry! I am just a demo for now. More features coming soon 😉</div>""", unsafe_allow_html=True)

    # Ask button to submit query
    if st.button("💬 Ask", key="chat_button", help="Submit your query to ChatBot"):
        st.markdown(f"""<div class="bot-response">Bot: Sorry! I am just a demo for now. More features coming soon 😉</div>""", unsafe_allow_html=True)


# -----------------------------------------
# Resume Recommendation System - Below Layout
# -----------------------------------------
st.markdown("---")
resume_model = pickle.load(open('F:\\PROJECT_PIPELINE_MLOPS\\SMART_CARRER_ADVISOR\\models\\model.pkl', 'rb'))
resume_tfidf = pickle.load(open('F:\\PROJECT_PIPELINE_MLOPS\\SMART_CARRER_ADVISOR\\models\\tfidf.pkl', 'rb'))
resume_label_encoder = pickle.load(open('F:\\PROJECT_PIPELINE_MLOPS\\SMART_CARRER_ADVISOR\\models\\label_encoders.pkl', 'rb'))

# Text cleaning function
def clean_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', text)  # Remove non-alphabetic characters
    text = text.lower()  # Lowercase
    text = re.sub(r'\s+', ' ', text)  # Remove multiple spaces
    text = text.strip()  # Trim spaces
    return text
# Resume Input
# -----------------------------------------
# Resume Recommendation System - Below Layout
# -----------------------------------------
st.markdown("<h2 style='text-align: center; color: #FF6347;'>Resume Recommendation System</h2>", unsafe_allow_html=True)

# Styling for the section
st.markdown("""
    <style>
        .resume-section {
            padding: 30px;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
        }
        .section-header {
            font-size: 24px;
            color: #2d2d2d;
            text-align: center;
            font-weight: bold;
        }
        .resume-textarea {
            width: 100%;
            height: 300px;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 16px;
            margin-top: 20px;
        }
        .predict-btn {
            background-color: #FF6347;
            color: white;
            border-radius: 5px;
            padding: 12px 20px;
            font-size: 16px;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .predict-btn:hover {
            background-color: #e53d26;
        }
    </style>
""", unsafe_allow_html=True)

# Text Input for Resume
user_resume = st.text_area("📝 Paste your Resume Text below (200–300 words):", height=300, key="resume_input", placeholder="Write or paste your resume here...")

# Predict Button
predict_button = st.button("🔍 Predict Career Path", key="predict_button", help="Click to predict the career path based on your resume")

# Display the section with resume input
# Initialize prediction_decoded outside the container to avoid reference error
# Initialize prediction_decoded outside the container to avoid reference error
prediction_decoded = None

with st.container():
    st.markdown("<div class='resume-section'>", unsafe_allow_html=True)

    # Predict button logic
    if predict_button:
        if user_resume.strip() != "":
            # Clean the input text
            cleaned_resume = clean_text(user_resume)

            # Transform the text using loaded TFIDF
            resume_text_transformed = resume_tfidf.transform([cleaned_resume])

            # Predict career path
            prediction_encoded = resume_model.predict(resume_text_transformed)[0]

            # Decode the prediction
            prediction_decoded = resume_label_encoder.inverse_transform([prediction_encoded])[0]

            # Display result with enhanced styles
            st.success(f"🎯 Recommended Career Path: **{prediction_decoded}**", icon="✅")
        else:
            st.warning("⚠️ Please write your resume summary before predicting.", icon="⚠️")

    st.markdown("</div>", unsafe_allow_html=True)

# Ensure the variable is only used when prediction_decoded is available
if prediction_decoded:
    # Display the result with larger font size, color, and additional instructions
    st.markdown(f"""
        <div style="background-color: #333; padding: 20px; border-radius: 10px;">
            <h2 style='color: #FF6347; font-size: 36px; text-align: center;'>🎯 This career path is the best for you to succeed!</h2>
            <p style='font-size: 24px; text-align: center; color: #FFFAFA;'>According to your resume, <strong style="font-size: 30px; color: #FFD700;">{prediction_decoded}</strong> is the best career path.</p>
            <p style='font-size: 20px; text-align: center; color: #4CAF50;'>Now, here are some important tips to prepare for this career:</p>
            <ul style='font-size: 18px; color: #FFFAFA;'>
                <li>1. Start learning relevant skills and tools.</li>
                <li>2. Consider enrolling in professional courses or following online tutorials.</li>
                <li>3. Gain work experience by working on projects.</li>
                <li>4. Stay updated with industry trends and new technologies.</li>
                <li>5. Focus on self-development and learn from mentors in the field.</li>
            </ul>
            <p style='font-size: 18px; text-align: center; color: #777;'>This is general advice, but you can create new plans based on your journey.</p>
        </div>
    """, unsafe_allow_html=True)



