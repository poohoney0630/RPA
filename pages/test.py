
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import pandas as pd
import numpy as np

import streamlit as st
from streamlit_chat import message



y = "정답입*니다! 학생님은 문제를 잘 읽고 문제* 상황에 따라 식을 세웠습니다. 일차방정식을 정확하게 풀어 동아리원의 수를 구하고cc 이를 바탕으로 배구공의 가격도 잘 구하셨습니다. 그리고 2500원씩 걷었을 때 부족한 금액을 정확히 계산하셨습니다. 아주 잘 풀었습니다! 다른 평가요소들도 확인하시고cc 자세한 풀이와 함께 문제를 한 번 더 풀어보세요. 만약 도움이 필요하다면 언제든지 물어보세요!"


message("무엇을 도와드릴까요?") 
message(y, is_user=True)  # align's the message to the right





def clear_submit():
    st.session_state["submit"] = False
query = st.text_area("Ask a question about the document", on_change=clear_submit)

st.warning(y)
st.info(y)
st.text_area(y)


import textwrap

long_sentence = "이 문장은 매우 길고 연결된 문장입니다. 한 화면에 표시하기 위해 일정 길이로 나누어야 합니다."

# 문자열을 일정 길이로 나누고, 각 줄을 리스트로 저장
wrapped_lines = textwrap.wrap(long_sentence, width=40)

# 나누어진 줄을 연결하여 하나의 문자열로 만듦
wrapped_sentence = "\n".join(wrapped_lines)

import streamlit as st



import re

x = "3*x = 4*x"
y = "정답입*니다! 학생님은 문제를 잘 읽고 문제* 상황에 따라 식을 세웠습니다. 일차방정식을 정확하게 풀어 동아리원의 수를 구하고cc 이를 바탕으로 배구공의 가격도 잘 구하셨습니다."
# 마크다운 표기 해제를 위해 특수문자를 이스케이프 처리
def code_print(x):
    return re.sub(r"([_*])", r"\\\1", x)

# 스타일이 있는 박스 생성
st.info(code_print("👨‍🎓  "+x))
st.warning(code_print("💬  "+y))
