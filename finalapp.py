import streamlit as st
from appv import video_app
from appb import book_app

a = st.sidebar.radio('Choose:',["Videos", "Books"])

st.markdown("<h1 style='color: blue;'>Grow with PRAGATHI</h1>", unsafe_allow_html=True)

if a == 'Videos':
    video_app()
elif a == 'Books':
    book_app()
    