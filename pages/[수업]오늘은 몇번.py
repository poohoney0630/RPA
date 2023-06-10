import random
import streamlit as st

st.title("🥴오늘은 몇번이 발표해볼까~?🤗")


def extract_random_numbers(n, m):
    numbers = list(range(1, n+1))
    random_numbers = random.sample(numbers, m)
    return random_numbers

def main():
    n = st.number_input("끝 번호를 입력해주세요!", min_value=1, value=10, step=1)
    m = st.number_input("몇 개의 번호를 추첨할 것인지 입력해주세요!", min_value=1, value=5, step=1)    

    if st.button("번호 추첨하기!"):
        random_numbers = extract_random_numbers(int(n), int(m))
        st.success(f"## 추첨 번호 : {random_numbers}")

if __name__ == '__main__':
    main()
