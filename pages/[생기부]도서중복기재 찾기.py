import streamlit as st
import pandas as pd
import numpy as np
from kiwipiepy import Kiwi

# 페이지 설명 부분
st.title("📚학생부 독서기록 중복 찾기")

st.info('###### 언제 사용하나요?\n생활기록부 점검시, 학생마다 독서기록이 중복된 경우가 왕왕 있습니다. 예를 들어 한 학생이 2학년 1학기와 1학년 1학기에 같은 책을 기록한 경우죠! 나이스에서 **반별 독서기록파일**을 csv파일로 다운받아, 아래에 업로드해주세요. 유사도에 따라 중복되거나 비슷한 형태소로 이뤄진 두 도서가 출력됩니다.')
st.warning('###### 어떻게 해결하나요?\n독서기록.csv ➡ 중복된 항목 출력')

         
def preprocessing(df):
    st.write(df)
    df = df.iloc[3:, :6]
    df.columns = ["name", "section", "year", "grade", "sem", "book"]  # column 이름 지정
    df = df.dropna(how='all')  # 모든 칸이 nan인 행 지우기
    df = df.fillna(method='ffill')  # 행별로 이름 채우기(전 행의 이름과 동일하게)
    df.drop(df[df['name'] =='이  름'].index, inplace=True)  # 페이지 넘어갈 때 있는 열이름 중복되므로 삭제
    original = df.values.tolist()  # list로
    pd.options.display.max_colwidth = 100
    return df

def find_duplicate_books_2(df, cut_off):
    kiwi = Kiwi()
    for student in df.name.unique():
        # 학생별로 도서명 문자열로 담기
        temp = df[df.name == student]
        all_book = temp.book.tolist()
        book_list_incomplete = []
        for book_by_row in all_book:
            book_list_incomplete = book_list_incomplete + book_by_row.split("), ")

        # 빈 문자열 원소 제거 및 괄호 처리하기
        book_list = []
        for book in book_list_incomplete:
            if len(book) == 0:
                continue
            elif book[-1] == ")":
                book_list.append(book)
            else:
                book_list.append(book + ")")

        for i in range(len(book_list)):
            for j in range(i+1, len(book_list)):
                similarity, morphs = get_similarity(book_list[i], book_list[j], kiwi)
                if similarity == 2:
                    st.write('#### 😱 {} 학생의 중복된 독서기록입니다.'.format(student))
                    st.write('📙', book_list[i], '📗', book_list[j])
                    st.write(temp[temp['book'].str.contains(book_list[i][:5])].iloc[:,1:])
                elif similarity >= cut_off:
                    st.write('#### {} 학생의 비슷한 독서기록입니다. 유사도:{}'.format(student, np.round(similarity, 2)))
                    # st.write(morphs)#########
                    st.write('📙', book_list[i], '📗', book_list[j])
                    st.write(temp[temp['book'].str.contains(book_list[i][:5])].iloc[:,1:])
                    st.write(temp[temp['book'].str.contains(book_list[j][:5])].iloc[:,1:])

def get_similarity(str1, str2, kiwi):
    # 문자열을 Kiwi 형태소 분석기를 사용하여 형태소로 분석
    tokens1 = kiwi.analyze(str1)[0][0]
    tokens2 = kiwi.analyze(str2)[0][0]

    # 형태소들을 추출하여 리스트에 저장
    morphemes1 = [token[0] for token in tokens1]
    morphemes2 = [token[0] for token in tokens2]
    morphemes1.remove('(')
    morphemes1.remove(')')
    morphemes2.remove('(')
    morphemes2.remove(')')
    morphs = [morphemes1, morphemes2]

    # 두 리스트의 길이의 합과 중복을 제외한 요소의 개수를 계산
    list_sum = len(morphemes1 + morphemes2)
    set_sum = len(set(morphemes1 + morphemes2))

    # 유사도 계산 (두 리스트의 길이의 합을 중복을 제외한 요소의 개수로 나눔)
    similarity = list_sum / set_sum

    # 유사도 반환
    return similarity, morphs

cut_off_percent = st.slider("유사도(%)를 설정해주세요. 유사도가 100인 경우 완전히 일치하는 도서가 출력됩니다.", min_value=50, max_value=100, step=10, value = 100 )
cut_off = cut_off_percent*0.014+0.6 # 100이면 2로, 50이면 약 1.3정도로

if 'book_record' not in st.session_state:
    st.session_state['book_record'] = ''

sample_book = pd.read_csv('https://raw.githubusercontent.com/Surihub/RPA/main/data/book_recording_sample.csv')


sample_checked = st.checkbox('샘플 파일 중복 기재 확인하기')
if sample_checked:
    with st.spinner('중복을 확인하는 중 입니다...'):
        find_duplicate_books_2(preprocessing(sample_book), cut_off)


book_record = st.file_uploader("파일 업로드해주세요! 준비된 파일이 없을 경우, 위의 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")
if book_record:
    book_record = pd.read_csv(book_record)
    st.session_state['book_record'] = book_record

upload_checked = st.checkbox('업로드한 파일 중복 기재 확인하기!')
if upload_checked:
    with st.spinner('중복을 확인하는 중입니다...'):
        try:
            find_duplicate_books_2(preprocessing(st.session_state['book_record']), cut_off)
        except:
            st.write("⚠올바른 파일을 업로드하셨는지 확인해주세요!")
