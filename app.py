import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random

# 별도 페이지 만들기

# 업무자동화
# 1. 시험문제 배점 설정하기
# 2. 생활기록부 독서 정정 : st.file_uploader
# 3. 조 편성하기 : 학생들 피쳐(설문지로 받은)에 따라 k개의 그룹을 만들 때, k개의 비슷한 그룹으로 분류 후 그 안에서 한명씩 추출하기

# 확률과 통계
# 1. 뽑기 확률 시뮬레이터
# 2. 데이터 프로파일링 : streamlit_pandas_profiling

st.write("# 😎Welcome to RPA in SCHOOL! 👋")
st.write("업무자동화 페이지에 오신 것을 환영합니다!")
st.write("왼쪽 사이드바의 기능들을 살펴보세요!")

st.markdown("----")
st.write('made by **숩숩** ✉ sbhath17@gmail.com ✉ ')
st.write('피드백 환영합니다🤩 > [피드백 하러 가기](https://forms.gle/nytXFQiRriwRgkKy7)')
# st.write("updated🕑 :",time.strftime('%Y.%m.%d %H:%M:%S'))
st.write("version_2.0, updated 2023.9.12")
