import streamlit as st 

col1 , col2 = st.columns(spec= 2, gap="xlarge" )

with col1:
    st.write("Left")
with col2:
    st.write("Right")    