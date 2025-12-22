import streamlit as st

# 1. 페이지 설정 및 디자인 (Custom CSS)
st.set_page_config(page_title="나만의 색깔 찾기 - MBTI Test", page_icon="🎨")

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 설정 */
    .main {
        background-color: #faf9f6;
        font-family: 'Pretendard', sans-serif;
    }
    
    /* 카드 스타일 디자인 */
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: 1px solid #fce4ec;
        background-color: white;
        color: #5d4037;
        padding: 20px;
        font-size: 16px;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    
    .stButton > button:hover {
        border-color: #f8bbd0;
        background-color: #fce4ec;
        color: #880e4f;
        transform: translateY(-2px);
    }
    
    /* 프로그레스 바 컬러 변경 */
    .stProgress > div > div > div > div {
        background-color: #f8bbd0;
    }
    
    /* 텍스트 스타일 */
    h1 {
        color: #d81b60;
        font-weight: 800;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .question-text {
        font-size: 22px;
        font-weight: 600;
        color: #4e342e;
        text-align: center;
        margin-bottom: 40px;
        padding: 20px;
    }

    .result-card {
        background-color: white;
        padding: 30px;
        border-radius: 30px;
        border: 1px solid #fce4ec;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 질문 데이터 설정
QUESTIONS = [
    {"type": "EI", "q": "주말에 더 에너지가 생기는 활동은?", "a": "친구들과 시끌벅적하게 놀기", "b": "집에서 포근한 이불 덮고 쉬기"},
    {"type": "SN", "q": "사과를 보면 드는 생각은?", "a": "빨갛고 맛있겠다, 아삭하겠지?", "b": "뉴턴의 중력.. 백설공주.. 사과 농장 주인은 누구일까?"},
    {"type": "TF", "q": "친구가 나 차 사고 났어 라고 한다면?", "a": "보험은 들었어? 다친 데는?", "b": "헐 세상에.. 너무 놀랐겠다, 괜찮아?"},
    {"type": "JP", "q": "여행 가기 전 나의 모습은?", "a": "시간 단위로 촘촘하게 엑셀 계획표 작성", "b": "비행기표랑 숙소만 있으면 어디든 갈 수 있어"},
    {"type": "EI", "q": "처음 본 사람과 대화할 때?", "a": "먼저 말을 걸며 분위기를 주도한다", "b": "누군가 말을 걸어주기를 기다린다"},
    {"type": "SN", "q": "어떤 문제를 해결할 때 선호하는 방식은?", "a": "나의 과거 경험과 검증된 데이터", "b": "새로운 아이디어와 나의 직관"},
    {"type": "TF", "q": "더 듣기 좋은 칭찬은?", "a": "너 진짜 일 잘한다, 똑똑해!", "b": "너랑 있으면 마음이 편해, 고마워"},
    {"type": "JP", "q": "과제를 끝내는 스타일은?", "a": "미리미리 조금씩 해서 마감 전 완료", "b": "마감 직전의 몰입감이 주는 짜릿함으로 완료"},
    {"type": "EI", "q": "모임이 끝나고 집에 갈 때 나의 기분은?", "a": "재밌었다! 내일 또 놀고 싶어", "b": "즐거웠지만 이제 빨리 혼자 쉬고 싶어"},
    {"type": "SN", "q": "영화를 볼 때 더 집중하는 부분은?", "a": "눈에 보이는 화려한 영상미와 액션", "b": "영화 속에 숨겨진 상징과 복선"},
    {"type": "TF", "q": "비판을 들었을 때 나의 반응은?", "a": "비판 내용이 논리적으로 맞는지 따져본다", "b": "나에게 그런 말을 한 상대방에게 상처받는다"},
    {"type": "JP", "q": "준비물을 챙길 때?", "a": "리스트를 만들어서 하나씩 체크한다", "b": "대충 챙기고 빠진 건 가서 사면 된다고 생각한다"}
]

# 결과 데이터
RESULTS = {
    "ISTJ": {"title": "청렴결백한 논리주의자", "theme": "미니멀리즘 워크스페이스", "desc": "차분하고 정돈된 모노톤의 무드"},
    "ISFJ": {"title": "용감한 수호자", "theme": "따뜻한 코티지 코어", "desc": "부드러운 햇살과 꽃무늬 패턴의 아늑한 무드"},
    "INFJ": {"title": "선의의 옹호자", "theme": "몽환적인 새벽 안개", "desc": "깊이 있고 신비로운 연보랏빛 무드"},
    "INTJ": {"title": "용의주도한 전략가", "theme": "모던 클래식 라이브러리", "desc": "지적인 분위기의 짙은 우드와 블랙 무드"},
    "ISTP": {"title": "만능 재주꾼", "theme": "빈티지 가라지(Garage)", "desc": "날 것 그대로의 인더스트리얼 무드"},
    "ISFP": {"title": "호기심 많은 예술가", "theme": "수채화가 그려진 캔버스", "desc": "다양한 파스텔 컬러가 섞인 감성 무드"},
    "INFP": {"title": "열정적인 중재자", "theme": "비밀스러운 숲 속 정원", "desc": "초록빛 싱그러움과 동화 같은 무드"},
    "INTP": {"title": "논리적인 사색가", "theme": "우주와 별의 궤적", "desc": "무한한 상상력을 자극하는 네이비 무드"},
    "ESTP": {"title": "모험을 즐기는 사업가", "theme": "활기찬 네온 스트릿", "desc": "에너지 넘치고 강렬한 컬러풀 무드"},
    "ESFP": {"title": "자유로운 영혼의 연예인", "theme": "반짝이는 여름 바다", "desc": "청량하고 시원한 에메랄드빛 무드"},
    "ENFP": {"title": "재기발랄한 활동가", "theme": "무지개 빛 페스티벌", "desc": "통통 튀는 밝고 화사한 멀티 컬러 무드"},
    "ENTP": {"title": "뜨거운 논쟁을 즐기는 변론가", "theme": "사이버펑크 연구소", "desc": "기발하고 독창적인 퓨처리스틱 무드"},
    "ESTJ": {"title": "엄격한 관리자", "theme": "세련된 시티 뷰 오피스", "desc": "깔끔하고 전문적인 도시의 무드"},
    "ESFJ": {"title": "사교적인 외교관", "theme": "디저트 가득한 홈파티", "desc": "달콤하고 화기애애한 웜톤 무드"},
    "ENFJ": {"title": "정의로운 사회운동가", "theme": "황금빛 노을 아래 광장", "desc": "모두를 포용하는 따뜻한 골드 무드"},
    "ENTJ": {"title": "대담한 통솔자", "theme": "럭셔리 펜트하우스 라운지", "desc": "카리스마 있고 세련된 대리석 무드"},
}

# 3. 상태 관리 (Session State)
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'scores' not in st.session_state:
    st.session_state.scores = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}

def select_answer(choice, q_type):
    if choice == 'a':
        st.session_state.scores[q_type] += 1
    else:
        st.session_state.scores[q_type] -= 1
    st.session_state.step += 1

# 4. 앱 화면 구성
st.title("나의 감성 MBTI 테스트 🌸")

if st.session_state.step < len(QUESTIONS):
    # 진행도 표시
    progress = st.session_state.step / len(QUESTIONS)
    st.progress(progress)
    
    # 질문 출력
    q_data = QUESTIONS[st.session_state.step]
    st.markdown(f'<p class="question-text">{q_data["q"]}</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(q_data["a"]):
            select_answer('a', q_data["type"])
            st.rerun()
    with col2:
        if st.button(q_data["b"]):
            select_answer('b', q_data["type"])
            st.rerun()
            
else:
    # 결과 계산
    res = st.session_state.scores
    mbti = ""
    mbti += "E" if res["EI"] >= 0 else "I"
    mbti += "S" if res["SN"] >= 0 else "N"
    mbti += "T" if res["TF"] >= 0 else "F"
    mbti += "J" if res["JP"] >= 0 else "P"
    
    result_data = RESULTS[mbti]
    
    # 결과 출력
    st.markdown(f"""
    <div class="result-card">
        <p style="font-size: 14px; color: #888; letter-spacing: 2px;">YOUR PERSONALITY TYPE</p>
        <h1 style="font-size: 60px; margin-top: 0;">{mbti}</h1>
        <h3 style="color: #444;">{result_data['title']}</h3>
        <hr style="border: 0.5px solid #eee; margin: 20px 0;">
        <p style="color: #666; font-size: 15px;">{result_data['desc']}</p>
        <div style="background-color: #fff9fa; padding: 20px; border-radius: 20px; border: 1px dashed #f8bbd0; margin-top: 20px;">
            <p style="font-weight: bold; color: #d81b60; margin-bottom: 5px;">🎨 추천 이미지 테마</p>
            <p style="font-size: 20px; color: #333;">{result_data['theme']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("테스트 다시하기"):
        st.session_state.step = 0
        st.session_state.scores = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
        st.rerun()

st.markdown("<br><p style='text-align: center; color: #ccc; font-size: 10px;'>Developed with S
