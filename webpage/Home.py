import streamlit as st
import base64

# Set the page title and layout
st.set_page_config(page_title="Home Page", layout="wide", initial_sidebar_state="collapsed")

# Hide the sidebar completely and adjust padding
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        #MainMenu {
            display: none;
        }
        .block-container {
            padding: 3rem 1rem 1rem 1rem !important;
        }
        div[data-testid="stToolbar"] {
            visibility: hidden;
        }
        .nav-links {
            display: flex;
            justify-content: center;
            padding: 20px;
            background-color: #f8f9fa;
            margin-bottom: 30px;
            position: relative;
            z-index: 1000;
        }
        .nav-links a {
            margin: 0 20px;
            padding: 8px 16px;
            text-decoration: none;
            color: #1f1f1f;
            font-size: 18px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .nav-links a:hover {
            background-color: #e9ecef;
        }
        .paragraph {
            max-width: 800px;
            margin: 0 auto 30px auto;
            text-align: justify;
            line-height: 1.8;
            font-size: 18px;
            color: #333;
            padding: 0 20px;
        }
        /* Center the button container */
        .download-button-container {
            display: flex;
            justify-content: center;
            margin-top: 40px;
            padding: 20px;
        }
        
        /* Button styling */
        .stButton {
            text-align: center;
        }
        .stButton > button {
            background-color: #0066cc;
            color: white;
            padding: 12px 30px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #0052a3;
        }
    </style>
""", unsafe_allow_html=True)

# Add navigation
st.markdown("""
    <div class="nav-links">
        <a href="Finance">Finance</a>
    </div>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
    <div class="paragraph">
    Welcome, my name is John Binek, and I am a data-driven problem-solver with expertise in Python, R, and SQL. 
    This page showcases my technical skillset and highlights projects I’ve worked on, reflecting my ability to tackle complex challenges across various domains.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="paragraph">
    I am currently pursuing a Master's in Quantitative and Computational Finance at the Georgia Institute of Technology, where I also completed my undergraduate degree 
    in Industrial Engineering with a focus on Analytics, Data Science, and Financial Systems. My academic journey includes coursework in Simulation, 
    Regression, Optimization, Artificial Intelligence, and Machine Learning. 
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="paragraph">
    Prior to attending Georgia Tech, I served as an Intelligence Specialist with the United States Coast Guard, Department of Homeland Security, and 
    the National Security Agency.  
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="paragraph">
    Feel free to click the button below to download a copy of my resume, or check out my github (https://github.com/johnbinek4)  
    </div>
""", unsafe_allow_html=True)

# st.markdown("""
#     <div class="paragraph">
#     Notes for week of 18NOV24: None
#     </div>
# """, unsafe_allow_html=True)

# Centered download button
col1, col2, col3 = st.columns([2, 1, 2])

with col2:
    with open("webpage/JohnBinekWebResume.pdf", "rb") as file:
        st.download_button(
            label="Download Resume",
            data=file,
            file_name="JohnBinekWebResume.pdf",
            mime="application/pdf"
        )