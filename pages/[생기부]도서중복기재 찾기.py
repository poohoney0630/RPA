import streamlit as st
import pandas as pd
import difflib
from difflib import SequenceMatcher
from kiwipiepy import Kiwi
import numpy as np

# 페이지 설명 부분
st.title("학교생활기록부 독서기록 중복 찾기📚")
st.write("생활기록부 점검시, 학생마다 독서기록이 중복된 경우가 왕왕 있습니다. 예를 들어 한 학생이 2학년 1학기와 1학년 1학기에 같은 책을 기록한 경우죠! 나이스에서 **반별 독서기록파일**을 csv파일로 다운받아, 아래에 업로드해주세요. 중복된 항목이 출력됩니다. ")

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

def find_duplicate_books(df):
    # 중복된 부분 찾기 (1) 책이름과 저자명이 완벽히 일치
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

        # 중복 횟수 세기
        book_count = {}
        lists = book_list
        for i in lists:
            try:
                book_count[i] += 1
            except:
                book_count[i] = 1

        # 중복 횟수가 2 이상인 아이템의 key만 담기
        book_duplicated = []
        for k, v in book_count.items():
            if v >= 2:
                book_duplicated.append(k)

        # 출력하기
        if len(book_duplicated) > 0:
            for book in book_duplicated:
                st.write('\n', student, "학생의 독서기록 중 **", book, "**이 중복되었습니다.")
            for i in range(len(book_duplicated)):
                st.write(temp[temp['book'].str.contains(book_duplicated[i][:2])])
        else:
            continue

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
                similarity = get_similarity(book_list[i], book_list[j], kiwi)
                if similarity == 2:
                    st.write('#### 😱 {} 학생의 중복된 독서기록입니다.'.format(student))
                    st.write('📙', book_list[i], '📗', book_list[j])
                    st.write(temp[temp['book'].str.contains(book_list[i][:5])].iloc[:,1:])
                elif similarity >= cut_off:
                    st.write('#### {} 학생의 비슷한 독서기록입니다. 유사도:{}'.format(student, np.round(similarity, 2)))
                    st.write('📙', book_list[i], '📗', book_list[j])
                    st.write(temp[temp['book'].str.contains(book_list[i][:5])].iloc[:,1:])
                    st.write(temp[temp['book'].str.contains(book_list[j][:5])].iloc[:,1:])
                




def get_similarity(str1, str2, kiwi):
    tokens1 = kiwi.analyze(str1)[0][0]
    tokens2 = kiwi.analyze(str2)[0][0]

    morphemes1 = [token[0] for token in tokens1]
    morphemes2 = [token[0] for token in tokens2]

    list_sum = len(morphemes1+morphemes2)
    set_sum = len(set(morphemes1+morphemes2))
    similarity = list_sum/set_sum
    return similarity

cut_off_percent = st.slider("조절할 숫자", min_value=50, max_value=100, step=10, value = 100 )
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
