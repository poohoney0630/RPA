import streamlit as st

st.title("☕커피 한 잔 할래요?")


# 너무 느려져서 삭제
# # 추가할 메뉴 선택하기
# default_menu = ['아메리카노', '카페라떼']  # 디폴트로 선택할 메뉴
# custom_menu = st.multiselect(
#     "메뉴를 선택하거나 추가하려면 선택하세요",
#     ["아메리카노", "카페라떼", "카페모카", "카라멜마끼야또", "바닐라라떼"],
#     default=default_menu
# )

# # 현재 메뉴 리스트 정의
# menu = custom_menu

custom_menu = st.text_input("추가할 메뉴가 있다면 입력해주세요","바닐라라떼").split(",")

# "세션 초기화" 버튼 생성
if st.button("메뉴를 확정지은 후에 이 버튼을 눌러주세요!"):
    st.session_state.clear()  # 세션 상태 초기화

st.header("메뉴 주문하기")
menu = ['아메리카노', '라떼'] # 기본 메뉴

# 사용자가 입력한 메뉴가 비어있지 않다면 메뉴 리스트에 추가

if len(custom_menu)>0:
    for m in custom_menu:
        menu.append(m)

button_counts = {}
for item in menu:
    button_counts[f"{item} HOT"] = 0
    button_counts[f"{item} ICE"] = 0

# 버튼 클릭 수를 저장할 세션 상태 초기화
if "button_counts" not in st.session_state:
    st.session_state.button_counts = button_counts

# 아메리카노와 라떼 버튼 및 "-" 버튼 생성
for button_label in st.session_state.button_counts.keys():
    button_col1, button_col2 = st.columns(2)
    
    # "+" 버튼
    if button_col1.button(f"{button_label} ➕"):
        st.session_state.button_counts[button_label] += 1
        st.info(f"{button_label} 추가되었어요!")

    # "-" 버튼
    if button_col2.button(f"{button_label} ➖"):
        if st.session_state.button_counts[button_label] > 0:
            st.session_state.button_counts[button_label] -= 1
            st.error(f"{button_label} 삭제되었어요!")

# 주문 현황판에 카운트 표시
st.write("### 주문 현황")
total_count = 0
order_record = ""
for button_label, count in st.session_state.button_counts.items():
#    st.write(f"{button_label}: {count}잔")
    order_record = order_record+f"{button_label}: {count}잔\n"
    total_count += count
st.code(order_record)

# 총 합 표시
memo = st.text_input("기타 메뉴 혹은 메모 : ")

# "Yes" 버튼을 누르면 주문 현황판을 큰 글씨로 표시
if st.button(f"총 {total_count}잔 시키신 것 맞나요?"):
    st.header("📃주문서")
    for button_label, count in st.session_state.button_counts.items():
        if count >0:
            st.write(f"#### {button_label}: {count} 잔")
    st.write(f"#### {memo}")
    st.write(f"## 총 {total_count}잔")



