# ... (상단 인증 및 설정 동일) ...

# ✅ UI 설정
st.set_page_config(page_title="알파코 이수율 확인 시스템", layout="centered")
st.markdown("""
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
        font-size: 1.7rem;
    }
    .title-box p {
        font-size: 1.6rem;
        margin-top: 0.3rem;
        font-weight: 600;
    }
    .info-block {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 1.5rem;
    }
    .info-block h4 {
        font-size: 18px;
        margin-bottom: 0.5rem;
    }
    .info-block p {
        font-size: 22px;
        font-weight: 600;
        margin: 0;
        color: #222;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-box"><h1>‍📚 [2025 교실혁명 선도교사 양성연수(5권역)] 🧑‍🏫</h1><p><이수율 현황 확인></p></div>', unsafe_allow_html=True)
st.markdown("##### ※ 이수율은 강의 후 24시간 뒤 반영됩니다.")

# ✅ 사용자 입력
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

            # 사전진단 & 사전워크숍
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-block"><h4>☑️ 사전진단 (2차시 / 120분)</h4><p>{}분</p></div>'.format(user["사전진단"]), unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="info-block"><h4>☑️ 사전워크숍 (3차시 / 180분)</h4><p>{}분</p></div>'.format(user["사전워크샵"]), unsafe_allow_html=True)

            # 원격연수
            st.markdown('<div class="info-block"><h4>☑️ 원격연수 (9과정 16차시 / 960분)</h4><p>{}분</p></div>'.format(user["원격연수"]), unsafe_allow_html=True)

            # 집합연수 & 컨퍼런스
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="info-block"><h4>☑️ 집합연수 (14차시 / 840분)</h4><p>{}분</p></div>'.format(user["집합연수"]), unsafe_allow_html=True)
            with col2:
                st.markdown('<div class="info-block"><h4>☑️ 컨퍼런스 (5차시 / 300분)</h4><p>{}분</p></div>'.format(user["컨퍼런스"]), unsafe_allow_html=True)

            # 총 이수율
            st.divider()
            st.metric(label="총 이수율", value=f"{user['총이수율']}%")

            if user["이수여부"] == "이수":
                st.success("✅ 이수 완료")
            else:
                st.error("📌 미이수")
        else:
            st.error("😢 입력하신 정보와 일치하는 사용자가 없습니다.")
