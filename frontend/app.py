import os
import streamlit as st
import requests
import json
import time
from typing import Dict, List, Any

# API Configuration
API_BASE_URL = os.getenv("BACKEND_URL", "http://20.238.165.133:8000")

# Set the backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://20.238.165.133:8000")

def main():
    st.set_page_config(
        page_title="Personalized Educational Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced CSS for better readability and modern design
    st.markdown("""
    <style>
    /* Global app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar background */
    .stSidebar {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    }

    /* Main content text */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
    .main .stMarkdown, .main .stMarkdown p, .main .stMarkdown h1, .main .stMarkdown h2, 
    .main .stMarkdown h3, .main .stMarkdown h4, .main .stMarkdown h5, .main .stMarkdown h6 {
        color: #000000 !important;
        line-height: 1.6 !important;
    }

    /* Sidebar text (default = white, inputs stay black) */
    .stSidebar * {
        color: white !important;
    }
    .stSidebar input[type="text"],
    .stSidebar input[type="email"], 
    .stSidebar input[type="password"] {
        color: #000000 !important;
    }

    /* Metrics */
    .stMetric, .stMetric > div, .stMetric > div > div {
        color: #000000 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #000000 !important;
        border: 2px solid #e9ecef !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25) !important;
        transform: translateY(-2px) !important;
        outline: none !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    /* Headers (hero style) */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white !important;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
        color: white !important;
    }

    /* Card container for equal layout */
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        justify-content: center;
    }
    .card-container > div {
        flex: 1 1 calc(33.333% - 1.5rem);
        min-width: 250px;
        max-width: 400px;
    }

    /* Cards */
    .quiz-card, .stats-card, .learning-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        color: #000000 !important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 180px;
    }
    .quiz-card:hover, .stats-card:hover, .learning-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    .quiz-card h4, .stats-card h3, .learning-card h3 {
        color: #000000 !important;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    .quiz-card p, .stats-card p, .learning-card p {
        color: #000000 !important;
    }

    /* Feedback messages */
    .stSuccess, .correct-answer {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border: 1px solid #28a745 !important;
        border-radius: 12px !important;
        color: #000000 !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    .stError, .incorrect-answer {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border: 1px solid #dc3545 !important;
        border-radius: 12px !important;
        color: #000000 !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%) !important;
        border: 1px solid #ffc107 !important;
        border-radius: 12px !important;
        color: #000000 !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%) !important;
        border: 1px solid #17a2b8 !important;
        border-radius: 12px !important;
        color: #000000 !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }

    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-header { padding: 1.5rem; margin-bottom: 1rem; }
        .main-header h1 { font-size: 2rem; }
        .quiz-card, .stats-card, .learning-card { padding: 1.5rem; margin: 0.5rem 0; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Personalized Educational Assistant</h1>
        <p>AI-powered learning platform with personalized explanations, interactive quizzes, and learning paths</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for authentication
    with st.sidebar:
        show_authentication_sidebar()
    
    # Main content
    if st.session_state.access_token is None:
        show_landing_page()
        return
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 Learn", "🧠 Quiz", "🗺️ Learning Path", "�� Dashboard", "👤 Profile"])
    
    with tab1:
        show_learning_tab()
    
    with tab2:
        show_enhanced_quiz_tab()
    
    with tab3:
        show_learning_path_tab()
    
    with tab4:
        show_dashboard_tab()
    
    with tab5:
        show_profile_tab()


def initialize_session_state():
    """Initialize session state variables"""
    if 'access_token' not in st.session_state:
        st.session_state.access_token = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'learning_sessions' not in st.session_state:
        st.session_state.learning_sessions = []
    if 'learning_progress' not in st.session_state:
        st.session_state.learning_progress = []
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Learn"
    if 'quiz_topic' not in st.session_state:
        st.session_state.quiz_topic = ""

def show_authentication_sidebar():
    """Show authentication sidebar"""
    st.header("🔐 Authentication")
    
    if st.session_state.access_token is None:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if login_user(email, password):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Login failed. Please check your credentials.")
        
        with tab2:
            st.subheader("Register")
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            
            if st.button("Register", type="primary", use_container_width=True):
                if register_user(reg_username, reg_email, reg_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed. Please try again.")
    else:
        st.success("✅ Logged in")
        st.markdown(f"**Welcome, {st.session_state.user_profile.get('username', 'User')}!**")
        if st.button("Logout", use_container_width=True):
            st.session_state.access_token = None
            st.session_state.user_profile = None
            st.session_state.current_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_score = 0
            st.rerun()

def show_landing_page():
    """Show landing page for non-authenticated users"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h3>🤖 AI-Powered Learning</h3>
            <p>Get personalized explanations tailored to your learning style and difficulty level.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h3>🧠 Interactive Quizzes</h3>
            <p>Test your knowledge with AI-generated quizzes and get instant feedback.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-card">
            <h3>🗺️ Learning Paths</h3>
            <p>Follow personalized learning paths designed for your goals and skill level.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔐Get Started")
    st.markdown("Create an account or login to access all features and start your personalized learning journey!")

def show_learning_tab():
    """Enhanced learning tab"""
    st.header("📚 Learn with AI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("What topic would you like to learn about?", 
                             placeholder="e.g., Python Functions, Machine Learning, Calculus")
        user_question = st.text_area("What specific question do you have?", 
                                   placeholder="e.g., How do I create a function in Python?")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("Get AI Explanation", type="primary", use_container_width=True):
                if topic and user_question:
                    with st.spinner("Generating personalized explanation..."):
                        explanation = get_ai_explanation(topic, user_question)
                        if explanation:
                            st.session_state.learning_sessions.append({
                                "topic": topic,
                                "question": user_question,
                                "explanation": explanation,
                                "timestamp": time.time()
                            })
                            st.markdown("### 🤖 AI Explanation")
                            st.markdown(explanation)
                        else:
                            st.error("Failed to generate explanation. Please try again.")
                else:
                    st.warning("Please enter both a topic and your question.")
        
        with col_btn2:
            if st.button("Clear", use_container_width=True):
                st.rerun()
    
    with col2:
        st.markdown("### 💡 Learning Tips")
        st.markdown("""
        - Be specific with your questions
        - Mention your current level if relevant
        - Ask for examples or analogies
        - Request step-by-step explanations
        """)
        
        if st.session_state.learning_sessions:
            st.markdown("### 🕒 Recent Sessions")
            for i, session in enumerate(st.session_state.learning_sessions[-3:]):
                with st.expander(f"Session {i+1}: {session['topic']}"):
                    st.markdown(f"**Question:** {session['question']}")
                    st.markdown(f"**Explanation:** {session['explanation'][:100]}...")

def show_enhanced_quiz_tab():
    """Enhanced quiz tab with interactive experience"""
    st.header("🧠 Interactive Quiz Experience")
    
    if not st.session_state.current_quiz:
        show_quiz_generation()
    else:
        show_quiz_taking()

def show_quiz_generation():
    """Show quiz generation interface"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Create Your Quiz")
        quiz_topic = st.text_input("Quiz Topic", placeholder="e.g., Python Functions")
        difficulty = st.selectbox("Difficulty Level", ["beginner", "intermediate", "advanced"])
        num_questions = st.slider("Number of Questions", 1, 10, 5)
        
        if st.button("Generate Quiz", type="primary", use_container_width=True):
            if quiz_topic:
                with st.spinner("Generating quiz questions..."):
                    quiz_data = generate_quiz(quiz_topic, difficulty, num_questions)
                    
                    if quiz_data and "questions" in quiz_data:
                        st.session_state.current_quiz = quiz_data
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_score = 0
                        st.success(f"Generated {len(quiz_data['questions'])} questions!")
                        st.rerun()
                    else:
                        st.error("Failed to generate quiz. Please try again.")
            else:
                st.warning("Please enter a quiz topic.")
    
    with col2:
        st.markdown("### 📊 Quiz Tips")
        st.markdown("""
        - Choose topics you've studied
        - Start with easier difficulty
        - Take your time with each question
        - Review explanations after answering
        """)

# def show_quiz_taking():
#     """Show interactive quiz taking interface"""
#     quiz = st.session_state.current_quiz
#     total_questions = len(quiz["questions"])
    
#     # Progress bar
#     progress = len(st.session_state.quiz_answers) / total_questions
#     st.markdown(f"""
#     <div class="progress-bar">
#         <div class="progress-fill" style="width: {progress * 100}%;"></div>
#     </div>
#     <p>Progress: {len(st.session_state.quiz_answers)}/{total_questions} questions answered</p>
#     """, unsafe_allow_html=True)
    
#     # Quiz questions
#     for i, question in enumerate(quiz["questions"]):
#         question_key = f"question_{i}"
        
#         if question_key not in st.session_state.quiz_answers:
#             st.markdown(f"""
#             <div class="quiz-card">
#                 <h4>Question {i+1}: {question['question']}</h4>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Answer options
#             selected_answer = st.radio(
#                 "Choose your answer:",
#                 options=question["options"],
#                 key=f"radio_{i}",
#                 index=None
#             )
            
#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 if st.button(f"Submit Answer {i+1}", key=f"submit_{i}", type="primary"):
#                     if selected_answer is not None:
#                         answer_index = question["options"].index(selected_answer)
#                         is_correct = answer_index == question["correct_answer"]
                        
#                         st.session_state.quiz_answers[question_key] = {
#                             "selected": answer_index,
#                             "correct": question["correct_answer"],
#                             "is_correct": is_correct,
#                             "explanation": question["explanation"]
#                         }
                        
#                         if is_correct:
#                             st.session_state.quiz_score += 1
                        
#                         st.rerun()
#                     else:
#                         st.warning("Please select an answer.")
            
#             with col2:
#                 if st.button(f"Skip Question {i+1}", key=f"skip_{i}"):
#                     st.session_state.quiz_answers[question_key] = {
#                         "selected": None,
#                         "correct": question["correct_answer"],
#                         "is_correct": False,
#                         "explanation": question["explanation"]
#                     }
#                     st.rerun()
            
#             st.markdown("---")
#         else:
#             # Show answered question
#             answer_data = st.session_state.quiz_answers[question_key]
#             if answer_data["selected"] is not None:
#                 selected_text = question["options"][answer_data["selected"]]
#                 correct_text = question["options"][answer_data["correct"]]
                
#                 if answer_data["is_correct"]:
#                     st.markdown(f"""
#                     <div class="correct-answer">
#                         <h4>✅ Question {i+1}: {question['question']}</h4>
#                         <p><strong>Your Answer:</strong> {selected_text} (Correct!)</p>
#                         <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div class="incorrect-answer">
#                         <h4>❌ Question {i+1}: {question['question']}</h4>
#                         <p><strong>Your Answer:</strong> {selected_text}</p>
#                         <p><strong>Correct Answer:</strong> {correct_text}</p>
#                         <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div class="quiz-card">
#                     <h4>⏭️ Question {i+1}: {question['question']} (Skipped)</h4>
#                     <p><strong>Correct Answer:</strong> {question['options'][answer_data['correct']]}</p>
#                     <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
#                 </div>
#                 """, unsafe_allow_html=True)
    
#     # Quiz completion
#     if len(st.session_state.quiz_answers) == total_questions:
#         show_quiz_results()

# def show_quiz_taking():
#     """Show interactive quiz taking interface"""
#     quiz = st.session_state.current_quiz
#     total_questions = len(quiz["questions"])
    
#     # Progress bar
#     progress = len(st.session_state.quiz_answers) / total_questions
#     st.markdown(f"""
#     <div class="progress-bar">
#         <div class="progress-fill" style="width: {progress * 100}%;"></div>
#     </div>
#     <p>Progress: {len(st.session_state.quiz_answers)}/{total_questions} questions answered</p>
#     """, unsafe_allow_html=True)
    
#     # Quiz questions
#     for i, question in enumerate(quiz["questions"]):
#         question_key = f"question_{i}"
        
#         if question_key not in st.session_state.quiz_answers:
#             st.markdown(f"""
#             <div class="quiz-card">
#                 <h4>Question {i+1}: {question['question']}</h4>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Answer options
#             selected_answer = st.radio(
#                 "Choose your answer:",
#                 options=question["options"],
#                 key=f"radio_{i}",
#                 index=None
#             )
            
#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 if st.button(f"Submit Answer {i+1}", key=f"submit_{i}", type="primary"):
#                     if selected_answer is not None:
#                         answer_index = question["options"].index(selected_answer)
#                         # Fix: Use the correct key for correct answer
#                         correct_answer_index = question.get("correct_answer", 0)
#                         is_correct = answer_index == correct_answer_index
                        
#                         st.session_state.quiz_answers[question_key] = {
#                             "selected": answer_index,
#                             "correct": correct_answer_index,
#                             "is_correct": is_correct,
#                             "explanation": question.get("explanation", "No explanation available")
#                         }
                        
#                         if is_correct:
#                             st.session_state.quiz_score += 1
                        
#                         st.rerun()
#                     else:
#                         st.warning("Please select an answer.")
            
#             with col2:
#                 if st.button(f"Skip Question {i+1}", key=f"skip_{i}"):
#                     correct_answer_index = question.get("correct_answer", 0)
#                     st.session_state.quiz_answers[question_key] = {
#                         "selected": None,
#                         "correct": correct_answer_index,
#                         "is_correct": False,
#                         "explanation": question.get("explanation", "No explanation available")
#                     }
#                     st.rerun()
            
#             st.markdown("---")
#         else:
#             # Show answered question
#             answer_data = st.session_state.quiz_answers[question_key]
#             if answer_data["selected"] is not None:
#                 selected_text = question["options"][answer_data["selected"]]
#                 correct_text = question["options"][answer_data["correct"]]
                
#                 if answer_data["is_correct"]:
#                     st.markdown(f"""
#                     <div class="correct-answer">
#                         <h4>✅ Question {i+1}: {question['question']}</h4>
#                         <p><strong>Your Answer:</strong> {selected_text} (Correct!)</p>
#                         <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div class="incorrect-answer">
#                         <h4>❌ Question {i+1}: {question['question']}</h4>
#                         <p><strong>Your Answer:</strong> {selected_text}</p>
#                         <p><strong>Correct Answer:</strong> {correct_text}</p>
#                         <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
#                     </div>
#                     """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div class="quiz-card">
#                     <h4>⏭️ Question {i+1}: {question['question']} (Skipped)</h4>
#                     <p><strong>Correct Answer:</strong> {question['options'][answer_data['correct']]}</p>
#                     <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
#                 </div>
#                 """, unsafe_allow_html=True)
    
#     # Quiz completion
#     if len(st.session_state.quiz_answers) == total_questions:
#         show_quiz_results()

def show_quiz_taking():
    """Show interactive quiz taking interface"""
    quiz = st.session_state.current_quiz
    total_questions = len(quiz["questions"])
    
    # Progress bar
    progress = len(st.session_state.quiz_answers) / total_questions
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%;"></div>
    </div>
    <p>Progress: {len(st.session_state.quiz_answers)}/{total_questions} questions answered</p>
    """, unsafe_allow_html=True)
    
    # Quiz questions
    for i, question in enumerate(quiz["questions"]):
        question_key = f"question_{i}"
        
        if question_key not in st.session_state.quiz_answers:
            st.markdown(f"""
            <div class="quiz-card">
                <h4>Question {i+1}: {question['question']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Answer options
            selected_answer = st.radio(
                "Choose your answer:",
                options=question["options"],
                key=f"radio_{i}",
                index=None
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Submit Answer {i+1}", key=f"submit_{i}", type="primary"):
                    if selected_answer is not None:
                        answer_index = question["options"].index(selected_answer)
                        # Fix: Get the correct answer index properly
                        correct_answer_index = int(question.get("correct_answer", 0))
                        
                        # Debug: Show what we're comparing
                        st.write(f"🔍 Debug: Selected index: {answer_index}, Correct index: {correct_answer_index}")
                        st.write(f"🔍 Debug: Selected text: '{selected_answer}'")
                        st.write(f"🔍 Debug: Correct text: '{question['options'][int(correct_answer_index)]}'")
                        
                        is_correct = answer_index == correct_answer_index
                        
                        st.session_state.quiz_answers[question_key] = {
                            "selected": answer_index,
                            "correct": correct_answer_index,
                            "is_correct": is_correct,
                            "explanation": question.get("explanation", "No explanation available")
                        }
                        
                        if is_correct:
                            st.session_state.quiz_score += 1
                        
                        st.rerun()
                    else:
                        st.warning("Please select an answer.")
            
            with col2:
                if st.button(f"Skip Question {i+1}", key=f"skip_{i}"):
                    correct_answer_index = question.get("correct_answer", 0)
                    st.session_state.quiz_answers[question_key] = {
                        "selected": None,
                        "correct": correct_answer_index,
                        "is_correct": False,
                        "explanation": question.get("explanation", "No explanation available")
                    }
                    st.rerun()
            
            st.markdown("---")
        else:
            # Show answered question
            answer_data = st.session_state.quiz_answers[question_key]
            if answer_data["selected"] is not None:
                selected_text = question["options"][answer_data["selected"]]
                correct_text = question["options"][answer_data["correct"]]
                
                if answer_data["is_correct"]:
                    st.markdown(f"""
                    <div class="correct-answer">
                        <h4>✅ Question {i+1}: {question['question']}</h4>
                        <p><strong>Your Answer:</strong> {selected_text} (Correct!)</p>
                        <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="incorrect-answer">
                        <h4>❌ Question {i+1}: {question['question']}</h4>
                        <p><strong>Your Answer:</strong> {selected_text}</p>
                        <p><strong>Correct Answer:</strong> {correct_text}</p>
                        <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="quiz-card">
                    <h4>⏭️ Question {i+1}: {question['question']} (Skipped)</h4>
                    <p><strong>Correct Answer:</strong> {question['options'][answer_data['correct']]}</p>
                    <p><strong>Explanation:</strong> {answer_data['explanation']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Quiz completion
    if len(st.session_state.quiz_answers) == total_questions:
        show_quiz_results()

def show_quiz_results():
    """Show quiz results and statistics"""
    quiz = st.session_state.current_quiz
    total_questions = len(quiz["questions"])
    score = st.session_state.quiz_score
    percentage = (score / total_questions) * 100
    
    st.markdown("### 🎉 Quiz Complete!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Score", f"{score}/{total_questions}")
    
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    
    with col3:
        if percentage >= 80:
            st.metric("Grade", "A+ 🏆")
        elif percentage >= 70:
            st.metric("Grade", "B+ 👍")
        elif percentage >= 60:
            st.metric("Grade", "C+ ✅")
        else:
            st.metric("Grade", "Needs Improvement 📚")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Take Another Quiz", type="primary"):
            st.session_state.current_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_score = 0
            st.rerun()
    
    with col2:
        if st.button("Review Answers"):
            st.rerun()
    
    with col3:
        if st.button("Save Results"):
            st.success("Results saved to your learning history!")

def show_learning_path_tab():
    """Enhanced learning path tab"""
    st.header("🗺️ Personalized Learning Path")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        path_topic = st.text_input("Learning Path Topic", placeholder="e.g., Machine Learning, Web Development")
        current_level = st.selectbox("Your Current Level", ["beginner", "intermediate", "advanced"])
        
        st.markdown("**Learning Goals (optional):**")
        goal1 = st.text_input("Goal 1", placeholder="e.g., Build a web application")
        goal2 = st.text_input("Goal 2", placeholder="e.g., Understand data analysis")
        goal3 = st.text_input("Goal 3", placeholder="e.g., Learn about algorithms")
        
        goals = [g for g in [goal1, goal2, goal3] if g.strip()]
        
        if st.button("Generate Learning Path", type="primary", use_container_width=True):
            if path_topic:
                with st.spinner("Creating personalized learning path..."):
                    learning_path = generate_learning_path(path_topic, current_level, goals)
                    if learning_path and "modules" in learning_path:
                        st.session_state.current_learning_path = learning_path
                        st.success("Learning path generated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to generate learning path. Please try again.")
            else:
                st.warning("Please enter a learning path topic.")
    
    with col2:
        st.markdown("### �� Learning Tips")
        st.markdown("""
        - Set clear, achievable goals
        - Be honest about your current level
        - Follow the suggested order
        - Practice regularly
        - Track your progress
        """)
    
    # Display learning path if available
    if 'current_learning_path' in st.session_state:
        display_learning_path(st.session_state.current_learning_path)

def show_dashboard_tab():
    """Enhanced dashboard with better analytics and visualizations"""
    st.header("📊 Learning Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card(
            "Learning Sessions", 
            str(len(st.session_state.learning_sessions)),
            f"+{len(st.session_state.learning_sessions)} this week" if st.session_state.learning_sessions else "Start learning!"
        )
    
    with col2:
        quiz_count = len([q for q in st.session_state.quiz_answers.values() if q.get("selected") is not None])
        create_metric_card(
            "Quizzes Taken", 
            str(quiz_count),
            "Keep it up!" if quiz_count > 0 else "Take your first quiz"
        )
    
    with col3:
        if st.session_state.quiz_score > 0:
            avg_score = (st.session_state.quiz_score / max(1, quiz_count)) * 100
            create_metric_card(
                "Average Score", 
                f"{avg_score:.1f}%",
                "Excellent!" if avg_score > 80 else "Good progress!" if avg_score > 60 else "Keep practicing!"
            )
        else:
            create_metric_card("Average Score", "N/A", "Take quizzes to see your score")
    
    with col4:
        # Calculate learning streak
        if st.session_state.learning_sessions:
            create_metric_card(
                "Learning Streak", 
                f"{len(st.session_state.learning_sessions)} days",
                "🔥 Amazing!"
            )
        else:
            create_metric_card("Learning Streak", "0 days", "Start your journey!")
    
    st.markdown("---")
    
    # Learning progress visualization
    if st.session_state.learning_sessions:
        st.markdown("### 📈 Learning Activity")
        
        # Topics chart
        topics = [session["topic"] for session in st.session_state.learning_sessions]
        topic_counts = {}
        for topic in topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Create a more detailed chart
        chart_data = {
            "Topic": list(topic_counts.keys()),
            "Sessions": list(topic_counts.values())
        }
        
        st.bar_chart(chart_data, height=300)
        
        # Learning path progress
        if 'current_learning_path' in st.session_state:
            st.markdown("### 🗺️ Current Learning Path Progress")
            learning_path = st.session_state.current_learning_path
            
            # Create a progress visualization for learning path
            modules = learning_path.get('modules', [])
            if modules:
                for i, module in enumerate(modules, 1):
                    with st.expander(f"Module {i}: {module.get('title', 'Untitled')} - {'✅ Completed' if i <= 2 else '⏳ In Progress' if i == 3 else '⏸️ Not Started'}"):
                        st.markdown(f"**Description:** {module.get('description', 'N/A')}")
                        st.markdown(f"**Duration:** {module.get('duration', 'N/A')}")
                        
                        if module.get('prerequisites'):
                            st.markdown("**Prerequisites:**")
                            for prereq in module['prerequisites']:
                                st.markdown(f"- {prereq}")
                        
                        if module.get('objectives'):
                            st.markdown("**Learning Objectives:**")
                            for obj in module['objectives']:
                                st.markdown(f"- {obj}")
    
    # Recent activity with enhanced styling
    st.markdown("### 🕒 Recent Activity")
    if st.session_state.learning_sessions:
        for i, session in enumerate(st.session_state.learning_sessions[-5:]):
            with st.expander(f"📚 {session['topic']} - {time.strftime('%Y-%m-%d %H:%M', time.localtime(session['timestamp']))}"):
                st.markdown(f"**Question:** {session['question']}")
                st.markdown(f"**Explanation:** {session['explanation'][:200]}...")
                
                # Add action buttons
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"View Full Explanation", key=f"view_{i}"):
                        st.markdown("**Full Explanation:**")
                        st.markdown(session['explanation'])
                with col2:
                    if st.button(f"Create Quiz", key=f"quiz_{i}"):
                        st.session_state.quiz_topic = session['topic']
                        st.rerun()
    else:
        st.info("No learning sessions yet. Start learning to see your activity here!")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Start Learning", use_container_width=True):
            st.session_state.active_tab = "Learn"
            st.rerun()
    
    with col2:
        if st.button("🧠 Take Quiz", use_container_width=True):
            st.session_state.active_tab = "Quiz"
            st.rerun()
    
    with col3:
        if st.button("🗺️ Learning Path", use_container_width=True):
            st.session_state.active_tab = "Learning Path"
            st.rerun()

def show_profile_tab():
    """Enhanced profile tab"""
    st.header("👤 Your Profile")
    
    if st.session_state.user_profile:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Profile Information")
            st.json(st.session_state.user_profile)
        
        with col2:
            st.markdown("### Learning Preferences")
            st.info("Profile preferences will be available in future updates.")
    else:
        st.info("Profile information not available.")

def display_learning_path(learning_path: Dict):
    """Display learning path with enhanced styling"""
    st.markdown("### ��️ Your Learning Path")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"**Topic:** {learning_path.get('topic', 'N/A')}")
        st.markdown(f"**Current Level:** {learning_path.get('current_level', 'N/A')}")
    
    with col2:
        st.markdown(f"**Total Estimated Time:** {learning_path.get('total_estimated_time', 'N/A')}")
    
    st.markdown("**Learning Goals:**")
    for goal in learning_path.get('learning_goals', []):
        st.markdown(f"- {goal}")
    
    st.markdown("**Modules:**")
    for i, module in enumerate(learning_path.get('modules', []), 1):
        with st.expander(f"Module {i}: {module.get('title', 'Untitled')}"):
            st.markdown(f"**Description:** {module.get('description', 'N/A')}")
            st.markdown(f"**Duration:** {module.get('duration', 'N/A')}")
            
            if module.get('prerequisites'):
                st.markdown("**Prerequisites:**")
                for prereq in module['prerequisites']:
                    st.markdown(f"- {prereq}")
            
            if module.get('objectives'):
                st.markdown("**Learning Objectives:**")
                for obj in module['objectives']:
                    st.markdown(f"- {obj}")

# API functions (same as before)
def login_user(email: str, password: str) -> bool:
    """Login user and store token"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data["access_token"]
            st.session_state.user_profile = data["user"]
            return True
        else:
            st.error(f"Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def register_user(username: str, email: str, password: str) -> bool:
    """Register new user"""
    try:
        response = requests.post(f"{API_BASE_URL}/api/auth/register", json={
            "username": username,
            "email": email,
            "password": password
        })
        return response.status_code == 200
    except Exception as e:
        st.error(f"Registration error: {str(e)}")
        return False

def get_ai_explanation(topic: str, user_input: str) -> str:
    """Get AI explanation"""
    try:
        # Input validation
        if not topic.strip() or not user_input.strip():
            st.error("Please provide both topic and question.")
            return None
        
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.post(f"{API_BASE_URL}/api/ai/explain", 
                               json={"topic": topic, "user_input": user_input},
                               headers=headers)
        
        if response.status_code == 200:
            return response.json()["explanation"]
        elif response.status_code == 400:
            error_data = response.json()
            st.error(f"Validation error: {error_data.get('detail', 'Invalid input')}")
            return None
        elif response.status_code == 401:
            st.error("Authentication failed. Please login again.")
            return None
        else:
            st.error(f"Server error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Please check if the backend is running.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

# def generate_quiz(topic: str, difficulty: str, num_questions: int) -> Dict:
#     """Generate quiz"""
#     try:
#         headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
#         response = requests.post(f"{API_BASE_URL}/api/ai/quiz/generate",
#                                json={"topic": topic, "difficulty_level": difficulty, "num_questions": num_questions},
#                                headers=headers)
        
#         if response.status_code == 200:
#             return response.json()
#         return None
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return None

def generate_quiz(topic: str, difficulty: str, num_questions: int) -> Dict:
    """Generate quiz"""
    try:
        # Input validation
        if not topic.strip():
            st.error("Please enter a quiz topic.")
            return None
        
        if num_questions < 1 or num_questions > 20:
            st.error("Number of questions must be between 1 and 20.")
            return None
        
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.post(f"{API_BASE_URL}/api/ai/quiz/generate",
                               json={"topic": topic, "difficulty_level": difficulty, "num_questions": num_questions},
                               headers=headers)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            error_data = response.json()
            st.error(f"Validation error: {error_data.get('detail', 'Invalid input')}")
            return None
        elif response.status_code == 401:
            st.error("Authentication failed. Please login again.")
            return None
        else:
            st.error(f"Server error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Please check if the backend is running.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def generate_learning_path(topic: str, current_level: str, goals: List[str]) -> Dict:
    """Generate learning path"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.post(f"{API_BASE_URL}/api/ai/learning-path",
                               json={"topic": topic, "current_level": current_level, "learning_goals": goals},
                               headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def show_loading_animation(message: str):
    """Show a loading animation with message"""
    with st.spinner(message):
        time.sleep(0.5)  # Small delay for better UX

def show_success_message(message: str):
    """Show a success message with animation"""
    st.success(f"✅ {message}")
    time.sleep(1)

def show_error_message(message: str):
    """Show an error message with styling"""
    st.error(f"❌ {message}")

def create_progress_bar(current: int, total: int, label: str = "Progress"):
    """Create an animated progress bar"""
    progress = current / total
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%;">
            {label}: {current}/{total}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title: str, value: str, delta: str = None, delta_color: str = "normal"):
    """Create a styled metric card"""
    delta_html = f'<div style="color: {delta_color}; font-size: 0.8rem;">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-container">
        <h3>{title}</h3>
        <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()