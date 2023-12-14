import streamlit as st
from pdf2image import convert_from_path
import tempfile
from PIL import Image
from streamlit_cropper import st_cropper

# 페이지 제목 설정
st.title("👀학습지를 스캔했는데 언제 본담...")

# 두 컬럼 생성
col1, col2 = st.columns(2)
with col1:
    st.info('###### 언제 사용하나요?\n스캔된 학습지(pdf파일)를 문항별로 정리해서 보고싶을 때')
with col2:
    st.warning('###### 어떻게 해결하나요?\npdf 영역별로 crop해서 모아보기!')

pdf_file = st.file_uploader("학습지 pdf 파일을 업로드해주세요.", type="pdf")


if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_file.read())
        temp_pdf_path = temp_pdf.name

    # PDF의 첫 페이지를 이미지로 변환
    images = convert_from_path(temp_pdf_path, first_page=1, last_page=1)

    if images:
        # 첫 페이지 이미지 표시 및 크롭 위젯
        image = images[0]
        cropped_image, crop_box = st_cropper(image, realtime_update=True, box_color="red", aspect_ratio=None, return_type="both")

        # "Next" 버튼
        if st.button("Next"):
            if crop_box:
                # 좌표 계산
                x1 = crop_box['left']
                y1 = crop_box['top']
                x2 = x1 + crop_box['width']
                y2 = y1 + crop_box['height']
                crop_coords = (x1, y1, x2, y2)

                # 모든 페이지를 잘라낸 이미지로 변환
                all_pages = convert_from_path(temp_pdf_path)
                for page_image in all_pages:
                    cropped_image = page_image.crop(crop_coords)
                    st.image(cropped_image)
            else:
                st.error("영역을 선택해 주세요.")