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

# 시작 페이지
def intro():

    st.write("# 😎Welcome to RPA in SCHOOL! 👋")
    st.write("업무자동화 페이지에 오신 것을 환영합니다!")

    st.sidebar.success("페이지를 선택해주세요!")

    st.write("### **학교에서 반복적이고 기계적인 일을 적게 할 수는 없을까?**")
    st.write("라는 고민(투덜)으로 시작한 업무자동화 페이지입니다. 학교에서 업무 효율화를 통해 교사의 전문성이 필요한 수업 평가, 기록의 질에 고민할 수 있는 시간을 확보하기 위해서죠! \n학교에서 업무나 수업 중 느끼는 '불편함'이 바로 업무자동화 '아이디어'입니다. ")
    st.write('made by **숩숩** ✉sbhath17@gmail.com')
    st.write("모바일로 들어오셨을 경우 : 왼쪽 상단의 '>' 버튼을 클릭하여 페이지를 이동해주세요.")
    st.write("last updated:",time.strftime('%Y.%m.%d %H:%M:%S'))

# 1. 시험문제 배점 정하기 페이지
def scoring_for_exam():
    # 페이지 설명 부분
    st.write("## 1. 시험문제 배점별 문항 수 설정하기📝")
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

# 2. 독서활동상황 중복기재 찾기 페이지
def book_recording():
    # 페이지 설명 부분
    st.write("## 2. 학교생활기록부 독서기록 중복 찾기📚")
    st.write("생활기록부 점검시, 학생마다 독서기록이 중복된 경우가 왕왕 있습니다. 예를 들어 한 학생이 2학년 1학기와 1학년 1학기에 같은 책을 기록한 경우죠! 나이스에서 **반별 독서기록파일**을 csv파일로 다운받아, 아래에 업로드해주세요. 중복된 항목이 출력됩니다. ")
    

    # 파일 업로드
    uploaded_file = st.file_uploader("파일 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")
    if uploaded_file is None:
        if st.button('샘플 파일 업로드 해보기'):
            #uploaded_file = pd.read_csv('book_recording_sample.csv')
            uploaded_file = pd.read_csv('https://raw.githubusercontent.com/Surihub/RPA/main/book_recording_sample.csv')
            st.write('샘플 파일 업로드 완료!')
            

    try:
        df = pd.DataFrame(uploaded_file.values[3:,:6])
        df.columns = ["name","section", "year", "grade","sem","book"]#column 이름 지정
        df = df.dropna(how='all')#모든 칸이 nan인 행 지우기
        df = df.fillna(method='ffill') #행별로 이름 채우기(전 행의 이름과 동일함)
        df.drop(df[df['name'] =='이  름'].index, inplace = True) #페이지 넘어갈 때 있는 열이름 삭제
        original = df.values.tolist() #list로
        pd.options.display.max_colwidth = 100

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
            for book in book_duplicated:
                st.write('\n',student, "학생의 독서기록 중 **",book,"**이 중복되었습니다. ")
            for i in range(len(book_duplicated)):
              st.write(temp[temp['book'].str.contains(book_duplicated[i][:2])]) 
          else:
            continue
    except:
        print(":D")

def prediction():
    # 10명의 선수와 10번의 게임에 대한 기록을 갖는 데이터 프레임을 생성합니다.
    df = pd.DataFrame(np.random.randint(0, 2, size=(10, 10)),
                    columns=['game_{}'.format(i) for i in range(1, 11)],
                    index=['player_{}'.format(i) for i in range(1, 11)])

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    # 데이터를 불러와서 전처리하는 함수를 정의합니다.
    def load_and_preprocess_data(data_path):
        # 데이터 파일을 불러옵니다.
        df = pd.read_csv(data_path, index_col=0)

        # 데이터를 학습용과 테스트용으로 분리합니다.
        X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :-1], df.iloc[:, -1], test_size=0.2, random_state=42)

        # 로지스틱 회귀 모델을 초기화합니다.
        clf = LogisticRegression()

        # 학습용 데이터로 모델을 학습시킵니다.
        clf.fit(X_train, y_train)
        return clf, X_test, y_test

    # 샘플 데이터 생성
    data = {'player1': [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
            'player2': [0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
            'player3': [1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
            'player4': [0, 1, 0, 0, 1, 1, 0, 1, 1, 1],
            'player5': [0, 1, 1, 1, 0, 0, 1, 1, 0, 0],
            'player6': [1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
            'player7': [0, 0, 1, 1, 0, 0, 1, 1, 1, 1],
            'player8': [0, 1, 0, 1, 1, 1, 0, 0, 1, 1],
            'player9': [1, 1, 1, 0, 0, 1, 1, 0, 0, 0],
            'player10': [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            'win': [1, 1, 0, 1, 0, 1, 1, 0, 0, 0]} # 마지막 열이 승리 여부

    df = pd.DataFrame(data)

    # 데이터를 학습용과 검증용으로 분할
    train, test = train_test_split(df, test_size=0.2)

    # 학습용 데이터를 입력과 타겟으로 나눔
    train_X = train.drop('win', axis=1)
    train_Y = train['win']

    # 모델 생성
    model = RandomForestClassifier()

    # 모델 학습
    model.fit(train_X, train_Y)

    # 검증용 데이터를 이용한 예측 및 정확도 계산
    test_X = test.drop('win', axis=1)
    test_Y = test['win']
    accuracy = model.score(test_X, test_Y)

    # 사용자 입력 받기
    st.title('Winning Probability Prediction')
    st.write('Enter the game results of each player:')

    # 입력 받은 데이터로 예측
    input_data = []
    for i in range(1, 11):
        input_data.append(st.number_input('Player {} win or lose (0 or 1)'.format(i)))
    pred_data = pd.DataFrame([input_data], columns=train_X.columns)
    pred = model.predict(pred_data)[0]

    # 예측 결과 출력
    st.write('Prediction Result:')
    if pred == 1:
        st.write('This team is likely to win with {}% probability.'.format(int(accuracy*100)))
    else:
        st.write('This team is likely to lose with {}% probability.'.format(int((1-accuracy)*100)))

def datavisualization():
    import seaborn as sns
    import matplotlib.pyplot as plt

    titanic = sns.load_dataset("titanic")
    st.write(titanic.head(5))
    fig = plt.figure(figsize=(10, 4))
    sns.histplot(x=titanic['age'])
    st.pyplot(fig)

def group_making():
    st.write("## 3. 학생들의 특성을 바탕으로 조 편성하기🤼‍♂️")
    st.write("수업 등에서 모둠을 구성할 때, 일반적으로 랜덤으로 편성을 많이 합니다. 하지만 가끔 경우에 따라 학생들의 특성에 따라 조를 편성하면 좋은 경우가 있습니다. 예를 들어 모둠별로 문제를 해결해야 하는 수업에서 점수가 낮은 학생들만 모여있다면 원활하게 진행되지 않겠죠? 혹은, 학생들의 특성이 어느정도는 달라야 서로 상호작용을 하며 배우는 것이 더 많을텐데요! 이러한 점을 고려해서 모둠을 편성하는 예시입니다. 완성된 결과를 보고, 꼭 검토 후 사용해주세요!")
    
    # 이름 생성하기
    def generate_names(n):
        first_names = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']
        last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전', '홍', '문', '양']
        names = []
        while len(names) < n:
            first = random.choice(first_names)
            last = random.choice(last_names)
            name = last + first + random.choice(first_names)
            if name not in names:
                names.append(name)
        return names

    # n명을 k개 그룹으로 나눌 때 조별 인원수 리스트
    def divide_n_into_k_parts(n, k):
        quotient = n // k
        remainder = n % k

        sizes = [quotient] * k
        for i in range(remainder):
            sizes[i] += 1

        intervals = []
        start = 0
        for size in sizes:
            end = start + size
            intervals.append(size)
            start = end

        return intervals
    
    # sample data(df) 생성하기
    #np.random.seed(42)
    n_students = 30
    names = generate_names(n_students)
    scores = np.round(np.random.normal(loc=50, scale=18, size=n_students))
    scores = np.clip(scores, 0, 100)
    grades = np.random.choice(['A', 'B', 'C', 'D'], size=n_students, p=[0.3, 0.3, 0.2, 0.2])
    data = {'이름': names, '점수': scores, '특성': grades}
    sample_data = pd.DataFrame(data)
    df = sample_data
    st.write('(파일 업로드 기능 보완 예정)')
    uploaded_file = st.file_uploader("파일 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")

    if st.button('샘플 파일 업로드 해보기'):
        uploaded_file = sample_data
        st.write('샘플 파일 업로드 완료! {}명의 학생입니다. 데이터는 버튼을 누를 때마다 리셋됩니다.  '.format(len(sample_data)))
        st.write(sample_data)
    # 파일 업로드
    # if uploaded_file is None:
    #     if st.button('샘플 파일 업로드 해보기'):
    #         uploaded_file = sample_data
    #         st.write(sample_data)
    #         st.write('샘플 파일 업로드 완료!')
    # try:
    #     df = pd.DataFrame(uploaded_file.values[:,:])
    #     st.write(df)
    # except:
    #     print(":D")
    k = int(st.text_input('모둠 수를 입력하세요:', value = 8)) # 그룹의 개수
    n = len(df)
    nb_of_st_list = divide_n_into_k_parts(n, k)
    if st.button('랜덤 모둠 편성'):
        st.write('랜덤으로 모둠을 편성합니다.')
        n = len(df)
        # 인원수 리스트 생성
        
        # 랜덤 셔플
        sample_random = df.sample(frac = 1).reset_index(drop=True)
        # 그룹 부여
        sample_random['group'] = 0
        # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
        start = 0
        for i, nb in enumerate(nb_of_st_list):
            end = start + nb
            sample_random.loc[start:end-1, 'group'] = i + 1
            start = end


        st.write(sample_random)

    # if st.button('특성 고려해서 편성하기'):
    #     # column 이름들을 버튼으로 만들기
    #     cols = df.columns.tolist()
    #     for col in cols:
    #         if st.button(col):
    #             st.write(df[col])

    #     # 선택된 column들만 출력하기
    #     if not st.button('Show All'):
    #         st.write(df)
    col = st.text_input('기준이 되는 열 이름을 입력해주세요 "점수" 혹은 "특성"을 입력해주세요 : ')
    st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과입니다. 복사하여 스프레드시트에 붙여넣기 해주세요. ')
    if col =='점수': # 수치
        def calculate_team_mean(team): 
            team_mean_list = []
            for i in range(k):
                team_mean = team[i].T[1].mean()
                team_mean_list.append(team_mean)
            return team_mean_list

        data = np.array(df[['이름', '점수']])

        team = []
        # 일단 순서대로 구분
        start = 0
        for nb in nb_of_st_list:
            end = start + nb
            team.append(data[start:end])
            start = end

        # 초기값 설정
        team_mean_list = calculate_team_mean(team).copy()
        range_i = np.max(team_mean_list)-np.min(team_mean_list)
        range_i_new = range_i-1 # 그냥, 초기값 설정. 바로 반복문 안에서 업데이트 할 예정


        for ii in range(10):
            range_i_save = range_i.copy()
            team_save = team.copy()
            team_mean_list_save = team_mean_list.copy()

            min, max = team[0].T[1].mean(), team[0].T[1].mean()
            max_index = np.argmax(team_mean_list)
            min_index = np.argmin(team_mean_list)

            # print(min, min_index, max, max_index)
            #최댓값 최솟값 뽑기 (min, max)
            #그 그룹 추출하기#############################################update
            team_min = team[min_index]
            team_max = team[max_index]
            #print(team_min, team_max)
            # team_min 에서 낮은 사람과 team_max에서 높은 사람 교환
            max_row_idx = np.argmax(team_max[:, 1])
            max_row = team_max[max_row_idx, :]
            min_row_idx = np.argmin(team_min[:, 1])
            min_row = team_min[min_row_idx, :]

            team_max = np.delete(team_max, max_row_idx, axis=0)
            team_max = np.vstack([team_max, min_row])
            team_min = np.delete(team_min, min_row_idx, axis=0)
            team_min = np.vstack([team_min, max_row])
            #print(team_min, team_max)
            team[max_index] = team_max
            team[min_index] = team_min
            #############################################################updated
            team_mean_list_new = calculate_team_mean(team)
            range_i_new = np.max(team_mean_list_new)-np.min(team_mean_list_new)

            st.write("그룹별 평균 점수의 범위가", range_i_save, range_i,"에서", range_i_new, "로 업데이트 되었어요!")        
            if range_i_new > range_i:
                break
            range_i = range_i_new


            #####################range_i_new >= range_i 라면 반복문 break,
        st.write("다음 step에서는 그룹별 평균 점수의 범위가 더 커집니다.... 여기서 중단합니다. ")
        team_df = pd.concat([pd.DataFrame(arr) for arr in team_save], ignore_index=True)
        team_df.columns = ['이름', '점수']
        team_df['group'] = 0
        # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
        start = 0
        for i, nb in enumerate(nb_of_st_list):
            end = start + nb
            team_df.loc[start:end-1, 'group'] = i + 1
            start = end

        st.write(team_df)
        st.write("최종 팀별 평균은 각각 {}입니다. ".format(np.round(team_mean_list_save)))


    elif col =="특성": #범주
        st.write(df[['이름', '특성']])


####################################################
page_names_to_funcs = {
    "소개글": intro,
    "1. 시험 문제 배점 정하기": scoring_for_exam, 
    "2. 학교생활기록부 독서기록 중복 찾기": book_recording,
    "3. 모둠 구성하기": group_making
#    "3. (시험중)승률 예측": prediction,
#    "4. (시험중)Data Visualization": datavisualization
}

demo_name = st.sidebar.selectbox("업무자동화 페이지", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()