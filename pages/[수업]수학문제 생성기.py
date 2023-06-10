import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random
# 페이지 설명 부분

st.write("## 4. 수학 문제 무한 생성기!🖍")
st.write("연습이 필요한 계산 문제 생성하느라 골치아프셨나요? 숫자만 바꿔도 되는 문제라면, 문제를 자동으로 만들고 채점도 자동으로 해보세요!")

# 일차방정식
st.write('### 1. 일차방정식 연습')
st.write('아래의 일차방정식의 해를 구하세요.')
st.write('예를 들어, 2x-1=3인 경우 답안에는 2만 입력하면 됩니다. ')
nums = list(range(1, 11))  # 1부터 10까지의 자연수 리스트 생성
random.shuffle(nums)  # 리스트를 무작위로 섞음
a, b, c = nums[:3]  # 리스트에서 앞에서 네 개를 뽑아서 변수에 할당
equation_str = '## $${}x-{}={}$$'.format(a, b, c)
user_input = st.number_input("아래 방정식에 대한 답을 입력하세요(소수 둘째자리에서 반올림)")
answer = np.round((b+c)/a, 1)   
st.write(equation_str)

if user_input == answer:
    feedback = "정답입니다!🎉 참 잘했어요. 다음 문제를 풀어보세요."
else:
    feedback = "오답입니다. 다시 도전해보세요!💪"
check_answer = st.button('정답 확인하기!')
if check_answer:
    st.write(feedback)
    st.write(f"정답은 {answer}입니다.")
update_equation = st.button('업데이트')
if update_equation:
    random.shuffle(nums)
    a, b, c = nums[:3]
#        equation_str = '## $${}x-{}={}$$'.format(a, b, c)
#        st.write(equation_str)

