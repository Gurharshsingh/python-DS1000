import streamlit as st


st.set_page_config(page_title="My first streamlit app",layout='wide')

st.title("New APP")

st.sidebar.title("APP")







st.header("Hello everyone")
st.sidebar.header("Welcome to my app")

st.write("How are you")

st.markdown("# Krish")

st.markdown("## Krish")

st.markdown("### Krish")



# name = st.sidebar.text_input("Enter your name: ")


# st.write("Hello, My name is ",name)



col1 ,col2,col3 = st.columns([1,3,1])


with col1:
    st.header("Hello everyone")

    st.write("How are you")

    st.markdown("# Krish")

    st.markdown("## Krish")

    st.markdown("### Krish")

    

with col2:
    

    st.header("Hello everyone")

    st.write("How are you")

    st.markdown("# Krish")

    st.markdown("## Krish")

    st.markdown("### Krish")

with col3:
    st.image('cyberpunk_city.png')



name  = st.text_input("Enter your name:")
st.write("Hello, My name is ",name)


# # name = st.sidebar.text_input("Enter your name:")
# # st.sidebar.write("Hello, My name is ",name)