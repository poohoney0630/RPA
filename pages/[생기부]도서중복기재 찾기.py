import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import datetime
import time
import random

# 페이지 설명 부분
st.title("학교생활기록부 독서기록 중복 찾기📚")
st.write("생활기록부 점검시, 학생마다 독서기록이 중복된 경우가 왕왕 있습니다. 예를 들어 한 학생이 2학년 1학기와 1학년 1학기에 같은 책을 기록한 경우죠! 나이스에서 **반별 독서기록파일**을 csv파일로 다운받아, 아래에 업로드해주세요. 중복된 항목이 출력됩니다. ")

sample_book = pd.read_csv('https://raw.githubusercontent.com/Surihub/RPA/main/data/book_recording_sample.csv')
# 샘플파일 업로드 하거나 파일 업로드

uploaded_file = st.file_uploader("(파일 업로드 기능 보완 예정)파일 업로드해주세요! 준비된 파일이 없을 경우, 아래 '샘플 파일 업로드 해보기' 버튼을 눌러 테스트해보세요.", type="csv")
if uploaded_file is None:
    if st.button('샘플 파일 업로드 해보기'):
        #uploaded_file = pd.read_csv('book_recording_sample.csv')
        uploaded_file = pd.read_csv('https://raw.githubusercontent.com/Surihub/RPA/main/data/book_recording_sample.csv')
        st.write('샘플 파일 업로드 완료! 눈으로 먼저 중복된 항목이 있는지 살펴보시고, 아래의 중복 기재 확인하기 버튼을 눌러주세요.')
        st.write(uploaded_file)
uploaded_file = uploaded_file
if st.button('중복 기재 확인하기!'):
    st.write("중복을 확인합니다......")

    #try:
    if uploaded_file is None:
        uploaded_file = sample_book
        
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
        #print("2.    " , book_list)

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
    #except:
    #    print(":D")
