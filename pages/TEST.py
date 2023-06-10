import os
import streamlit as st
import csv

# 현재 파일이 위치한 디렉토리
current_directory = os.path.dirname(os.path.abspath(__file__))
# 데이터 파일 경로
data_file_path = os.path.join(current_directory, 'data.csv')

# Streamlit 앱 코드
def main():
    st.title("Data to CSV Example")
    
    # 데이터 입력을 위한 텍스트 입력 필드
    data_input = st.text_input("Enter data")
    
    # 저장 버튼
    if st.button("Save"):
        # CSV 파일을 추가 모드로 열기
        with open(data_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            # 데이터를 CSV 파일에 작성
            writer.writerow([data_input])
        st.success("Data saved successfully!")
    
    # CSV 파일의 데이터 표시
    # with open(data_file_path, 'r') as file:
    #     reader = csv.reader(file)
    #     rows = list(reader)
    #     st.table(rows)

# Streamlit 앱 실행
if __name__ == '__main__':
    main()
