import streamlit as st
import numpy as np
import pandas as pd
import random
from faker import Faker
import matplotlib.pyplot as plt

st.title("특성을 바탕으로 조 편성하기🤼‍♂️")

st.info('###### 언제 사용하나요?\n몇개의 번호 중에서 여러 번호를 추첨할 때! ')
st.warning('###### 어떻게 해결하나요?\n학생 데이터를 업로드하여 특성 고려한 편성')

# seed를 고정시키는 코드
seed = 1234

fake = Faker('ko_KR')
fake.seed_instance(seed)

def generate_names_faker(n):
    return [fake.name() for _ in range(n)]

def divide_n_into_k_parts(n, k):
    quotient = n // k
    remainder = n % k
    return [quotient + (1 if i < remainder else 0) for i in range(k)]

def random_group(df, k):
    sample_random = df.sample(frac=1).reset_index(drop=True)
    group_sizes = divide_n_into_k_parts(len(df), k)
    sample_random['group'] = np.repeat(np.arange(1, k+1), group_sizes)
    return sample_random

def categorical_data_grouping(df, col, k, n_repeat, threshold):
    one_hot_encoded = pd.get_dummies(df[col], prefix=col)
    df_encoded = pd.concat([df, one_hot_encoded], axis=1)
    df_group = random_group(df_encoded, k)
    
    def calculate_group_std_sum_and_std(df):
        return [df[df['group'] == i+1][one_hot_encoded.columns].sum().std() for i in range(k)], df

    st.write('### 초기 랜덤 데이터')
    group_stds, df = calculate_group_std_sum_and_std(df_group)
    show_group_stds = pd.DataFrame(group_stds).T
    show_group_stds.columns = [f"group{i+1}" for i in range(len(group_stds))]
    show_group_stds.index = ['stdev']
    st.write(show_group_stds)


    show_results = []
    iteration = 0

    while iteration < n_repeat:
        group_list = df_group['group'].unique()
        top_indices = show_group_stds.T['stdev'].nlargest(2).index
        g1 = int(top_indices.values[0][-1])
        g2 = int(top_indices.values[1][-1])
        df1 = df_group[df_group['group'] == g1]
        df2 = df_group[df_group['group'] == g2]
        
        p1, p2 = random.choice(df1.index), random.choice(df2.index)
        df_group.at[p1, 'group'], df_group.at[p2, 'group'] = g2, g1

        group_stds, df = calculate_group_std_sum_and_std(df_group)
        show_group_stds = pd.DataFrame(group_stds).T
        show_group_stds.columns = [f"group{i+1}" for i in range(len(group_stds))]
        show_group_stds.index = ['stdev']
        show_result = show_group_stds.T.sum().values[0]
        show_results.append(show_result)
        
        if show_result < threshold:
            break
        
        iteration += 1
    fig = plt.figure(figsize=(5, 3))
    plt.plot([i for i in range(len(show_results))], show_results, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Sum of Standard Deviations')
    plt.title('Sum of Standard Deviations over Iterations')
    st.pyplot(fig)
    # 최종 결과물
    st.write('### 트레이딩 후 조편성 결과')
    st.write(df_group)
    st.write(show_group_stds)
    

def grouping(df, k):
    selected_option = st.radio("옵션 선택", ['랜덤', '범주', '수치'])
    col_list = df.columns.tolist()

    if selected_option == '랜덤':
        st.write(random_group(df, k))
    elif selected_option == '수치':
        st.write('수치형은 아직 준비중입니다.')
    elif selected_option == '범주':
        col = st.selectbox('기준이 되는 열 이름을 선택해주세요', col_list)
        # 루프를 실행할 임계값 설정
        threshold = st.number_input("임계값을 입력해주세요. 이 값보다 작으면 반복을 멈춥니다.", value = 5)
        n_repeat = st.number_input("최대 반복횟수를 설정해주세요", value = 30)
        if st.button('편성하기'):

            categorical_data_grouping(df, col, k, n_repeat, threshold)

# 샘플 데이터 생성


if st.checkbox('샘플 파일 조 편성하기'):
    n_students = int(st.text_input('샘플 데이터를 생성합니다. 학생 수를 설정해주세요:', value='30'))
    names = generate_names_faker(n_students)
    scores = np.clip(np.round(np.random.normal(55, 18, n_students)), 0, 100)
    grades = np.random.choice(['A', 'B', 'C', 'D'], n_students, p=[0.3, 0.3, 0.2, 0.2])
    energy = np.random.choice(['E','I'], n_students, p=[0.5, 0.5])
    sample_data = pd.DataFrame({'이름': names, '점수': scores, '특성': grades, '에너지': energy})
    k = int(st.text_input('모둠 수를 입력하세요:', value='8'))

    with st.spinner('조 편성 중 ...'):
        grouping(sample_data, k)

student_data = st.file_uploader("학생 데이터 csv 파일을 업로드해주세요!", type="csv")

if student_data:
    student_data = pd.read_csv(student_data, encoding='euc-kr')
    st.session_state['student_data'] = student_data
    k = int(st.text_input('모둠 수를 입력하세요:', value='8'))    

if st.checkbox('업로드한 파일 조 편성하기!'):
    
    st.write(st.session_state['student_data'])
    with st.spinner('조 편성 중...'):
        grouping(st.session_state['student_data'], k)
        # try:
        #     # k = int(st.text_input('모둠 수를 입력하세요:', value='8'))
        #     grouping(st.session_state['student_data'], k)
        # except:
        #     st.write("⚠올바른 파일을 업로드하셨는지 확인해주세요!")
