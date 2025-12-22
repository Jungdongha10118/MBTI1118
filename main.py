# app.py
import streamlit as st

# ----------------------
# Page Config
# ----------------------
st.set_page_config(
    page_title="MBTI test",
    page_icon="🎀",
    layout="centered"
)

# ----------------------
# Soft Pastel UI
# ----------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(180deg, #fdfbfb 0%, #f7f6ff 100%);
    }
    .card {
        background: #ffffff;
        padding: 28px;
        border-radius: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 40px;
    }
    .result-card {
        background: #fff7fb;
        padding: 36px;
        border-radius: 28px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Question Data
# (MBTI letters hidden from user)
# ----------------------
QUESTIONS = [
    ("사람들과 함께 있으면 기분이 더 살아난다",
     "사람들과 어울리는 게 좋다",
     "혼자만의 시간이 더 편하다",
     "E", "I"),

    ("새로운 사람에게 먼저 말을 거는 편이다",
     "자연스럽게 먼저 다가간다",
     "상대가 다가와주길 기다린다",
     "E", "I"),

    ("정보를 받아들일 때 더 끌리는 건",
     "지금 보이고 느껴지는 것",
     "의미나 가능성",
     "S", "N"),

    ("아이디어를 떠올릴 때",
     "현실적인 방법부터 생각한다",
     "상상부터 펼쳐본다",
     "S", "N"),

    ("결정을 내릴 때 더 중요한 건",
     "이유와 기준",
     "사람의 마음",
     "T", "F"),

    ("갈등 상황에서 나는",
     "문제 해결이 우선이다",
     "감정이 상하지 않게 한다",
     "T", "F"),

    ("하루를 보낼 때",
     "계획이 있으면 마음이 편하다",
     "흐름에 맡기는 게 좋다",
     "J", "P"),

    ("약속이 생기면",
     "미리 준비해둔다",
     "그때 가서 생각한다",
     "J", "P"),

    ("여행 스타일은",
     "일정이 있는 여행",
     "즉흥적인 여행",
     "J", "P"),

    ("생각이 정리될 때는",
     "말하거나 글로 풀 때",
     "혼자 곱씹을 때",
     "E", "I"),

    ("새로운 아이디어를 들으면",
     "실현 가능한지 본다",
     "확장해보고 싶다",
     "S", "N"),

    ("누군가 고민을 말할 때",
     "해결책을 제시한다",
     "공감부터 한다",
     "T", "F"),
]

# ----------------------
# Result Theme
# ----------------------
THEMES = {
    "ENFP": ("🌈 자유로운 파스텔", "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"),
    "INFJ": ("🌙 고요한 밤", "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429"),
    "INTJ": ("🧊 미니멀 블루", "https://images.unsplash.com/photo-1496307042754-b4aa456c4a2d"),
    "ISFP": ("🎨 감성 아트", "https://images.unsplash.com/photo-1526318472351-c75fcf070305"),
    "ESFJ": ("🌸 따뜻한 꽃", "https://images.unsplash.com/photo-1490750967868-88aa4486c946"),
}

# ----------------------
# Title
# ----------------------
st.markdown('<div class="title">MBTI Test</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">당신의 분위기를 알아보는 12가지 질문</div>', unsafe_allow_html=True)

# ----------------------
# Session
# ----------------------
if "answers" not in st.session_state:
    st.session_state.answers = {}

# ----------------------
# Questions UI
# ----------------------
for i, (q, opt1, opt2, v1, v2) in enumerate(QUESTIONS):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**Q{i+1}. {q}**")
    st.session_state.answers[i] = st.radio(
        "",
        [opt1, opt2],
        index=None,
        key=f"q{i}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# Result
# ----------------------
if st.button("결과 확인하기 🎀"):
    score = {k: 0 for k in "EISNTFJP"}

    for i, (_, opt1, opt2, v1, v2) in enumerate(QUESTIONS):
        if st.session_state[f"q{i}"] == opt1:
            score[v1] += 1
        elif st.session_state[f"q{i}"] == opt2:
            score[v2] += 1

    mbti = (
        ("E" if score["E"] >= score["I"] else "I") +
        ("S" if score["S"] >= score["N"] else "N") +
        ("T" if score["T"] >= score["F"] else "F") +
        ("J" if score["J"] >= score["P"] else "P")
    )

    theme, img = THEMES.get(
        mbti,
        ("🌼 부드러운 파스텔", "https://images.unsplash.com/photo-1500534623283-312aade485b7")
    )

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.subheader(f"당신의 MBTI는 **{mbti}**")
    st.write(f"어울리는 분위기: **{theme}**")
    st.image(img, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

