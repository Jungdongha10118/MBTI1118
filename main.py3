import streamlit as st
import time

# --- 1. 페이지 설정 및 디자인 (CSS) ---
st.set_page_config(page_title="나의 감성 MBTI 찾기", page_icon="🌸", layout="centered")

# 파스텔 톤 CSS 스타일 적용
st.markdown("""
    <style>
    /* 전체 배경색 - 부드러운 크림색 */
    .stApp {
        background-color: #FFFDF9;
        color: #5D5C61;
    }
    
    /* 제목 스타일 */
    h1 {
        font-family: 'Gamja Flower', sans-serif;
        color: #938F96;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 버튼 스타일 커스터마이징 */
    div.stButton > button {
        width: 100%;
        background-color: #E2F0CB; /* 파스텔 민트 */
        color: #5D5C61;
        border: none;
        border-radius: 15px;
        padding: 15px 20px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    div.stButton > button:hover {
        background-color: #FFB7B2; /* 파스텔 핑크 (호버 시) */
        color: white;
        transform: translateY(-2px);
    }

    /* 진행바 색상 변경 */
    div.stProgress > div > div > div > div {
        background-color: #FFB7B2;
    }

    /* 텍스트 박스 스타일 */
    .question-box {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 30px;
        font-size: 22px;
        font-weight: 600;
        color: #6D6875;
    }
    
    .result-card {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #E2F0CB;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    </style>
    
    <!-- 구글 폰트 로드 (감성적인 폰트) -->
    <link href="https://fonts.googleapis.com/css2?family=Gamja+Flower&family=Nanum+Pen+Script&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# --- 2. 데이터 (질문 및 결과) ---

# 질문 리스트 (총 12개: E/I, S/N, T/F, J/P 순환)
# type: 점수를 더할 지표 (예: 'E'를 선택하면 E 점수 +1)
questions = [
    # 1. E vs I
    {"q": "오랜만에 찾아온 주말, 당신의 선택은?", 
     "a": "친구들과 핫플레이스에서 브런치!", "a_type": "E",
     "b": "집에서 좋아하는 영화 보며 뒹굴뒹굴.", "b_type": "I"},
    
    # 2. S vs N
    {"q": "멍하니 창밖을 바라볼 때 드는 생각은?", 
     "a": "저 사람 옷 예쁘네.. 오늘 날씨 좋다.", "a_type": "S",
     "b": "저 구름은 솜사탕 같아.. 내가 만약 구름이라면?", "b_type": "N"},
    
    # 3. T vs F
    {"q": "친구가 우울해서 머리를 잘랐다고 한다. 당신의 반응은?", 
     "a": "왜 우울해? 무슨 일 있어?", "a_type": "T",
     "b": "머리 자르니까 기분 전환 됐어? 너무 잘 어울린다!", "b_type": "F"},
     
    # 4. J vs P
    {"q": "여행을 떠나기 전날 밤, 당신의 모습은?", 
     "a": "분 단위 엑셀 계획표와 짐 싸기 완료.", "a_type": "J",
     "b": "일단 여권이랑 지갑만 챙기자! 나머진 가서 해결.", "b_type": "P"},
     
    # 5. E vs I
    {"q": "새로운 모임에 나갔을 때 나는?", 
     "a": "먼저 말을 걸고 분위기를 주도한다.", "a_type": "E",
     "b": "구석에서 조용히 분위기를 살핀다.", "b_type": "I"},
     
    # 6. S vs N
    {"q": "맛집을 찾을 때 더 신뢰하는 것은?", 
     "a": "실제 방문자 리뷰와 별점 데이터.", "a_type": "S",
     "b": "가게의 분위기와 나의 직감.", "b_type": "N"},
     
    # 7. T vs F
    {"q": "친구가 나에게 서운함을 토로할 때?", 
     "a": "내가 잘못한 부분에 대해 논리적으로 분석한다.", "a_type": "T",
     "b": "일단 친구의 마음에 공감하고 사과한다.", "b_type": "F"},
     
    # 8. J vs P
    {"q": "일을 시작하기 전에 나는?", 
     "a": "체계적인 순서와 마감 기한을 정한다.", "a_type": "J",
     "b": "일단 중요한 것부터 손에 잡히는 대로 시작한다.", "b_type": "P"},
     
    # 9. E vs I
    {"q": "일주일 동안 사람을 만나지 못했다면?", 
     "a": "너무 심심하고 에너지가 빠진다.", "a_type": "E",
     "b": "오히려 좋아, 재충전의 시간이다.", "b_type": "I"},
     
    # 10. S vs N
    {"q": "영화를 보고 난 후 주로 하는 말은?", 
     "a": "주인공 연기가 대박이었어. CG가 리얼하던데?", "a_type": "S",
     "b": "결말의 의미가 뭘까? 감독의 의도는...", "b_type": "N"},
     
    # 11. T vs F
    {"q": "고민 상담을 해줄 때 더 중요하게 생각하는 것은?", 
     "a": "현실적인 해결책 제시.", "a_type": "T",
     "b": "따뜻한 위로와 경청.", "b_type": "F"},
     
    # 12. J vs P
    {"q": "갑작스러운 일정 변경이 생겼을 때?", 
     "a": "스트레스 받는다. 계획이 틀어졌어!", "a_type": "J",
     "b": "오케이, 오히려 색다른 경험이 될 수도?", "b_type": "P"}
]

# 결과 데이터 (16개 유형)
mbti_results = {
    "ISTJ": {"animal": "성실한 거북이", "desc": "한 번 시작한 일은 끝까지 해내는 책임감 대장.", "theme": "차분한 서재와 짙은 우드 톤", "color": "#6D6875"},
    "ISFJ": {"animal": "포근한 코알라", "desc": "뒤에서 묵묵히 챙겨주는 배려의 아이콘.", "theme": "따뜻한 베이지색 담요와 코코아", "color": "#E5B299"},
    "INFJ": {"animal": "신비로운 유니콘", "desc": "조용해 보이지만 속에는 우주를 품고 있는 사람.", "theme": "새벽녘의 보랏빛 안개 숲", "color": "#B5838D"},
    "INTJ": {"animal": "치밀한 호랑이", "desc": "전체를 꿰뚫어 보는 통찰력 있는 전략가.", "theme": "차가운 도시의 밤하늘과 별", "color": "#2B2D42"},
    "ISTP": {"animal": "만능 재주꾼 고양이", "desc": "효율성을 중시하며 상황 파악이 빠른 현실주의자.", "theme": "빈티지 공방과 그레이 톤", "color": "#8D99AE"},
    "ISFP": {"animal": "자유로운 나무늘보", "desc": "누워있는게 제일 좋아. 하지만 감수성은 풍부해.", "theme": "햇살이 비치는 침대 위", "color": "#FFCDB2"},
    "INFP": {"animal": "꿈꾸는 파랑새", "desc": "마음이 여리고 낭만을 좇는 이상주의자.", "theme": "동화 속 파스텔 핑크 구름", "color": "#FFB7B2"},
    "INTP": {"animal": "호기심 많은 부엉이", "desc": "남들이 보지 못하는 관점으로 세상을 분석하는 천재.", "theme": "깊은 밤의 도서관", "color": "#3D405B"},
    "ESTP": {"animal": "활동적인 치타", "desc": "스릴을 즐기며 문제를 즉각적으로 해결하는 해결사.", "theme": "에너지 넘치는 네온 사인", "color": "#E07A5F"},
    "ESFP": {"animal": "재주 넘치는 돌고래", "desc": "주변 사람들을 즐겁게 만드는 분위기 메이커.", "theme": "반짝이는 여름 바다", "color": "#4ECDC4"},
    "ENFP": {"animal": "해피 바이러스 강아지", "desc": "열정이 넘치고 상상력이 풍부한 인간 스파크.", "theme": "무지개와 놀이공원", "color": "#F7D794"},
    "ENTP": {"animal": "재치 있는 여우", "desc": "지루한 건 질색! 끊임없이 새로운 것에 도전하는 논쟁가.", "theme": "톡톡 튀는 팝아트 갤러리", "color": "#FF6B6B"},
    "ESTJ": {"animal": "엄격한 사자", "desc": "규칙을 준수하고 사람들을 이끄는 리더.", "theme": "깔끔하게 정돈된 오피스", "color": "#343A40"},
    "ESFJ": {"animal": "다정한 펭귄", "desc": "사람들을 돕는 것을 좋아하고 조화를 중시하는 평화주의자.", "theme": "화사한 봄날의 피크닉", "color": "#FAD02E"},
    "ENFJ": {"animal": "정의로운 골든리트리버", "desc": "타인의 성장을 도우며 리더십을 발휘하는 언변가.", "theme": "따스한 모닥불과 캠핑", "color": "#E5989B"},
    "ENTJ": {"animal": "카리스마 독수리", "desc": "비전을 가지고 목표를 향해 돌진하는 대담한 지도자.", "theme": "세련된 마천루의 야경", "color": "#1D3557"},
}

# --- 3. 로직 함수 ---

def init_session():
    """세션 상태 초기화"""
    if 'current_q' not in st.session_state:
        st.session_state.current_q = 0
        st.session_state.score = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
        st.session_state.finished = False

def calculate_mbti():
    """점수를 바탕으로 MBTI 문자열 생성"""
    score = st.session_state.score
    mbti = ""
    mbti += "E" if score['E'] >= score['I'] else "I"
    mbti += "S" if score['S'] >= score['N'] else "N"
    mbti += "T" if score['T'] >= score['F'] else "F"
    mbti += "J" if score['J'] >= score['P'] else "P"
    return mbti

def next_question(selected_type):
    """다음 질문으로 넘어가고 점수 기록"""
    # 선택한 타입 점수 증가
    st.session_state.score[selected_type] += 1
    
    # 마지막 질문이 아니면 인덱스 증가
    if st.session_state.current_q < len(questions) - 1:
        st.session_state.current_q += 1
    else:
        st.session_state.finished = True
    
    # 리렌더링 (Streamlit 특성상 자동이지만 명시적으로)
    st.rerun()

def restart_test():
    """테스트 다시 시작"""
    st.session_state.current_q = 0
    st.session_state.score = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    st.session_state.finished = False
    st.rerun()

# --- 4. 메인 UI 렌더링 ---

init_session()

# 헤더
st.title("🌸 감성 MBTI 테스트")
st.markdown("<p style='text-align: center; color: #888;'>당신의 마음속 색깔을 찾아보세요</p>", unsafe_allow_html=True)
st.write("---")

# 퀴즈 진행 중
if not st.session_state.finished:
    q_idx = st.session_state.current_q
    question = questions[q_idx]
    
    # 진행바
    progress = (q_idx + 1) / len(questions)
    st.progress(progress)
    st.caption(f"Question {q_idx + 1} / {len(questions)}")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # 질문 박스
    st.markdown(f"<div class='question-box'>{question['q']}</div>", unsafe_allow_html=True)
    
    # 답변 버튼 (2열 배치)
    col1, col2 = st.columns(2)
    
    # 버튼 클릭 시 콜백 함수 호출을 피하고 직접 로직 처리 (레이아웃 이슈 방지)
    with col1:
        if st.button(question['a']):
            next_question(question['a_type'])
    with col2:
        if st.button(question['b']):
            next_question(question['b_type'])

# 결과 화면
else:
    result_mbti = calculate_mbti()
    data = mbti_results[result_mbti]
    
    with st.spinner('당신의 감성을 분석하고 있습니다...'):
        time.sleep(1.5)
    
    st.balloons()
    
    st.markdown(f"""
    <div class='result-card'>
        <h2 style='color: {data['color']}; margin-bottom: 10px;'>{result_mbti}</h2>
        <h3 style='margin-bottom: 20px;'>{data['animal']}</h3>
        <p style='font-size: 18px; margin-bottom: 30px;'>{data['desc']}</p>
        <hr style='border-top: 1px dashed #bbb; margin: 20px 0;'>
        <h4 style='color: #666;'>🎨 추천 이미지 테마</h4>
        <div style='background-color: {data['color']}20; padding: 15px; border-radius: 10px; margin-top: 10px;'>
            <strong style='color: {data['color']}; font-size: 20px;'>{data['theme']}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    if st.button("🔄 다시 테스트하기"):
        restart_test()
