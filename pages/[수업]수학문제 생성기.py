import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random
# 페이지 설명 부분

st.title("수학 문제 무한 생성기!🖍")
st.write("### 🤯 언제 사용하나요?")
st.write("연습이 필요한 계산 문제가 항상 부족하다구요? 문제 찾기 귀찮다구요?숫자만 바꿔도 되는 문제라면, 문제를 자동으로 만들고 채점도 자동으로 해보세요!")
st.write("### 💡 계수가 다른 일차방정식 문제 무한 생성")

st.write('아래의 일차방정식의 해를 구하세요.')
st.write('예를 들어, 2x-1=3인 경우 답안에는 2만 입력하면 됩니다. ')

# Initialize equation numbers and index
if "equation_nums" not in st.session_state:
    st.session_state.equation_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Example equation numbers

if "equation_index" not in st.session_state:
    st.session_state.equation_index = 0

equation_nums = st.session_state.equation_nums
equation_index = st.session_state.equation_index

# Retrieve equation numbers based on index
a, b, c = equation_nums[equation_index * 3: equation_index * 3 + 3]
equation_str = '## $${}x-{}={}$$'.format(a, b, c)

# User input and answer
user_input = st.number_input("아래 방정식에 대한 답을 입력하세요(소수 둘째자리에서 반올림)")
answer = np.round((b + c) / a, 1)
st.write(equation_str)

# Checking the answer
if st.button('정답 확인하기!'):
    if user_input == answer:
        st.write('## 🎉정답입니다! ')
        st.write("참 잘했어요. 다음 문제를 해결해보세요.")
    else:
        st.write('## 😓오답입니다! ')
        st.write("다시 한 번 시도해보세요!💪")
    st.write(f"정답은 {answer} 입니다.")

# Update button
if st.button('다음 문제 풀기'):
    equation_index += 1
    if equation_index * 3 + 3 > len(equation_nums):
        random.shuffle(equation_nums)
        equation_index = 0
    st.session_state.equation_index = equation_index
