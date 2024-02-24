import streamlit as st
import numpy as np
import pandas as pd
import time


st.markdown("# Main page 🎈")

st.sidebar.markdown("# Main page 🎈")

chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    # columns=['a', 'b', 'c']),
    columns=['lat', 'lon'])

line_chart = st.line_chart(chart_data)

with st.spinner('Loading...'):
  time.sleep(2)
  st.map(chart_data)



st.text_input("Chat Input", key='chat_input', placeholder="Enter a prompt")
if st.checkbox('Show slider'):
  x = st.slider('slider')
  st.write('Temperature:', f'{x}%')

option = st.sidebar.selectbox(
  "which number do you like best?",
  [1, 2, 3, 4, 5] 
)
st.sidebar.file_uploader("Upload your file", key='file')
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)
add_slider

left, right = st.columns(2)
left.text('Hello how are you')
with right:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

