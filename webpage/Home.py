import streamlit as st

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
    </style>
""", unsafe_allow_html=True)

# Add styling
st.markdown("""
    <style>
    /* Add spacing and styling for content */
    .section-heading {
        color: #1f1f1f;
        font-size: 24px;
        margin-bottom: 15px;
        font-weight: 500;
    }
    /* Remove default streamlit padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 20rem;
        padding-right: 20rem;
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
    /* Download button styling */
    .download-button {
        text-align: center;
        margin: 20px 0;
    }
    .stButton>button {
        background-color: #0066cc;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    </style>

    <div class="nav-links">
        <a href="Finance">Finance</a>
        <a href="Sports">Sports</a>
    </div>
""", unsafe_allow_html=True)

# Create centered container for resume display
st.markdown('<div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">', unsafe_allow_html=True)

# Add title
st.title("John Binek")

# Add download button for resume
with open("webpage/resume.pdf", "rb") as file:
    btn = st.download_button(
        label="Download Resume",
        data=file,
        file_name="JohnBinekQFResume.pdf",
        mime="application/pdf"
    )

# Display PDF
st.markdown("### Resume Preview")
st.markdown(
    """
    <iframe 
        src="webpage/resume.pdf" 
        width="800" 
        height="1000" 
        style="border: none;">
    </iframe>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)