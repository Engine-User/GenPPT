import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        color: #FF0000;
        background-color: #1E1E1E;
    }

    .stButton > button {
        color: #FF0000;
        background-color: #2E2E2E;
        border: 2px solid #FF0000;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #FF0000;
        color: #1E1E1E;
    }

    .download-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #FF0000;
        color: #1E1E1E;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .download-btn:hover {
        background-color: #CC0000;
    }

    .stTextInput > div > div > input {
        color: #FF0000;
        background-color: #2E2E2E;
        border: 2px solid #FF0000;
    }

    h1, h2, h3 {
        color: #FF0000;
    }

    .stSpinner > div > div {
        border-top-color: #FF0000 !important;
    }
    </style>
    """, unsafe_allow_html=True)