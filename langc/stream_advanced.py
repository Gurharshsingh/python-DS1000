import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Advanced Streamlit App", layout="wide")

# ==========================================
# 1. Navigation on Sidebar with Options Menu
# ==========================================
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",  
        options=["Home", "HTML & CSS", "Session State"],  
        icons=["house", "code-slash", "arrow-repeat"],  
        menu_icon="cast" 
    )

# ==========================================
# Page Content based on Selection
# ==========================================
if selected == "Home":
    st.title("Welcome to the Advanced Topics App!🚗")
    st.write("Use the sidebar menu to navigate through different Streamlit topics.")
    st.info("Topics covered: Sidebar Option Menu, HTML/CSS integration, and Session State.")

elif selected == "HTML & CSS":
    st.title("Adding Custom HTML and CSS")
    
    # 2. Injecting custom CSS using st.markdown with unsafe_allow_html=True
    st.markdown("""
        <style>
        .custom-title {
            font-size: 40px;
            color: #FF4B4B;
            text-align: center;
            font-family: 'Helvetica Neue', sans-serif;
            background-color: #262730;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }


        .custom-titlee {
            font-size: 40px;
            color: #F17925;
            text-align: center;
            font-family: 'Times New Roman', serif;
            background-color: #F8C792;
            padding: 0px;
            border-radius: 50px;
            margin-bottom: 20px;
        }


        .highlight {
            color: #00C2A8;
            font-weight: bold;
            font-size: 24px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 3. Using the custom CSS classes in HTML
    st.markdown('<div class="custom-title">This is a custom HTML Title! ✨</div>', unsafe_allow_html=True)
    st.markdown('<p class="highlight">This text is styled using custom CSS injected into Streamlit.</p>', unsafe_allow_html=True)
    st.markdown('<div class="custom-titlee">This is a custom HTML Title! ✨</div>', unsafe_allow_html=True)

    st.write("---")
    st.write("By passing `unsafe_allow_html=True` to `st.markdown()`, you can write raw HTML and CSS to customize your app's UI beyond the default Streamlit components.")

elif selected == "Session State":
    st.title("Understanding Session State 🔄")
    st.write("Session state allows you to save variables across reruns of your Streamlit app.")
    st.markdown('<div class="custom-titlee">This is a custom HTML Title! ✨</div>', unsafe_allow_html=True)
    # 4. Initialize session state variables
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    col1, col2 = st.columns(2)
    
    with col1:
        # Button to increment the counter
        if st.button("➕ Increment Counter"):
            st.session_state.counter += 1
            
    with col2:
        # Button to reset the counter
        if st.button("🔄 Reset Counter"):
            st.session_state.counter = 0

    st.markdown(f"### Current Counter Value: `{st.session_state.counter}`")
    
    st.info("""
    **Try this out:**
    1. Click 'Increment Counter' a few times.
    2. Switch to the 'Home' tab using the sidebar.
    3. Come back to the 'Session State' tab. 
    4. Notice how the counter value is preserved! Standard Python variables would reset to 0 every time the app reruns.
    """)
