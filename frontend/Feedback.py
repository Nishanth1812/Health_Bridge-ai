
import streamlit as st

import streamlit as st
import requests

# Set consistent backend URL from secrets
backend_url = st.secrets.get("BACKEND_URL", "http://localhost:5000")

st.title("Provide Feedback")

# Create form
with st.form("feedback_form"):
    query = st.text_input("Original question")
    answer = st.text_area("Assistant answer")
    rating = st.slider("Rating", 1, 5, 3)
    comments = st.text_area("Additional comments")
    
    # Submit button
    submitted = st.form_submit_button("Submit Feedback")
    
    if submitted:
        # Validate form fields
        if not query:
            st.error("Please enter your original question.")
        elif not answer:
            st.error("Please enter the assistant's answer.")
        else:
            # Prepare payload
            payload = {
                "query": query,
                "answer": answer,
                "rating": rating,
                "comments": comments
            }
            
            # Send feedback to backend
            try:
                with st.spinner("Submitting feedback..."):
                    res = requests.post(f"{backend_url}/feedback/", json=payload)
                    
                if res.status_code == 200:
                    st.success("Feedback sent. Thank you!")
                    # Optional: Clear form fields
                    st.session_state.query = ""
                    st.session_state.answer = ""
                    st.session_state.rating = 3
                    st.session_state.comments = ""
                else:
                    st.error(f"Failed to submit feedback. Status code: {res.status_code}")
                    st.text(f"Error details: {res.text}")
            except Exception as e:
                st.error(f"Error submitting feedback: {e}")

# Display recent feedback summary
st.header("Feedback Summary")
st.info("This section will show aggregated feedback metrics once the backend endpoint is fully implemented.")

# Placeholder for feedback metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Rating", "4.3/5")
with col2:  
    st.metric("Total Feedback Count", "283")
with col3:
    st.metric("Top Area for Improvement", "Response Speed")
