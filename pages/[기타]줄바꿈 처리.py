import streamlit as st

st.title("✅줄바꿈 띄어쓰기 마스터")

st.info('###### 언제 사용하나요?\npdf에서 텍스트를 복사해올 때, 줄바꿈이 제멋대로여서 delete&space 여러 번 하신 적 있나요? 아래에서 간단하게 처리해보세요! ')
st.warning('###### 어떻게 해결하나요?\n줄바꿈 이상한 텍스트 ➡ 줄바꿈 없이 정리된 텍스트')
def split_by_enter(text):
    return text.split('\n')

def space_remove(text):
    # 줄바꿈 문자를 공백으로 대체하여 모든 줄바꿈을 제거
    text = text.replace('\n', '')
    return text

def space_add(text):
    # 줄바꿈 문자를 공백으로 대체하여 모든 줄바꿈을 제거
    text = text.replace('\n', ' ')
    return text

def customize_spacing(text):
    # 텍스트 입력 받기
    splitted = split_by_enter(text)
    result = ""
    st.write('#### 공백을 추가하는 경우에만 체크박스에 체크해주세요.')

    for i in range(len(splitted) - 1):
        word = splitted[i].split(" ")[-1]
        word_next = splitted[i+1].split(" ")[0]
        if st.checkbox(f"{word}✅{word_next}"):
            result += splitted[i] + " "
        else:
            result += splitted[i]

    # 마지막 줄은 공백을 추가하지 않음
    result += splitted[-1]

    return result


def main():
    sample = "여러분 안녕하세요. 만나서 반\n갑습니다. 저는 숩숩입니다. 페이지에\n방문해주셔서 감사합니다:D"
    text = st.text_area("줄바꿈을 수정할 텍스트를 입력해주세요.", sample)
    fn = st.radio('space option',['공백 모두 제거','공백 모두 추가', '커스터마이징'])
    if fn == '공백 모두 제거':
        result = space_remove(text)
    elif fn == '공백 모두 추가':
        result = space_add(text)
    elif fn == '커스터마이징':
        result = customize_spacing(text)
    st.info(result)
    st.code(result)
    st.write("바로 위에서 오른 쪽에 '겹쳐진 사각형 모양'을 클릭하면 복사가 됩니다. ")

if __name__ == '__main__':
    main()
