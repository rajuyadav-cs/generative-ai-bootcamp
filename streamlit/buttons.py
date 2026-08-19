import streamlit as st 

name = st.text_input("Your name")
age = st.number_input("Age", min_value=1)

if st.button("Submit"):
    st.success(f"Hello {name}")