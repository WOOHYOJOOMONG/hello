import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# ✅ 구글 시트 인증
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(
    dict(st.secrets["gcp_service_account"]),
    scopes=scopes
)
client = gspread.authorize(credentials)

# ✅ 구글 시트 열기
try:
    sheet = client.open_by_key("1oOQGk4IAoBgK6WeWdnlAWbLrIBuF6G84y8CIaqXog6w").sheet1
    records = sheet.get_all_records()
except Exception as e:
    st.error(f"❌ 구글 시트 접근 중 오류: {e}")
    st.stop()

# ✅ UI 설정
st.set_page_config(page_title="알파코 이수율 확인 시스템", layout="centered")
st.markdown(
    """
    <style>
    .title-box {
        background-color: #003366;
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .title-box h1 {
        margin-bottom: 0.2rem;
        font-size: 1.7rem;  /* 메인 제목 크기 */
    }
      .title-box p {
        font-size: 1.6rem;  /* 소제목 크기 증가 */
        margin-top: 0.3rem;
        font-weight: 600;  /* 굵게 강조 */
    }
      .title-box k {
        font-size: 1.5rem;  /* 제일 작은 제목 크기 증가 */
        margin-top: 0.5rem;
        font-weight: 600;  /* 굵게 강조 */
   
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="title-box"><h1>‍📚 [2025 교실혁명 선도교사 양성연수(5권역)] 🧑‍🏫</h1><p><이수율 현황 확인></p><k>이수율은 강의 후 24시간 뒤 반영됩니다.</k></div>', unsafe_allow_html=True)

# ✅ 사용자 입력
st.markdown("##### ※ 이수율은 강의 후 24시간 뒤 반영됩니다.")
name = st.text_input("👤 이름을 입력하세요: ", placeholder="예: 홍길동")
phone_last4 = st.text_input("📱 전화번호 뒷 네 자리를 입력하세요: ", max_chars=4, placeholder="예: 1234")

st.markdown("---")

# ✅ 사용자 찾기 함수
def find_user(name, phone_last4):
    for user in records:
        if user["이름"] == name and str(user["전화번호뒷자리"]).zfill(4) == phone_last4:
            return user
    return None

# ✅ 조회 버튼
if st.button("📥 이수율 조회하기"):
    if not name or not phone_last4:
        st.warning("⚠️ 이름과 전화번호 뒷자리를 모두 입력해주세요.")
    else:
        user = find_user(name, phone_last4)
        if user:
            st.success(f"🎉 {user['이름']} 선생님의 이수 정보")

            # 사전진단 + 사전워크숍
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("사전진단(2차시/120분)", value=f"{user['사전진단']}분", disabled=True)
            with col2:
                st.text_input("사전워크샵(3차시/180분)", value=f"{user['사전워크샵']}분", disabled=True)
            st.markdown("<hr>", unsafe_allow_html=True)

            # 원격연수
            st.text_input("원격연수(9과정 16차시/960분)", value=f"{user['원격연수설명']}", disabled=True)
            st.markdown("<hr>", unsafe_allow_html=True)

            # 집합연수 + 컨퍼런스
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("집합연수(14차시/840분)", value=f"{user['집합연수']}분", disabled=True)
            with col2:
                st.text_input("컨퍼런스(5차시/300분)", value=f"{user['컨퍼런스']}분", disabled=True)
            st.markdown("<hr>", unsafe_allow_html=True)

            st.divider()
            st.metric(label="총 이수율", value=f"{user['총이수율']}%")

            if user["이수여부"] == "이수":
                st.success("✅ 이수 완료")
            else:
                st.error("📌 미이수")
        else:
            st.error("😢 입력하신 정보와 일치하는 사용자가 없습니다.")
