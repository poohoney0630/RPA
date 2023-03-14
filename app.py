import streamlit as st
import pandas as pd
import numpy as np

st.title('업무자동화 in SCHOOL😎')
st.write('made by 숩숩')
st.write("# 1. 시험문제 배점별 문항수 설정하기")
st.write("배점 총 합과 문항수, 배점 리스트를 입력해주시면 가능한 배점별 문항 수가 출력됩니다. ")
st.write("시험문제 낼 때, 협의시간을 줄여보세요!")



N = st.number_input('배점 총 합', min_value=1, max_value=100, value=70, step=1)
n = st.number_input('총 문항 수 :', min_value=1, max_value=100, value=20, step=1)

scorelist = st.text_input("문항 배점 리스트(2,3,4,5,6과 같이 수와 컴마로만 입력해주세요. :")
#st.write(type(scorelist))

if scorelist!="":
  score = list(map(float, scorelist.split(",")))
  st.write(len(score),"가지의 배점을 입력하셨습니다.")
  N = int(N)
  n = int(n)
  case = []
# 배점당 2문제 이상은 있도록 설정(range(2, n-1))
  for s in range(2,n-1):
    for w in range(2,n-1):
      for z in range(2,n-1):
        for y in range(2,n-1):
          for x in range(2,n-1):
            if (x+y+z+w+s == n)&(score[0]*x+score[1]*y+score[2]*z+score[3]*w+score[4]*s== N)&(z>=np.floor(n/5)) : 
              # 배점이 중간인 문항 수가 나머지보다 적지는 않게
              st.write(x,y,z,w,s)
              case.append([x,y,z,w,s])
            else :
              continue

  if len(case)==0:
    st.write('가능한 문항 수가 존재하지 않습니다. 문항 수나 배점 리스트를 다시 설정하세요. ')
  else : 
    st.write('{}가지 모든 경우를 출력하였습니다. '.format(len(case)))


#st.dataframe(pd.DataFrame(case), use_container_width=True)

#sample
# 3.6, 3.8, 4.0, 4.2, 4.4
# 4.1, 4.3, 4.5, 4.7, 4.9
