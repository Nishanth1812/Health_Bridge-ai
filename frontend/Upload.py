import streamlit as st
import requests

# Set consistent backend URL from secrets
backend_url = st.secrets.get("BACKEND_URL", "http://localhost:5000")

st.title("Upload Medical Documents")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx"])

if uploaded_file:
    st.write("File uploaded:", uploaded_file.name)
    
    # Display file details
    file_details = {
        "Filename": uploaded_file.name,
        "File type": uploaded_file.type,
        "File size": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    st.json(file_details)
    
    # Option to process the file
    if st.button("Process Document"):
        with st.spinner("Processing document..."):
            try:
                # Prepare the file for upload
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Send the file to the backend
                response = requests.post(
                    f"{backend_url}/documents/upload",
                    files=files
                )
                
                if response.status_code == 200:
                    st.success("Document processed successfully!")
                    # Display any information returned by the API
                    result = response.json()
                    st.json(result)
                else:
                    st.error(f"Failed to process document. Status code: {response.status_code}")
                    st.text(f"Response: {response.text}")
            except Exception as e:
                st.error(f"Error processing document: {e}")
    
    st.divider()
    
    # Fallback for when API is not available
    st.info("If the backend API is not available, you can view a preview of the document below.")
    
    if uploaded_file.type == "text/plain":
        # Display text content for TXT files
        stringio = uploaded_file.getvalue().decode("utf-8")
        st.text_area("Document Content", stringio, height=300)
    elif uploaded_file.type == "application/pdf":
        # Display PDF
        st.write("PDF Preview:")
        st.warning("PDF preview not available in this demo. The file would be processed by the backend.")
    else:  
        st.write("File preview not available for this file type.")
