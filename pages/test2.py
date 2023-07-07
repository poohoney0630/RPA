# 세션 상태 활용하기

import streamlit as st
 
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''
 
user_input = st.text_input("텍스트를 입력하세요")
if user_input:
    st.session_state['user_input'] = user_input
 
st.write(f"입력한 내용: {st.session_state['user_input']}")
# 이 예제에서는 사용자의 입력이 세션 상태에 저장되어 애플리케이션이 다시 실행되더라도 유지됩니다.


if 'username' not in st.session_state:
    st.session_state['username'] = ''
 
username = st.text_input("사용자 이름을 입력하세요")
if username:
    st.session_state['username'] = username
 
st.write(f"안녕하세요, {st.session_state['username']}님!")