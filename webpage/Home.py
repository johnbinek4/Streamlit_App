import streamlit as st
import base64

# Set the page title and layout
st.set_page_config(page_title="Home Page", layout="wide", initial_sidebar_state="collapsed")

# Hide the sidebar completely
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
        /* Center the PDF viewer */
        iframe {
            display: block;
            margin: 0 auto;
        }
        /* Remove default streamlit padding */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        /* Navigation styling */
        .nav-links {
            display: flex;
            justify-content: center;
            padding: 20px;
            background-color: #f8f9fa;
            margin-bottom: 30px;
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
    </style>

    <div class="nav-links">
        <a href="Finance">Finance</a>
        <a href="Sports">Sports</a>
    </div>
""", unsafe_allow_html=True)

# Display PDF content
try:
    with open("webpage/JohnBinekQFResume.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
except Exception as e:
    st.error("Error displaying PDF content")
    st.error(f"Error details: {str(e)}")