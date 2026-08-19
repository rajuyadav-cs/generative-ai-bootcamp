import streamlit as st 

name = st.text_input("What's your name: ")
if name:
    st.write(f"Hii! {name}, Welcome to Snezhnaya")
    

age = st.text_input("What's your age: ")

if age:
    age = int(age)

    if 0 < age < 18:
        st.write("You are not an adult!")
    elif age >= 18:
        st.write("You are an adult now!")   