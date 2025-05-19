import streamlit as st
import requests

# Set consistent backend URL from secrets
backend_url = st.secrets.get("BACKEND_URL", "http://localhost:5000")

st.title("Chat with the Preventive Healthcare Assistant")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Display chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Chat input
user_input = st.chat_input("Ask me about preventive screenings, vaccinations, ...")
if user_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    st.chat_message("user").write(user_input)
    
    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    f"{backend_url}/chat/", 
                    json={"query": user_input}, 
                    timeout=60
                )
                
                if resp.status_code == 200:
                    try:
                        answer = resp.json().get("answer", "Sorry, something went wrong.")
                    except Exception as e:
                        st.error(f"Error parsing JSON: {e}")
                        answer = "Sorry, couldn't parse the server response."
                else:
                    st.error(f"Server returned status code: {resp.status_code}")
                    answer = f"Sorry, server error occurred (Status: {resp.status_code})."
                    
                # Write the answer
                st.write(answer)
                
                # Add assistant message to history
                st.session_state.history.append({"role": "assistant", "content": answer})
                
            except requests.exceptions.Timeout:
                st.error("Request timed out. The server took too long to respond.")
            except requests.exceptions.ConnectionError:
                st.error("Connection error. Please check if the backend server is running.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
