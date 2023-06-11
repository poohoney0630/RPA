import streamlit as st

st.title("📎연수 자료 모음")

st.write("## 1. Google Apps Script에서 자동 메일 전송하기 코드")
st.write('여러 명의 사람들에게 한꺼번에, 개별화된 메일을 보낼 수 있는 GAS 코드입니다. ')
st.write("구글 앱스 스크립트 링크 : [Google Apps Script](https://www.google.com/script/start/)")

# Define your code
code = """
function sendEmails() {
  //스프레드시트 열기(스프레드시트 주소로)
  var spreadsheet = SpreadsheetApp.openByUrl('여기에 구글 시트 주소를 붙여넣어주세요. ');

  //시트 가져오기
  var sheet = spreadsheet.getSheetByName('시트1');

  //데이터 범위 가져오기
  var dataRange = sheet.getDataRange();

  // 데이터 배열로 가져오기
  var data = dataRange.getValues();
  
  // 데이터 처리를 위한 반복문image.png
  for (var i = 1; i < data.length; i++) {
    // 이메일 주소와 메시지 가져오기
    var emailAddress = data[i][0];
    var message = data[i][2];
    
    // 이메일 보내기
    MailApp.sendEmail({
      to: emailAddress,
      subject: '선생님의 피드백입니다. ',
      body: message
    });
  }
}
"""

# Create a session state variable to store the toggle state
if "show_code" not in st.session_state:
    st.session_state.show_code = False

# Display the toggle button and handle the click event
if st.button("Code"):
    st.session_state.show_code = not st.session_state.show_code

# Display the code block based on the toggle state
if st.session_state.show_code:
    st.code(code)