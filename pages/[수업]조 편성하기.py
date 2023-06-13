import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random
from faker import Faker
st.title("학생들의 특성을 바탕으로 조 편성하기🤼‍♂️")
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

fake = Faker('ko_KR')
# n명의 자료 생성하기
def generate_names_faker(n):
    names = []
    for _ in range(n):
        name = fake.name()
        names.append(name)
    return names

# st.write(generate_names(5))
# st.write(generate_names_faker(5))

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

st.write("❗업로드 기능 보완 예정❗")
uploaded_file = st.file_uploader("파일 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")
# 샘플 데이터 생성
n_students = int(st.text_input('샘플 데이터를 생성합니다. 학생 수를 설정해주세요:', value = 30))
names = generate_names_faker(n_students)
scores = np.round(np.random.normal(loc=55, scale=18, size=n_students))
scores = np.clip(scores, 0, 100)
grades = np.random.choice(['A', 'B', 'C', 'D'], size=n_students, p=[0.3, 0.3, 0.2, 0.2])
energy = np.random.choice(['E','I'], size=n_students, p=[0.6, 0.4])
data = {'이름': names, '점수': scores, '특성': grades, '에너지':energy}
sample_data = pd.DataFrame(data)


# if st.button('샘플 파일 적용해보기'):
#     uploaded_file = sample_data
#     st.write('샘플 파일 생성 완료! {}명의 학생입니다. 데이터는 버튼을 누를 때마다 리셋됩니다.  '.format(len(sample_data)))
#     st.write(sample_data)

try:
    # 파일 업로드
    if uploaded_file is None:
        if st.button('샘플 자료 적용해보기'):
            df = sample_data
            st.write('샘플 자료 생성 완료! {}명의 학생입니다. 데이터는 버튼을 누를 때마다 리셋됩니다.  '.format(len(sample_data)))
            st.write(df)
    elif st.button('업로드한 학생 파일 확인하기'):
        uploaded_file = pd.read_csv(uploaded_file, encoding = 'euc-kr')
        # uploaded_file = sample_data
        st.write(uploaded_file)
        df = sample_data
        st.write(df)
        st.write('학생 파일 업로드 완료!')
        
except ValueError:
    st.write("파일을 업로드하거나 샘플 학생 데이터를 생성해보세요.")        
# try:
#     df = pd.DataFrame(uploaded_file.values[:,:])
#     st.write(df)
# except:
#     st.write(":D")

#df = pd.DataFrame(uploaded_file)#.values[:,:])
df = sample_data

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
col = st.text_input('기준이 되는 열 이름을 입력해주세요("점수", "특성", "에너지") : ')
st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')


if col =='점수': # 수치
    def calculate_team_mean(team): 
        team_mean_list = []
        for i in range(k):
            team_mean = team[i].T[1].mean()
            team_mean_list.append(team_mean)
        return team_mean_list

    data = np.array(df.loc[:,['이름', col]])#[['이름', '점수']])

    team = []
    # 일단 순서대로 구분
    start = 0
    for nb in nb_of_st_list:
        end = start + nb
        team.append(data[start:end])
        start = end

    # 초기값 설정
    team_mean_list = calculate_team_mean(team)
    dispersion = np.max(team_mean_list)-np.min(team_mean_list)
    st.write("## 그룹 편성 결과")

    for ii in range(10):
        
        #그 그룹 추출하기#############################################update
        min, max = team[0].T[1].mean(), team[0].T[1].mean()
        max_index = np.argmax(team_mean_list)
        min_index = np.argmin(team_mean_list)

        #최댓값 최솟값 뽑기 (min, max)
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
        dispersion_new = np.max(team_mean_list_new)-np.min(team_mean_list_new)
        
        st.write("그룹별 평균 점수의 범위가", np.round(dispersion, 2),"에서", np.round(dispersion_new, 2), "로 업데이트 되었어요!")        
        if dispersion_new > dispersion:
            break
        dispersion = dispersion_new
        #team = team_new
        team_mean_list = team_mean_list_new


        #####################range_i_new >= range_i 라면 반복문 break,
    st.write("다음 step에서는 그룹별 평균 점수의 범위가 더 커졌으므로 여기서 중단합니다. ")
    team_df = pd.concat([pd.DataFrame(arr) for arr in team], ignore_index=True)
    team_df.columns = ['이름', '점수']
    team_df['group'] = 0
    # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
    start = 0
    for i, nb in enumerate(nb_of_st_list):
        end = start + nb
        team_df.loc[start:end-1, 'group'] = i + 1
        start = end

    st.write(team_df)
    st.write("최종 팀별 평균은 각각 {}입니다. ".format(np.round(team_mean_list)))

elif col =="특성" or "에너지":


    def calculate_team_sum_std(team): 
        team_vec_list = []
        team_vec_std_list = []
        for t in team:
            team_vec = np.sum(t.T[2:2+len(df[col].unique())], axis = 1)
            team_vec_list.append(team_vec)
            team_vec_std_list.append(np.std(team_vec))
        return team_vec_list, team_vec_std_list
    # Define the objective_function
    def objective_function(team):
        team_vec_list, team_vec_std_list = calculate_team_sum_std(team)
        return np.sum(team_vec_std_list)

    # Define the neighborhood_function
    def neighborhood_function(team):
        new_team = team.copy()
        # Implement logic to swap students between teams in the new_team allocation
        return new_team

    # Define the simulated_annealing function
    def simulated_annealing(initial_team):
        current_team = initial_team
        current_energy = objective_function(current_team)

        # Set the initial temperature and other parameters
        temperature = 100.0
        cooling_rate = 0.01
        num_iterations = 1000

        best_team = current_team
        best_energy = current_energy

        for _ in range(num_iterations):
            new_team = neighborhood_function(current_team)
            new_energy = objective_function(new_team)

            if new_energy < current_energy or np.random.rand() < np.exp((current_energy - new_energy) / temperature):
                current_team = new_team
                current_energy = new_energy

            if new_energy < best_energy:
                best_team = new_team
                best_energy = new_energy

            temperature *= 1 - cooling_rate

        return best_team

    # Provide the initial team allocation
    initial_team = []  # Replace with your initial team allocation

    # Train the model using Simulated Annealing
    optimal_team = simulated_annealing(initial_team)


# elif col =="특성" or "에너지": #범주
    def reset_cate(df):

        df = df[['이름', col]]
        one_hot_encoded = pd.get_dummies(df[col], prefix=col)
        # one-hot encoding
        data = np.array(pd.concat([df, one_hot_encoded], axis=1))
        data_df = pd.DataFrame(data)
        data_df.columns = ['이름', col]+list(df[col].unique())
        data_df['group'] = 0
        data_df = data_df.sample(frac = 1).reset_index(drop=True)
        # 조 임의 편성
        team = []
        start = 0
        for nb in nb_of_st_list:
            end = start + nb
            team.append(data[start:end])
            start = end

        start = 0
        for i, nb in enumerate(nb_of_st_list):
            end = start + nb
            data_df.loc[start:end-1, 'group'] = i + 1
            start = end        #

        def calculate_team_sum_std(team): 
            team_vec_list = []
            team_vec_std_list = []
            for t in team:
                team_vec = np.sum(t.T[2:2+len(df[col].unique())], axis = 1)
                team_vec_list.append(team_vec)
                team_vec_std_list.append(np.std(team_vec))
            return team_vec_list, team_vec_std_list

        team_vec_list, team_vec_std_list = calculate_team_sum_std(team)

        st.write("## 모둠별 '불균형도'의 합(The lower, the better):",np.round(np.sum(team_vec_std_list), 2))
        st.write('y값은 낮을수록 학생들이 골고루 있다는 뜻입니다! (그룹 내 학생들의 원핫인코딩 벡터합 원소의 표준편차)')
        st.write('이 결과가 마음에 드실 경우, 아래의 표를 복사하여 스프레드시트에 붙여넣기 해주세요.')
        st.write(data_df)
        st.write('합을 최소화시키는 알고리즘은 곧 업데이트 될 예정입니다.😂')

    if st.button('편성 결과 보기'):
        reset_cate(df)