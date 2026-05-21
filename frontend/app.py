import streamlit as st
import requests

st.title('Claimpilot: Insurance Assistant')

# Document Upload Feature
uploaded_file = st.file_uploader('Upload a receipt, invoice, or PDF report', type=['png', 'jpg', 'jpeg', 'pdf'])
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    # Extract extension from filename
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension in ['png', 'jpg', 'jpeg']:
        st.image(uploaded_file, caption='Preview', width=250)
    elif file_extension == 'pdf':
        st.success('PDF Document loaded')
        
    if st.button('Extract Data'):
        with st.spinner('Analyzing document...'):
            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files={'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            )
            if response.status_code == 200:
                extracted_text = response.json().get('extracted_text', '')
                st.info(extracted_text)
            else:
                st.error("Failed to analyze document")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.header('Human Review Panel')
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "assistant" and "HUMAN REVIEW" in st.session_state.messages[-1]["content"]:
        if st.button('Approve Claim #1', type='primary', use_container_width=True):
            msg = 'Please change the status of claim #1 to Approved'
            st.session_state.messages.append({"role": "user", "content": msg})
            
            with st.spinner("Updating database..."):
                response = requests.post("http://127.0.0.1:8000/chat", json={"message": msg})
                if response.status_code == 200:
                    assistant_response = response.json().get("response", "No response received.")
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.rerun()

        if st.button('Deny Claim #1', use_container_width=True):
            msg = 'Please change the status of claim #1 to Denied'
            st.session_state.messages.append({"role": "user", "content": msg})
            
            with st.spinner("Updating database..."):
                response = requests.post("http://127.0.0.1:8000/chat", json={"message": msg})
                if response.status_code == 200:
                    assistant_response = response.json().get("response", "No response received.")
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.rerun()
    else:
        st.info("No manual reviews pending.")

# React to user input
if prompt := st.chat_input("What is your claim about?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send message to backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"message": prompt}
        )
        
        if response.status_code == 200:
            assistant_response = response.json().get("response", "No response received.")
            with st.chat_message("assistant"):
                st.markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            with st.chat_message("assistant"):
                st.error(f"Backend returned an error ({response.status_code}): {response.text}")
                
    except requests.exceptions.ConnectionError:
        with st.chat_message("assistant"):
            st.error("Connection error: Could not connect to the backend server. Is it running on http://127.0.0.1:8000?")