import streamlit as st


st.set_page_config(page_title="My first streamlit app")


st.header("New app")

st.sidebar.header("User Input")

username = st.sidebar.text_input("Enter Your Name")

st.markdown("# hello {}".format(username))


