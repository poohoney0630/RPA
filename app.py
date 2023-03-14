import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import time

# 별도 페이지 만들기

# 업무자동화
# 1. 시험문제 배점 설정하기
# 2. 생활기록부 독서 정정 : st.file_uploader

# 확률과 통계
# 1. 뽑기 확률 시뮬레이터
# 2. 데이터 프로파일링 : streamlit_pandas_profiling

# 시작 페이지
def intro():

    st.write("# 😎Welcome to RPA in SCHOOL! 👋")
    st.sidebar.success("Select a demo above.")
    st.write('made by 숩숩')

# 1. 시험문제 배점 정하기 페이지
def scoring_for_exam():
    # 페이지 설명 부분
    st.write("## 1. 시험문제📝 배점별 문항 수 설정하기")
    st.write("배점 총 합과 문항수, 배점 리스트를 입력해주시면 가능한 배점별 문항 수가 출력됩니다. ")
    st.write("시험문제 낼 때, 협의시간을 줄여보세요!")

    # 입력창
    N = st.number_input('배점 총 합', min_value=1, max_value=100, value=70, step=1)
    n = st.number_input('총 문항 수 :', min_value=1, max_value=100, value=20, step=1)
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



def book_recording():
    # 페이지 설명 부분
    st.write("## 2. 학교생활기록부 독서기록📚 중복 찾기")
    st.write("생활기록부 점검시, 학생마다 독서기록이 중복된 경우가 왕왕 있습니다.")
    st.write("예를 들어 한 학생이 2학년 1학기와 1학년 1학기에 같은 책을 기록한 경우죠! ")
    st.write("나이스에서 반별 독서기록파일을 csv파일로 다운받아, 아래에 업로드해주세요. 중복된 항목이 출력됩니다. ")
    uploaded_file = st.file_uploader("Choose a file")
    
    df = pd.DataFrame(pd.read_csv(uploaded_file).values[3:,:6])
    df.columns = ["name","section", "year", "grade","sem","book"]#column 이름 지정
    df = df.dropna(how='all')#모든 칸이 nan인 행 지우기
    df = df.fillna(method='ffill') #행별로 이름 채우기(전 행의 이름과 동일함)
    df.drop(df[df['name'] =='이  름'].index, inplace = True) #페이지 넘어갈 때 있는 열이름 삭제
    original = df.values.tolist() #list로
    pd.options.display.max_colwidth = 100
    st.write(df.head(3))

    # 중복된 부분 찾기 (1) 책이름과 저자명이 완벽히 일치
    for student in df.name.unique():
      #학생별로 도서명 문자열로 담기
      temp = df[df.name==student]
      all_book = temp.book.tolist()
      book_list_incomplete = []
      for book_by_row in all_book :   
        book_list_incomplete = book_list_incomplete+book_by_row.split("), ")

      #print("1. " , book_list_incomplete)

      # 빈 문자열 원소 제거 및 괄호 처리하기
      book_list = []
      for book in book_list_incomplete:
        if len(book)==0:
          continue
        elif book[-1]==")":
          book_list.append(book)
        else:
          book_list.append(book+")")
      #print("2. " , book_list)

      # 중복 횟수 세기
      book_count={}
      lists = book_list
      for i in lists:
          try: book_count[i] += 1
          except: book_count[i]=1
      #print("3. " , book_count)

      # 중복 횟수가 2 이상인 아이템의 key만 담기
      book_duplicated = []
      for k, v in book_count.items():
          if v >= 2: 
              book_duplicated.append(k)
      #print("4. " , book_duplicated)

      # 출력하기
      if len(book_duplicated)>0:
        st.write('\n',student, "학생의 중복된 항목이 있습니다.:")
        for book in book_duplicated:
            st.write(">>",book)
        st.write('>> 다음 영역 중에서 찾아보세요.')
        for i in range(len(book_duplicated)):
          st.write(temp[temp['book'].str.contains(book_duplicated[i][:2])]) 
      else:
        continue


####################################################
page_names_to_funcs = {
    "소개글": intro,
    "1. 시험 문제 배점 정하기": scoring_for_exam, 
    "2. 학교생활기록부 독서기록 중복 찾기": book_recording 
}

demo_name = st.sidebar.selectbox("페이지를 이동해주세요.", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()