import streamlit as st

myfirstlist = [1,2,3,4,5]

st.title('업무자동화 in SCHOOL😎')
st.write('made by 숩숩')


import pandas as pd

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)

st.dataframe(df, use_container_width=True)

response = st.text_input("하고싶은 말을 입력해주세요.")
st.write(response)
st.write('반가워요!')