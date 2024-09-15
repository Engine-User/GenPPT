import streamlit as st
import base64
import requests
import os

# Set page config
st.set_page_config(page_title="GenPPT", layout="wide", page_icon="📊", initial_sidebar_state="collapsed")

# Load custom CSS
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'intro'

# Navigation
def nav_bar():
    col1, col2, col3, col4 = st.columns([1,1,1,3])
    with col1:
        if st.button("GenPPT", key="nav_intro", use_container_width=True):
            st.session_state.current_page = 'intro'
    with col2:
        if st.button("GENERATE", key="nav_generate", use_container_width=True):
            st.session_state.current_page = 'generate'
    with col3:
        if st.button("WHY?", key="nav_about", use_container_width=True):
            st.session_state.current_page = 'about'

# Pages
def intro_page():
    st.markdown('<h1 class="main-heading">Welcome to GenPPT</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="intro-content-3d">
        <div class="intro-content">
            <h2 class="sub-heading">Transform Your Ideas into Stunning Presentations</h2>
            <p>GenPPT harnesses the power of Large Language Models to create professional PowerPoint presentations in seconds. Just enter your thoughts and have your presentation ready on the go.</p>
            <h3>Guidelines for best results:</h3>
            <ol>
                <li>Enter your presentation topic.</li>
                <li>Make sure to be specific and clear, add references if you can.</li>
                <li>Click 'Generate Presentation'.</li>
                <li>Review the generated slides.</li>
                <li>Download your ready-to-use PowerPoint file</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_page():
    st.markdown('<h1 class="generate-heading">Generate Your Presentation</h1>', unsafe_allow_html=True)

    topic = st.text_input("Enter the topic for your presentation:")
    generate_button = st.button("Generate Presentation", key="generate_btn")

    if generate_button and topic:
        with st.spinner("Generating your presentation...This may take a few seconds."):
            try:
                response = requests.post("http://localhost:8000/generate_ppt", json={"text": topic}, timeout=120)
                
                if response.status_code == 200:
                    data = response.json()
                    slide_titles = data["slide_titles"]
                    slide_contents = data["slide_contents"]
                    ppt_path = data["ppt_path"]
                    
                    st.success("Presentation generated successfully!")
                    
                    # Display PPT preview
                    st.subheader("Presentation Preview")
                    for title, content in zip(slide_titles, slide_contents):
                        with st.expander(title):
                            st.markdown(content)
                    
                    # Download button
                    st.markdown(get_ppt_download_link(ppt_path), unsafe_allow_html=True)
                else:
                    st.error(f"An error occurred while generating the presentation. Status code: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend server. Please make sure the FastAPI backend is running.")
                st.info("To start the backend server, run the following command in your terminal:")
                st.code("uvicorn main:app --reload")
            except requests.exceptions.Timeout:
                st.error("The request to generate the presentation timed out. Please try again or try a shorter topic.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

def about_page():
    st.markdown('<h1 class="about-heading">About GenPPT</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-content">
        <div class="engineer-message">
            <p>GenPPT aims to streamline the process by generating PowerPoint presentations from scratch.</p>
            <p>Instead of spending hours building slides, use this tool to brainstorm and organize your ideas efficiently.</p>
            <p>You can either copy the generated content into your file for further editing or download the complete PPT to customize it as needed.</p>
            <p>Easy!\n\n
            
            ggengineerco@gmail.com
            
    </div>
   
    """, unsafe_allow_html=True)

def get_ppt_download_link(ppt_path):
    with open(ppt_path, "rb") as file:
        ppt_contents = file.read()
    b64_ppt = base64.b64encode(ppt_contents).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64_ppt}" download="{os.path.basename(ppt_path)}" class="download-btn">Download PowerPoint</a>'

def main():
    nav_bar()
    
    if st.session_state.current_page == 'intro':
        intro_page()
    elif st.session_state.current_page == 'generate':
        generate_page()
    elif st.session_state.current_page == 'about':
        about_page()

if __name__ == "__main__":
    main()