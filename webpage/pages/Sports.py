import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Sports Analytics", layout="wide")

# Add sidebar with styling
st.markdown("""
    <style>
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    #MainMenu {
        display: none;
    }
    section[data-testid="stSidebarNav"] {
        display: none;
    }
    .main-title {
        text-align: center;
        color: #1f1f1f;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 30px;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Add main title
st.markdown('<div class="main-title">Sports Analytics</div>', unsafe_allow_html=True)

# Add description text
st.markdown("""
    Welcome to my sports analytics portfolio. Here you'll find various projects and analyses 
    across different sports, focusing on data-driven insights and predictive modeling. My work 
    combines statistical analysis, machine learning, and domain knowledge to extract meaningful 
    patterns from sports data.
    
    Select a sport from the sidebar to explore specific projects and analyses.
""")

# Add sidebar navigation
with st.sidebar:
    st.title("Sports Categories")
    sports_nav = st.radio(
        "Select Sport",
        ["Baseball", "Football", "NFL Big Data Bowl '25 (Kaggle Competition)"],
        key="sports_nav",
        label_visibility="collapsed"
    )

# Handle Sports navigation
if sports_nav == "Baseball":
    st.header("Baseball Analytics")
    st.write("""
    Coming Soon!
    
    Future content will include:
    - Player performance analysis
    - Statistical modeling
    - Predictive analytics
    - Game strategy insights
    """)

elif sports_nav == "Football":
    st.header("Football Analytics")
    st.write("""
    Coming Soon!
    
    Future content will include:
    - Game strategy analysis
    - Player performance metrics
    - Team statistics
    - Predictive modeling
    """)

elif sports_nav == "NFL Big Data Bowl '25 (Kaggle Competition)":
    st.header("NFL Big Data Bowl '25")
    st.write("""
    Coming Soon!
    
    This section will showcase my work on the NFL Big Data Bowl 2025 Kaggle competition, including:
    - Competition approach and methodology
    - Data analysis and visualization
    - Model development
    - Results and insights
    """)