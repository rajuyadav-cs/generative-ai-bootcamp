import streamlit as st 

st.title("Table Calculator")

if "count" not in st.session_state:
    
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

if st.button("Decrement"):
    st.session_state.count -= 1

st.header("Counter")
st.write(st.session_state.count) 

if "messages" not in st.session_state:
    
    st.session_state.messages = []

number = st.number_input("Enter your table number")
if st.button("Calculate"):
    st.session_state.messages.append(f"{number} * {st.session_state.count} = {number*st.session_state.count}")
st.write(st.session_state.messages)                   