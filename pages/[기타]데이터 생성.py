import streamlit as st
import pandas as pd
import numpy as np

st.title("📊데이터 생성하기")
col1, col2 = st.columns(2)
with col1:
    st.info('###### 언제 사용하나요?\n피벗테이블을 원시자료로 녹일 때!')
with col2:
    st.warning('###### 어떻게 해결하나요?\npd.melt기능과 유사합니다. ')


st.write("### 범주형 데이터")
st.write("변수명과 빈도수를 입력해주세요.")

# 단변량
var_name = st.text_input("변수명을 입력해주세요. (예:학교급)")
val_list = st.text_input("변수의 값을 나열해주세요. (예:초,중,고)")
val_list = list(map(str, val_list.split(",")))
val_count_list = []
for val in val_list:
    val_count = st.number_input(f"{val}의 빈도수")
    val_count_list.append(val_count)

data = []
for val, val_count in zip(val_list, val_count_list):
    for i in range(int(val_count)):
        data.append(val)
df = pd.DataFrame(data)
st.write(df)

# 다변량 케이스
# num_variables = int(st.text_input("다변량 변수 수를 입력하세요:", value='2'))
# multivariate_data = []

# for _ in range(num_variables):
#     var_name = st.text_input("변수명을 입력해주세요.")
#     val_list = st.text_input("변수의 값을 나열해주세요.")
#     val_list = list(map(str, val_list.split(",")))
#     val_count_list = []
#     for val in val_list:
#         val_count = st.number_input("다변량 빈도수")
#         val_count_list.append(val_count)

#     data = []
#     for val, val_count in zip(val_list, val_count_list):
#         for i in range(int(val_count)):
#             data.append(val)
    
#     multivariate_data.append(data)

# df_multivariate = pd.DataFrame(multivariate_data).T
# df_multivariate.columns = [f"변수{i+1}" for i in range(num_variables)]
# st.write("다변량 데이터프레임:")
# st.write(df_multivariate)