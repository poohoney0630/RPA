import pandas as pd
import streamlit as st

st.write("### **학교에서 반복적이고 기계적인 일을 적게 할 수는 없을까?**")
st.write("라는 고민(투덜)으로 시작한 업무자동화 페이지입니다. 학교에서 업무 처리가 효율적으로 된다면 교사의 전문성이 필요한 수업 평가, 기록의 질에 고민할 수 있는 시간을 확보할 수 있으니까요!")
st.write("학교에서 업무나 수업 중 느끼는 '불편함'이 바로 업무자동화 '아이디어'입니다. 🎁")
st.write('이메일로 오류나 피드백, 제안사항이 있으실 경우 언제든지 보내주세요!!')



st.write('made by **숩숩** ✉ sbhath17@gmail.com ✉')


# import pandas as pd
# import streamlit as st

# # Create input fields for text and star rating
# text_input = st.text_input("재미있게 사용하셨다면 후기를 남겨주세요!")

# # Create a styled button for star rating selection
# star_rating = st.radio("별점을 선택해주세요!", ['⭐','⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'], index=2,key="rating")

# # Create a submit button
# if st.button("의견 제출하기"):
#     # Create a dictionary with the entered data
#     data = {'Text': [text_input], 'Star Rating': [star_rating]}

#     # Append the data to an existing CSV file or create a new one
#     df = pd.DataFrame(data)

#     # Check if the CSV file has been created before
#     if 'csv_created' not in st.session_state:
#         st.session_state.csv_created = False

#     if not st.session_state.csv_created:
#         df.to_csv('feedback_rating.csv', index=False)
#         st.session_state.csv_created = True
#     else:
#         df.to_csv('feedback_rating.csv', mode='a', header=False, index=False)

#     # Display a success message
#     st.success("의견 감사합니다.😀")
