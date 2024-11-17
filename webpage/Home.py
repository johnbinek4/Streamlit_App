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
        /* Adjust padding to ensure navigation is visible */
        .block-container {
            padding: 3rem 1rem 1rem 1rem !important;
        }
        div[data-testid="stToolbar"] {
            visibility: hidden;
        }
        /* Navigation styling */
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
        /* Content styling */
        .content-section {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
            line-height: 1.6;
        }
        .paragraph {
            margin-bottom: 30px;
            font-size: 18px;
            color: #333;
        }
        /* Button styling */
        .stButton>button {
            background-color: #0066cc;
            color: white;
            padding: 10px 25px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            margin-top: 30px;
        }
        .stButton>button:hover {
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

# Content sections
st.markdown("""
    <div class="content-section">
        <div class="paragraph">
        Welcome! I'm John Binek, a Master's candidate in Quantitative and Computational Finance at Georgia Tech. 
        My academic journey combines rigorous quantitative analysis with practical financial applications, 
        preparing me for the dynamic world of quantitative trading and financial engineering.
        </div>
        
        <div class="paragraph">
        With a background in Industrial Engineering and experience in the United States Coast Guard, 
        I bring a unique perspective to financial analysis. My military service enhanced my leadership abilities 
        and analytical skills, particularly in intelligence operations and tactical planning.
        </div>
        
        <div class="paragraph">
        My current focus lies in derivatives pricing, algorithmic trading, and machine learning applications 
        in finance. I'm particularly interested in market making strategies and volatility trading, 
        combining theoretical knowledge with practical implementation.
        </div>
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