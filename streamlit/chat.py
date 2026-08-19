import streamlit as st 

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI ASSISSTANT")    

for message in st.session_state.messages:
    
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask Something...")

if prompt:
    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt 
        }
    )
    with st.chat_message("user"):
        st.write(prompt) 
    
    response = f"You said: {prompt}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)           