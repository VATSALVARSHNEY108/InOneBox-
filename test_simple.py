import streamlit as st

st.set_page_config(
    page_title="Test App",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Test App")
st.write("This is a simple test to see if Streamlit is working")

if st.button("Test Button"):
    st.success("Button works!")