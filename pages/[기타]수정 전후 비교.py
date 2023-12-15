import streamlit as st
import difflib

# 페이지 제목 설정
st.title("🧐무엇이 바뀌었는가...")

# 두 컬럼 생성
col1, col2 = st.columns(2)
with col1:
    st.info('###### 언제 사용하나요?\n두 텍스트에서 어떤 부분이 바뀌었는지 두 눈을 크게 떠도 찾지 못할 때!')
with col2:
    st.warning('###### 어떻게 해결하나요?\n하나하나 비교하기')

# 텍스트 입력 받기
text_before, text_after = st.columns(2)
with text_before:
    text1 = st.text_area("수정 전 텍스트를 입력해주세요.", value = "안녕하셰요!반 갑솝니다. ")
with text_after:
    text2 = st.text_area("수정 후 텍스트를 입력해주세요.", value = "안녕하세요! 반갑습니다. ")


# difflib를 사용하여 두 텍스트의 차이를 시각적으로 표시
@st.cache_data
def show_diff(text1, text2, font_size):
    diff = difflib.ndiff(text1, text2)
    diff_text = ""
    for c in diff:
        if c[0] == ' ':
            diff_text += c[2]
        elif c[0] == '-':
            diff_text += f"<span style='color: red; background-color: #e9e9e9; font-weight: bold; font-size: {font_size}em; text-decoration: line-through;'>{c[2]}</span>"
        elif c[0] == '+':
            if c[2] == ' ':
                diff_text += f"<span style='color: blue; background-color: yellow; font-weight: bold; font-size: {font_size}em; text-decoration: underline;'>v</span>"
            else:
                diff_text += f"<span style='color: blue; background-color: yellow; font-weight: bold; font-size: {font_size}em; text-decoration: underline;'>{c[2]}</span>"
    return diff_text

font_size = st.number_input("수정할 부분을 얼마나 크게 나타낼까요?", value = 1.5)

if st.button("비교하기"):

    diff_result = show_diff(text1, text2, font_size)
    st.markdown(diff_result, unsafe_allow_html=True)
