import streamlit as st 

st.sidebar.title("Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2)