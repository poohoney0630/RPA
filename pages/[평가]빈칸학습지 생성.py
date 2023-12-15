import streamlit as st
from kiwipiepy import Kiwi
import docx
from io import BytesIO

# from transformers import BertTokenizer, BertModel
# import torch

# 페이지 제목 설정
st.title("🧐빈칸 뚫기 학습지 만들기")

# 두 컬럼 생성
col1, col2 = st.columns(2)
with col1:
    st.info('###### 언제 사용하나요?\n텍스트 입력해서 하나하나 지우고 빈칸을 만들어야 할 때!')
with col2:
    st.warning('###### 어떻게 해결하나요?\n입력받은 텍스트의 해당 부분을 클릭하면 빈칸으로 만들어서 워드파일로 생성하기')

# 빈칸을 만들 내용을 입력받음
contents = st.text_area("빈칸을 만들 내용을 입력해주세요", value="의사는 인간의 존엄과 가치를 존중하며, 의료를 적정하고 공정하게 시행하여 인류의 건강을 보호증진함에 헌신한다. ")





tab1, tab2 = st.tabs(['수작업', '자동화'])
with tab1:
    # 형태소 분석
    kiwi = Kiwi()
    tokens = kiwi.analyze(contents)[0][0]

    # 명사를 저장할 집합
    nouns = set()

    # 각 토큰에 대해 명사 추출
    for token in tokens:
        if token.tag == "NNG":
            nouns.add(token.form)

    # 명사 선택 위젯
    selected_nouns = st.multiselect('빈칸으로 만들 명사를 선택하세요', list(nouns))

    # '생성하기' 버튼
    if st.button('빈칸 뚫기 미리보기'):
        # 체크된 명사를 빈칸으로 치환
        for noun in selected_nouns:
            contents = contents.replace(noun, '___'*len(noun))

        # 결과 표시
        st.write(contents)

        # 워드 문서 생성
        doc = docx.Document()
        doc.add_paragraph(contents)
        
        # 워드 파일 다운로드
        with BytesIO() as f:
            doc.save(f)
            f.seek(0)
            st.download_button('워드 파일로 다운로드하기', f, file_name='학습지.docx')

with tab2:
    st.write("준비중입니다....")
    # # BERT 모델과 토크나이저 초기화
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    # model = BertModel.from_pretrained('bert-base-uncased', output_attentions=True)

    # # 사용자 입력 텍스트
    # text = contents

    # # BERT를 사용하여 텍스트 처리
    # inputs = tokenizer(text, return_tensors="pt", add_special_tokens=True)
    # outputs = model(**inputs)
    # attentions = outputs.attentions

    # # Attention 가중치 계산 (마지막 레이어 사용)
    # # 차원 축소를 위해 mean() 대신 squeeze() 사용
    # # Attention 가중치 계산 (마지막 레이어 사용)
    # # 여러 차원을 가진 텐서를 처리하기 위해 mean() 메소드 사용
    # last_layer_attentions = attentions[-1].squeeze(0)
    # word_attentions = last_layer_attentions.mean(dim=0).squeeze()

    # # 가중치가 스칼라가 아닐 경우를 대비해 조건부 처리
    # weighted_tokens = []
    # for token, weight in zip(tokens, word_attentions):
    #     if weight.numel() == 1:  # numel() 메소드는 텐서 내 요소의 총 개수를 반환
    #         weighted_tokens.append((token, weight.item()))
    #     else:
    #         # 텐서에 여러 요소가 있는 경우 평균값 사용
    #         weighted_tokens.append((token, weight.mean().item()))


    # # 상위 10개 중요 단어 추출
    # top_tokens = sorted(weighted_tokens, key=lambda x: x[1], reverse=True)[:10]

    # # 중요 단어 선택 위젯
    # selected_tokens = st.multiselect('중요 단어 선택', [token for token, weight in top_tokens])

    # # '생성하기' 버튼
    # if st.button('빈칸 생성하기'):
    #     # 선택된 토큰을 빈칸으로 치환
    #     for token in selected_tokens:
    #         text = text.replace(token, "____")
    #     st.write(text)