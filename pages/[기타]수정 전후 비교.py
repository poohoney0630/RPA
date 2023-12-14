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
    text1 = st.text_input("수정 전 텍스트를 입력해주세요.", value = "띄어쓰기안했쥐롱")
with text_after:
    text2 = st.text_input("수정 후 텍스트를 입력해주세요.", value = "띄어쓰기 했찌롱")

# difflib를 사용하여 두 텍스트의 차이를 시각적으로 표시
def show_diff(text1, text2):
    diff = difflib.ndiff(text1, text2)
    diff_text = ""
    for c in diff:
        if c[0] == ' ':
            diff_text += c[2]
        elif c[0] == '-':
            diff_text += f"<span style='color: red; font-weight: bold; text-decoration: line-through;'>{c[2]}</span>"
        elif c[0] == '+':
            diff_text += f"<span style='color: blue; font-weight: bold;'>{c[2]}</span>"
    return diff_text

if st.button("비교하기"):
    diff_result = show_diff(text1, text2)
    st.markdown(diff_result, unsafe_allow_html=True)
