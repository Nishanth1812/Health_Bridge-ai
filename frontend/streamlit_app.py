import streamlit as st
import os

# Set page configuration once for the entire app
st.set_page_config(
    page_title="Preventive Healthcare Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add app title and description to the sidebar
st.sidebar.title("Preventive Healthcare Assistant")
st.sidebar.info(
    "Navigate through the different sections using the sidebar menu above."
)

# Display custom content on the main page if no other page is selected
# (Note: This content will only show when streamlit_app.py is run directly)
st.title("Welcome to the Preventive Healthcare Assistant")
st.markdown("""
    This application provides personalized preventive healthcare recommendations and information.
    
    ### How to use:
    1. **Chat**: Ask questions about preventive healthcare on the home page
    2. **Upload Documents**: Share medical documents for more personalized recommendations
    3. **View Dashboard**: Check system metrics and performance
    4. **Provide Feedback**: Help us improve by sharing your experience
    
    Use the sidebar to navigate between sections.
""")

# Info about this being an entry point
st.info("This is the main application entry point. The actual chat interface is on the Home page.")

# Create shortcut buttons to main sections
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Go to Chat"):
        st.switch_page("Chat.py")
with col2:
    if st.button("Upload Documents"):
        st.switch_page("Upload.py")

# Create pages directory if it doesn't exist
# This is needed when setting up the app for the first time
os.makedirs("pages", exist_ok=True)