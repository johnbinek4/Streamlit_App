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
        .stButton > button {
            margin: 0 auto;
            display: block;
            background-color: #0066cc;
            color: white;
            padding: 12px 30px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            margin-top: 40px;
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
        <a href="Sports">Sports</a>
    </div>
""", unsafe_allow_html=True)

# Main content
st.markdown("""
    <div class="paragraph">
    Welcome! I'm John Binek, a Master's candidate in Quantitative and Computational Finance at Georgia Tech. 
    My academic journey combines rigorous quantitative analysis with practical financial applications, 
    preparing me for the dynamic world of quantitative trading and financial engineering.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="paragraph">
    With a background in Industrial Engineering and experience in the United States Coast Guard, 
    I bring a unique perspective to financial analysis. My military service enhanced my leadership abilities 
    and analytical skills, particularly in intelligence operations and tactical planning.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="paragraph">
    My current focus lies in derivatives pricing, algorithmic trading, and machine learning applications 
    in finance. I'm particularly interested in market making strategies and volatility trading, 
    combining theoretical knowledge with practical implementation.
    </div>
""", unsafe_allow_html=True)

# Resume download button
with open("webpage/JohnBinekQFResume.pdf", "rb") as file:
    btn = st.download_button(
        label="Download Resume",
        data=file,
        file_name="JohnBinekQFResume.pdf",
        mime="application/pdf"
    )