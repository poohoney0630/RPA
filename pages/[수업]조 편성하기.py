import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
import random
from faker import Faker

st.title("특성을 바탕으로 조 편성하기🤼‍♂️")

st.info('###### 언제 사용하나요?\n몇개의 번호 중에서 여러 번호를 추첨할 때! ')
st.warning('###### 어떻게 해결하나요?\n학생 데이터를 업로드하여 특성 고려한 편성')# seed를 고정시키는 코드
seed = 1234

fake = Faker('ko_KR')
fake.seed_instance(seed)  # faker의 난수를 고정합니다.

# n명의 자료 생성하기
def generate_names_faker(n):
    names = []
    for _ in range(n):
        name = fake.name()
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



def random_group(df, k):
    n = len(df)
    # 인원수 리스트 생성
    
    # 랜덤 셔플
    sample_random = df.sample(frac=1).reset_index(drop=True)
    # 그룹 부여
    sample_random['group'] = 0
    # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
    start = 0
    nb_of_st_list = divide_n_into_k_parts(n, k)

    for i, nb in enumerate(nb_of_st_list):
        end = start + nb
        sample_random.loc[start:end-1, 'group'] = i + 1
        start = end
    return sample_random



def grouping(df, k):
    # 라디오 버튼 선택에 따른 코드 실행
    selected_option = st.radio("옵션 선택", ['랜덤', '범주'])

    if selected_option == '랜덤':
        if st.button('편성하기'):
            st.write('랜덤으로 모둠을 편성합니다.')

            n = len(df)
            # 인원수 리스트 생성
            
            # 랜덤 셔플
            sample_random = df.sample(frac=1).reset_index(drop=True)
            # 그룹 부여
            sample_random['group'] = 0
            # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
            start = 0
            nb_of_st_list = divide_n_into_k_parts(n, k)

            for i, nb in enumerate(nb_of_st_list):
                end = start + nb
                sample_random.loc[start:end-1, 'group'] = i + 1
                start = end
            st.write(sample_random)

    elif selected_option == '수치':
        col = st.text_input('기준이 되는 열 이름을 입력해주세요("점수"):', value='점수')
        st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')
        if st.button('편성하기'):
            # 수치 편성 코드
            # ...
            st.write('hello numerical')

    elif selected_option == '범주':
        col = st.selectbox('기준이 되는 열 이름을 선택해주세요', ['특성', '에너지'])
        st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')
        if st.button('편성하기'):
            # 범주 편성 코드
            epsilon_sum = float(st.text_input('그룹별 표준편차의 합의 임계값을 선택해주세요. ', value = 2.0))
            epsilon_std = float(st.text_input('그룹별 표준편차의 표준편차의 임계값을 선택해주세요. ', value = 0.10))
            categorical_data_grouping(df, col, epsilon_sum, epsilon_std)
            # st.write('hello categorical')
    #return sample_random


def categorical_data_grouping(df, col, epsilon_sum, epsilon_std):
    def calculate_group_std_sum_and_std():
        df_group = random_group(df_encoded, k)
        group_stds = []
        for i in range(k):
            group_data = df_group[df_group['group'] == i+1][categories]  # 해당 그룹의 데이터 선택
            group_std = group_data.sum().std()  # 그룹의 표준편차 계산
            group_stds.append(group_std)
        return np.sum(group_stds), np.std(group_stds), df_group
    # df = sample_data
    # col = '특성'

    # 'col' 열의 각 값에 대해 원-핫 인코딩을 수행하고, 열 이름 앞에 'col'을 붙이기
    one_hot_encoded = pd.get_dummies(df[col], prefix=col)

    # 원-핫 인코딩된 데이터 프레임의 모든 열 이름을 'categories' 변수에 저장
    categories = one_hot_encoded.columns

    # 원래의 데이터 프레임 'df'와 원-핫 인코딩된 데이터 프레임을 합침
    df_encoded = pd.concat([df, one_hot_encoded], axis=1)

    # 'random_group' 함수를 사용하여 'df_encoded' 데이터 프레임을 'k' 개의 그룹으로 무작위 분할
    df_group = random_group(df_encoded, k)


    previous_group_std_sum = float('inf')
    previous_group_std_std = float('inf')
    group_std_sum, group_std_std, df_group = calculate_group_std_sum_and_std()

    while group_std_sum > epsilon_sum or group_std_std > epsilon_std:  # 수정된 조건문
        if (group_std_sum < previous_group_std_sum) and (group_std_std < previous_group_std_std):
            st.write(f"그룹별 표준편차 합: {np.round(group_std_sum,2)}, 그룹별 표준편차의 표준편차: {np.round(group_std_std, 2)}")

        previous_group_std_sum = group_std_sum
        previous_group_std_std = group_std_std
        group_std_sum, group_std_std, df_group = calculate_group_std_sum_and_std()
        
    st.write('최종 그룹별 표준편차 합:', group_std_sum)
    st.write('최종 그룹별 표준편차의 표준편차:', group_std_std)
    st.write(df_group)

    result = []
    for i in range(k):
        result.append(df_group[df_group['group'] == i+1][categories].sum())
        group_mean = df_group[df_group['group'] == i+1][categories].sum().mean()
        group_std = df_group[df_group['group'] == i+1][categories].sum().std()
        # st.write('group', i+1, '의 범주별 인원 수', group_std)
    result= pd.DataFrame(result)
    result['group']=range(1, 1+k)
    st.write(result)





sample_checked = st.checkbox('샘플 파일 조 편성하기')
# 샘플 데이터 생성
n_students = int(st.text_input('샘플 데이터를 생성합니다. 학생 수를 설정해주세요:', value = 30))
names = generate_names_faker(n_students)
scores = np.round(np.random.normal(loc=55, scale=18, size=n_students))
scores = np.clip(scores, 0, 100)
grades = np.random.choice(['A', 'B', 'C', 'D'], size=n_students, p=[0.3, 0.3, 0.2, 0.2])
energy = np.random.choice(['E','I'], size=n_students, p=[0.6, 0.4])
data = {'이름': names, '점수': scores, '특성': grades, '에너지': energy}
sample_data = pd.DataFrame(data)

if 'student_data' not in st.session_state:
    st.session_state['student_data'] = ''

if sample_checked:
    with st.spinner('조 편성 중 ...'):
        k = int(st.text_input('모둠 수를 입력하세요:', value=8)) # 그룹의 개수
        grouping(sample_data, k)



student_data = st.file_uploader("학생 데이터 csv 파일을 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")

if student_data:
    student_data = pd.read_csv(student_data, encoding = 'utf-8')
    st.session_state['student_data'] = student_data
    
upload_checked = st.checkbox('업로드한 파일 조 편성하기!')
if upload_checked:
    st.write(student_data.head(5))
    with st.spinner('조 편성 중...'):
        try:
            k = int(st.text_input('모둠 수를 입력하세요:', value=8)) # 그룹의 개수
            grouping(student_data, k)
        except:
            st.write("⚠올바른 파일을 업로드하셨는지 확인해주세요!")

# df = sample_data
# col = '특성'

# one_hot_encoded = pd.get_dummies(df[col], prefix=col)
# categories = one_hot_encoded.columns

# df_encoded = pd.concat([df, one_hot_encoded], axis=1)
# df_group = random_group(df_encoded, k)


# def calculate_group_std_sum_and_std():
#     df_group = random_group(df_encoded, k)
#     group_stds = []
#     for i in range(k):
#         group_data = df_group[df_group['group'] == i+1][categories]  # 해당 그룹의 데이터 선택
#         group_std = group_data.sum().std()  # 그룹의 표준편차 계산
#         group_stds.append(group_std)
#     return np.sum(group_stds), np.std(group_stds), df_group

# previous_group_std_sum = float('inf')
# previous_group_std_std = float('inf')
# group_std_sum, group_std_std, df_group = calculate_group_std_sum_and_std()

# while group_std_sum > 6.0 or group_std_std > 2.0:  # 수정된 조건문
#     if group_std_sum < previous_group_std_sum and group_std_std < previous_group_std_std:
#         st.write(f"그룹별 표준편차 합: {np.round(group_std_sum,2)}, 그룹별 표준편차의 표준편차: {np.round(group_std_std, 2)}")

#     previous_group_std_sum = group_std_sum
#     previous_group_std_std = group_std_std
#     group_std_sum, group_std_std, df_group = calculate_group_std_sum_and_std()
    
# st.write('최종 그룹별 표준편차 합:', group_std_sum)
# st.write('최종 그룹별 표준편차의 표준편차:', group_std_std)

# st.write(df_group)

# result = []
# for i in range(k):
#     result.append(df_group[df_group['group'] == i+1][categories].sum())
#     group_mean = df_group[df_group['group'] == i+1][categories].sum().mean()
#     group_std = df_group[df_group['group'] == i+1][categories].sum().std()
#     # st.write('group', i+1, '의 범주별 인원 수', group_std)
# result= pd.DataFrame(result)
# result['group']=range(1, 1+k)
# st.write(result)


##############################

# import seaborn as sns
# import matplotlib.pyplot as plt
# import streamlit as st
# import numpy as np
# import pandas as pd
# from faker import Faker

# st.title("학생들의 특성을 바탕으로 조 편성하기🤼‍♂️")
# st.write("수업 등에서 모둠을 구성할 때, 일반적으로 랜덤으로 편성을 많이 합니다. 하지만 가끔 경우에 따라 학생들의 특성에 따라 조를 편성하면 좋은 경우가 있습니다. 예를 들어 모둠별로 문제를 해결해야 하는 수업에서 점수가 낮은 학생들만 모여있다면 원활하게 진행되지 않겠죠? 혹은, 학생들의 특성이 어느정도는 달라야 서로 상호작용을 하며 배우는 것이 더 많을텐데요! 이러한 점을 고려해서 모둠을 편성하는 예시입니다. 완성된 결과를 보고, 꼭 검토 후 사용해주세요!")


# fake = Faker('ko_KR')

# # n명의 자료 생성하기
# def generate_names_faker(n):
#     names = []
#     for _ in range(n):
#         name = fake.name()
#         names.append(name)
#     return names

# # n명을 k개 그룹으로 나눌 때 조별 인원수 리스트
# def divide_n_into_k_parts(n, k):
#     quotient = n // k
#     remainder = n % k

#     sizes = [quotient] * k
#     for i in range(remainder):
#         sizes[i] += 1

#     intervals = []
#     start = 0
#     for size in sizes:
#         end = start + size
#         intervals.append(size)
#         start = end

#     return intervals

# st.write("❗업로드 기능 보완 예정❗")
# uploaded_file = st.file_uploader("파일 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")

# # 샘플 데이터 생성
# n_students = int(st.text_input('샘플 데이터를 생성합니다. 학생 수를 설정해주세요:', value = 30))
# names = generate_names_faker(n_students)
# scores = np.round(np.random.normal(loc=55, scale=18, size=n_students))
# scores = np.clip(scores, 0, 100)
# grades = np.random.choice(['A', 'B', 'C', 'D'], size=n_students, p=[0.3, 0.3, 0.2, 0.2])
# energy = np.random.choice(['E','I'], size=n_students, p=[0.6, 0.4])
# data = {'이름': names, '점수': scores, '특성': grades, '에너지': energy}
# sample_data = pd.DataFrame(data)

# try:
#     if uploaded_file is None:
#         if st.button('샘플 자료 적용해보기'):
#             df = sample_data
#             st.write('샘플 자료 생성 완료! {}명의 학생입니다. 데이터는 버튼을 누를 때마다 리셋됩니다.  '.format(len(sample_data)))
#             st.write(df)
#     elif st.button('업로드한 학생 파일 확인하기'):
#         uploaded_file = pd.read_csv(uploaded_file, encoding='euc-kr')
#         st.write(uploaded_file)
#         df = sample_data
#         st.write(df)
#         st.write('학생 파일 업로드 완료!')

# except ValueError:
#     st.write("파일을 업로드하거나 샘플 학생 데이터를 생성해보세요.")        

# k = int(st.text_input('모둠 수를 입력하세요:', value=8)) # 그룹의 개수

# # 라디오 버튼 선택에 따른 코드 실행
# selected_option = st.radio("옵션 선택", ['랜덤', '수치', '범주'])

# if selected_option == '랜덤':
#     if st.button('편성하기'):
#         st.write('랜덤으로 모둠을 편성합니다.')

#         n = len(df)
#         # 인원수 리스트 생성
        
#         # 랜덤 셔플
#         sample_random = df.sample(frac=1).reset_index(drop=True)
#         # 그룹 부여
#         sample_random['group'] = 0
#         # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
#         start = 0
#         nb_of_st_list = divide_n_into_k_parts(n, k)

#         for i, nb in enumerate(nb_of_st_list):
#             end = start + nb
#             sample_random.loc[start:end-1, 'group'] = i + 1
#             start = end
#         st.write(sample_random)

# elif selected_option == '수치':
#     col = st.text_input('기준이 되는 열 이름을 입력해주세요("점수"):', value='점수')
#     st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')
#     if st.button('편성하기'):
#         # 수치 편성 코드
#         # ...
#         st.write('hello numerical')

# elif selected_option == '범주':
#     col = st.selectbox('기준이 되는 열 이름을 선택해주세요', ['특성', '에너지'])
#     st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')
#     if st.button('편성하기'):
#         # 범주 편성 코드
#         # ...
#         st.write('hello categorical')


# fake = Faker('ko_KR')
# # n명의 자료 생성하기
# def generate_names_faker(n):
#     names = []
#     for _ in range(n):
#         name = fake.name()
#         names.append(name)
#     return names



# # n명을 k개 그룹으로 나눌 때 조별 인원수 리스트
# def divide_n_into_k_parts(n, k):
#     quotient = n // k
#     remainder = n % k

#     sizes = [quotient] * k
#     for i in range(remainder):
#         sizes[i] += 1

#     intervals = []
#     start = 0
#     for size in sizes:
#         end = start + size
#         intervals.append(size)
#         start = end

#     return intervals

# st.write("❗업로드 기능 보완 예정❗")
# uploaded_file = st.file_uploader("파일 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")
# # 샘플 데이터 생성
# n_students = int(st.text_input('샘플 데이터를 생성합니다. 학생 수를 설정해주세요:', value = 30))
# names = generate_names_faker(n_students)
# scores = np.round(np.random.normal(loc=55, scale=18, size=n_students))
# scores = np.clip(scores, 0, 100)
# grades = np.random.choice(['A', 'B', 'C', 'D'], size=n_students, p=[0.3, 0.3, 0.2, 0.2])
# energy = np.random.choice(['E','I'], size=n_students, p=[0.6, 0.4])
# data = {'이름': names, '점수': scores, '특성': grades, '에너지':energy}
# sample_data = pd.DataFrame(data)


# # if st.button('샘플 파일 적용해보기'):
# #     uploaded_file = sample_data
# #     st.write('샘플 파일 생성 완료! {}명의 학생입니다. 데이터는 버튼을 누를 때마다 리셋됩니다.  '.format(len(sample_data)))
# #     st.write(sample_data)

# try:
#     # 파일 업로드
#     if uploaded_file is None:
#         if st.button('샘플 자료 적용해보기'):
#             df = sample_data
#             st.write('샘플 자료 생성 완료! {}명의 학생입니다. 데이터는 버튼을 누를 때마다 리셋됩니다.  '.format(len(sample_data)))
#             st.write(df)
#     elif st.button('업로드한 학생 파일 확인하기'):
#         uploaded_file = pd.read_csv(uploaded_file, encoding = 'euc-kr')
#         # uploaded_file = sample_data
#         st.write(uploaded_file)
#         df = sample_data
#         st.write(df)
#         st.write('학생 파일 업로드 완료!')
        
# except ValueError:
#     st.write("파일을 업로드하거나 샘플 학생 데이터를 생성해보세요.")        
# # try:
# #     df = pd.DataFrame(uploaded_file.values[:,:])
# #     st.write(df)
# # except:
# #     st.write(":D")

# #df = pd.DataFrame(uploaded_file)#.values[:,:])
# df = sample_data

# k = int(st.text_input('모둠 수를 입력하세요:', value = 8)) # 그룹의 개수
# n = len(df)

# nb_of_st_list = divide_n_into_k_parts(n, k)




# # 라디오 버튼 선택에 따른 코드 실행
# selected_option = st.radio("옵션 선택", ['랜덤', '수치', '범주'])

# if selected_option == '랜덤':
#     if st.button('편성하기'):
#         st.write('랜덤으로 모둠을 편성합니다.')

#         n = len(df)
#         # 인원수 리스트 생성
        
#         # 랜덤 셔플
#         sample_random = df.sample(frac = 1).reset_index(drop=True)
#         # 그룹 부여
#         sample_random['group'] = 0
#         # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
#         start = 0
#         for i, nb in enumerate(nb_of_st_list):
#             end = start + nb
#             sample_random.loc[start:end-1, 'group'] = i + 1
#             start = end
#         st.write(sample_random)

#     # if st.button('특성 고려해서 편성하기'):
#     #     # column 이름들을 버튼으로 만들기
#     #     cols = df.columns.tolist()
#     #     for col in cols:
#     #         if st.button(col):
#     #             st.write(df[col])

#     #     # 선택된 column들만 출력하기
#     #     if not st.button('Show All'):
#     #         st.write(df)




# elif selected_option == '수치':
#     col = st.text_input('기준이 되는 열 이름을 입력해주세요("점수"):', value='점수')
#     st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')
#     if st.button('편성하기'):
#         # 수치 편성 코드
#         # ...
#         st.write('hello numerical')


# elif selected_option == '범주':
#     col = st.selectbox('기준이 되는 열 이름을 선택해주세요', ['특성', '에너지'])
#     st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')
#     if st.button('편성하기'):
#         # 범주 편성 코드
#         # ...
#         st.write('hello categorical')






# # 랜덤
# if st.button('랜덤 모둠 편성'):
#     st.write('랜덤으로 모둠을 편성합니다.')
#     n = len(df)
#     # 인원수 리스트 생성
    
#     # 랜덤 셔플
#     sample_random = df.sample(frac = 1).reset_index(drop=True)
#     # 그룹 부여
#     sample_random['group'] = 0
#     # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
#     start = 0
#     for i, nb in enumerate(nb_of_st_list):
#         end = start + nb
#         sample_random.loc[start:end-1, 'group'] = i + 1
#         start = end
#     st.write(sample_random)

# # if st.button('특성 고려해서 편성하기'):
# #     # column 이름들을 버튼으로 만들기
# #     cols = df.columns.tolist()
# #     for col in cols:
# #         if st.button(col):
# #             st.write(df[col])

# #     # 선택된 column들만 출력하기
# #     if not st.button('Show All'):
# #         st.write(df)
# col = st.text_input('기준이 되는 열 이름을 입력해주세요("점수", "특성", "에너지") : ')
# st.write(col, '(을/를) 고려하여 학생을 모둠별로 편성한 결과를 보려면 아래 버튼을 클릭해주세요. ')

# # 수치
# if col =='점수': 
#     def calculate_team_mean(team): 
#         team_mean_list = []
#         for i in range(k):
#             team_mean = team[i].T[1].mean()
#             team_mean_list.append(team_mean)
#         return team_mean_list

#     data = np.array(df.loc[:,['이름', col]])#[['이름', '점수']])

#     team = []
#     # 일단 순서대로 구분
#     start = 0
#     for nb in nb_of_st_list:
#         end = start + nb
#         team.append(data[start:end])
#         start = end

#     # 초기값 설정
#     team_mean_list = calculate_team_mean(team)
#     dispersion = np.max(team_mean_list)-np.min(team_mean_list)
#     st.write("## 그룹 편성 결과")

#     for ii in range(10):
        
#         #그 그룹 추출하기#############################################update
#         min, max = team[0].T[1].mean(), team[0].T[1].mean()
#         max_index = np.argmax(team_mean_list)
#         min_index = np.argmin(team_mean_list)

#         #최댓값 최솟값 뽑기 (min, max)
#         team_min = team[min_index]
#         team_max = team[max_index]
#         #print(team_min, team_max)
#         # team_min 에서 낮은 사람과 team_max에서 높은 사람 교환
#         max_row_idx = np.argmax(team_max[:, 1])
#         max_row = team_max[max_row_idx, :]
#         min_row_idx = np.argmin(team_min[:, 1])
#         min_row = team_min[min_row_idx, :]

#         team_max = np.delete(team_max, max_row_idx, axis=0)
#         team_max = np.vstack([team_max, min_row])
#         team_min = np.delete(team_min, min_row_idx, axis=0)
#         team_min = np.vstack([team_min, max_row])
#         #print(team_min, team_max)
#         team[max_index] = team_max
#         team[min_index] = team_min
#         #############################################################updated
#         team_mean_list_new = calculate_team_mean(team)
#         dispersion_new = np.max(team_mean_list_new)-np.min(team_mean_list_new)
        
#         st.write("그룹별 평균 점수의 범위가", np.round(dispersion, 2),"에서", np.round(dispersion_new, 2), "로 업데이트 되었어요!")        
#         if dispersion_new > dispersion:
#             break
#         dispersion = dispersion_new
#         #team = team_new
#         team_mean_list = team_mean_list_new


#         #####################range_i_new >= range_i 라면 반복문 break,
#     st.write("다음 step에서는 그룹별 평균 점수의 범위가 더 커졌으므로 여기서 중단합니다. ")
#     team_df = pd.concat([pd.DataFrame(arr) for arr in team], ignore_index=True)
#     team_df.columns = ['이름', '점수']
#     team_df['group'] = 0
#     # 리스트 nb_of_st_list를 사용하여 'group' 열에 값을 할당
#     start = 0
#     for i, nb in enumerate(nb_of_st_list):
#         end = start + nb
#         team_df.loc[start:end-1, 'group'] = i + 1
#         start = end

#     st.write(team_df)
#     st.write("최종 팀별 평균은 각각 {}입니다. ".format(np.round(team_mean_list)))

# # 범주
# elif col =="특성" or "에너지":
#     def calculate_team_sum_std(team): 
#         team_vec_list = []
#         team_vec_std_list = []
#         for t in team:
#             team_vec = np.sum(t.T[2:2+len(df[col].unique())], axis = 1)
#             team_vec_list.append(team_vec)
#             team_vec_std_list.append(np.std(team_vec))
#         return team_vec_list, team_vec_std_list
#     # Define the objective_function
#     def objective_function(team):
#         team_vec_list, team_vec_std_list = calculate_team_sum_std(team)
#         return np.sum(team_vec_std_list)

#     # Define the neighborhood_function
#     def neighborhood_function(team):
#         new_team = team.copy()
#         # Implement logic to swap students between teams in the new_team allocation
#         return new_team

#     # Define the simulated_annealing function
#     def simulated_annealing(initial_team):
#         current_team = initial_team
#         current_energy = objective_function(current_team)

#         # Set the initial temperature and other parameters
#         temperature = 100.0
#         cooling_rate = 0.01
#         num_iterations = 1000

#         best_team = current_team
#         best_energy = current_energy

#         for _ in range(num_iterations):
#             new_team = neighborhood_function(current_team)
#             new_energy = objective_function(new_team)

#             if new_energy < current_energy or np.random.rand() < np.exp((current_energy - new_energy) / temperature):
#                 current_team = new_team
#                 current_energy = new_energy

#             if new_energy < best_energy:
#                 best_team = new_team
#                 best_energy = new_energy

#             temperature *= 1 - cooling_rate

#         return best_team

#     # Provide the initial team allocation
#     initial_team = []  # Replace with your initial team allocation

#     # Train the model using Simulated Annealing
#     optimal_team = simulated_annealing(initial_team)


#     def reset_cate(df):

#         df = df[['이름', col]]
#         one_hot_encoded = pd.get_dummies(df[col], prefix=col)
#         # one-hot encoding
#         data = np.array(pd.concat([df, one_hot_encoded], axis=1))
#         data_df = pd.DataFrame(data)
#         data_df.columns = ['이름', col]+list(df[col].unique())
#         data_df['group'] = 0
#         data_df = data_df.sample(frac = 1).reset_index(drop=True)
#         # 조 임의 편성
#         team = []
#         start = 0
#         for nb in nb_of_st_list:
#             end = start + nb
#             team.append(data[start:end])
#             start = end

#         start = 0
#         for i, nb in enumerate(nb_of_st_list):
#             end = start + nb
#             data_df.loc[start:end-1, 'group'] = i + 1
#             start = end        #

#         def calculate_team_sum_std(team): 
#             team_vec_list = []
#             team_vec_std_list = []
#             for t in team:
#                 team_vec = np.sum(t.T[2:2+len(df[col].unique())], axis = 1)
#                 team_vec_list.append(team_vec)
#                 team_vec_std_list.append(np.std(team_vec))
#             return team_vec_list, team_vec_std_list

#         team_vec_list, team_vec_std_list = calculate_team_sum_std(team)

#         st.write("## 모둠별 '불균형도'의 합(The lower, the better):",np.round(np.sum(team_vec_std_list), 2))
#         st.write('y값은 낮을수록 학생들이 골고루 있다는 뜻입니다! (그룹 내 학생들의 원핫인코딩 벡터합 원소의 표준편차)')
#         st.write('이 결과가 마음에 드실 경우, 아래의 표를 복사하여 스프레드시트에 붙여넣기 해주세요.')
#         st.write(data_df)
#         st.write('합을 최소화시키는 알고리즘은 곧 업데이트 될 예정입니다.😂')

#     if st.button('편성 결과 보기'):
#         reset_cate(df)