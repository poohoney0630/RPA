import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import random
import itertools


# 1. 시험문제 배점 정하기 페이지
# 페이지 설명 부분
st.title("문제 배점별 문항 수 설정하기📝")


col1, col2 = st.columns(2)
with col1:
    st.info('###### 언제 사용하나요?\n배점 총 합과 문항수, 배점 리스트를 입력해주시면 가능한 배점별 문항 수가 출력됩니다. 시험문제 낼 때, 협의시간을 줄여보세요! ')
with col2:
    st.warning('###### 어떻게 해결하나요?\n대입법으로 부정방정식을 해결합니다. ')



N = st.number_input('배점 총 합을 입력해주세요!', min_value=1, max_value=100, value=70, step=1)
n = st.number_input('총 문항 수를 입력해주세요!', min_value=1, max_value=100, value=20, step=1)
scorelist = st.text_input("문항 배점 리스트(2,3,4,5,6과 같이 수와 컴마로만 입력하고 Enter를 눌러주세요. :")

if scorelist != "":
    try:
        scorelist = list(map(float, scorelist.split(",")))
    except ValueError:
        st.write("문항 배점을 올바르게 입력해주세요!")
        scorelist = []
else:
    scorelist = []

if scorelist:
    comb = itertools.product(range(1, n), repeat=len(scorelist))

    # 각 조합에 대해 두 방정식을 만족하는지 확인합니다.
    sol_list = []
    for c in comb:
        if sum(c) == n and sum([v * c[i] for (i, v) in enumerate(scorelist)]) == N:
            sol_list.append(c)
            # st.write(c)
else:
    sol_list = []

if sol_list:
    solution = pd.DataFrame(sol_list)
    solution.columns = scorelist
    st.write(solution)
    st.write("열 이름(배점)을 클릭하면 오름차순/내림차순으로 정렬됩니다.")
    st.write("일반적으로, 난이도 중인 문항 수가 가장 많으므로 난이도 '중'인 배점을 기준으로 정렬하는 것이 좋겠네요!")
    st.write('배점의 종류는 브루트 포스(brute-force search)방법을 사용하므로 배점의 종류가 많아질 경우 오래 걸릴 수 있습니다....')
else:
    st.write("해가 존재하지 않습니다.")
