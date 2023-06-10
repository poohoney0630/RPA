import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random


# 1. 시험문제 배점 정하기 페이지
# 페이지 설명 부분
st.write("## 1. 시험문제 배점별 문항 수 설정하기📝")
st.write("배점 총 합과 문항수, 배점 리스트를 입력해주시면 가능한 배점별 문항 수가 출력됩니다. ")
st.write("시험문제 낼 때, 협의시간을 줄여보세요!")

# 입력창
N = st.number_input('배점 총 합을 입력해주세요!', min_value=1, max_value=100, value=70, step=1)
n = st.number_input('총 문항 수를 입력해주세요!', min_value=1, max_value=100, value=20, step=1)
scorelist = st.text_input("문항 배점 리스트(2,3,4,5,6과 같이 수와 컴마로만 입력하고 Enter를 눌러주세요. :")

if scorelist !="":
    scorelist = list(map(float, scorelist.split(",")))
else:
    print(":D")

# 변수 설정하기
x_list = [] 
for i in range(1, len(scorelist)+1):
    globals()['x' + str(i)] = None
    x_list.append('x' + str(i))
    
# 함수 정의하기 indef_eq_3, indef_eq_4, indef_eq_5
def indef_eq_3(scorelist, N, n):
    sol_list = []
    for globals()[x_list[-1]] in range(1,n):
        A = np.array([scorelist, np.ones(len(scorelist)).tolist()])
        b = [N-globals()[x_list[-1]]*scorelist[-1], 
            n-globals()[x_list[-1]]]
        sol = np.linalg.solve(A.T[:-1].T, b)
        if np.all(sol > 0):
            sol = np.append(sol, globals()[x_list[-1]])
            sol_list.append(sol)
        else:
            continue
    return pd.DataFrame(sol_list, columns=scorelist).sort_index(axis =1)

def indef_eq_4(scorelist, N, n):
    sol_list = []
    for globals()[x_list[-1]] in range(1,n):
        for globals()[x_list[-2]] in range(1,n):
            A = np.array([scorelist, np.ones(len(scorelist)).tolist()])
            b = [N-globals()[x_list[-1]]*scorelist[-1] 
                -globals()[x_list[-2]]*scorelist[-2], 
                n-globals()[x_list[-1]]
                -globals()[x_list[-2]]]
            sol = np.linalg.solve(A.T[:-2].T, b)
            if np.all(sol > 0):
                sol = np.append(sol, globals()[x_list[-2]])
                sol = np.append(sol, globals()[x_list[-1]])
                sol_list.append(sol)
            else:
                continue
    return pd.DataFrame(sol_list, columns=scorelist).sort_index(axis =1)

def indef_eq_5(scorelist, N, n):
    sol_list = []
    for globals()[x_list[-1]] in range(1,n):
        for globals()[x_list[-2]] in range(1,n):
            for globals()[x_list[-3]] in range(1,n):
                A = np.array([scorelist, np.ones(len(scorelist)).tolist()])
                b = [N-globals()[x_list[-1]]*scorelist[-1] 
                        -globals()[x_list[-2]]*scorelist[-2]
                        -globals()[x_list[-3]]*scorelist[-3], 
                    n-globals()[x_list[-1]]
                    -globals()[x_list[-2]]
                    -globals()[x_list[-3]]]
                sol = np.linalg.solve(A.T[:-3].T, b)
                if np.all(sol > 0):
                    sol = np.append(sol, globals()[x_list[-3]])
                    sol = np.append(sol, globals()[x_list[-2]])
                    sol = np.append(sol, globals()[x_list[-1]])
                    sol_list.append(sol)
                else:
                    continue
                    
    return pd.DataFrame(sol_list, columns=scorelist).sort_index(axis =1)

# scorelist 길이에 따라 함수를 골라 출력하는 함수
def nb_of_item(scorelist, N, n):
    if len(scorelist)==3:
        st.write(indef_eq_3(scorelist, N, n))
    elif len(scorelist)==4:
        st.write(indef_eq_4(scorelist, N, n))
    elif len(scorelist)==5:
        st.write(indef_eq_5(scorelist, N, n))
    else:
        st.write('배점 종류는 3가지, 4가지, 5가지만 가능합니다. ')
#####################################################################
nb_of_item(scorelist, int(N),int(n))
st.write("열 이름(배점)을 클릭하면 오름차순/내림차순으로 정렬됩니다.")
st.write("일반적으로, 난이도 중인 문항 수가 가장 많으므로 난이도 '중'인 배점을 기준으로 정렬하는 것이 좋겠네요!")
