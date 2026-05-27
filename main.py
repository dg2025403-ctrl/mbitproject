import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="MBTI 포켓몬 매칭 ✨",
    page_icon="⚡",
    layout="centered"
)

# MBTI별 포켓몬 데이터
mbti_pokemon = {
    "INTJ": {
        "name": "뮤츠",
        "emoji": "🧠💜",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "description": "전략가이자 천재! 뮤츠는 강력한 지능과 독립적인 성격을 가진 INTJ와 닮았어요. 깊은 사색을 즐기는 당신과 완벽한 짝! 🎯",
        "traits": ["🧩 전략적", "🔮 직관적", "🎯 목표지향"]
    },
    "INTP": {
        "name": "폴리곤2",
        "emoji": "🤖💡",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/233.png",
        "description": "논리와 분석의 화신! 폴리곤2는 끊임없이 진화하며 새로운 지식을 탐구하는 INTP와 찰떡! 🔬",
        "traits": ["🔍 분석적", "💭 호기심왕", "🧪 탐구형"]
    },
    "ENTJ": {
        "name": "리자몽",
        "emoji": "🔥👑",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "description": "타고난 리더! 리자몽의 카리스마와 강력한 추진력은 ENTJ 그 자체! 하늘을 지배하는 당신! 🏆",
        "traits": ["👑 리더십", "🔥 추진력", "⚔️ 도전적"]
    },
    "ENTP": {
        "name": "겟핸보숭",
        "emoji": "🐵✨",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/424.png",
        "description": "재치만점 토론왕! 영리하고 장난기 가득한 겟핸보숭은 자유로운 영혼 ENTP와 환상의 콤비! 🎪",
        "traits": ["💡 창의적", "🎭 재치만점", "🚀 모험가"]
    },
    "INFJ": {
        "name": "에브이",
        "emoji": "🦊🌙",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/197.png",
        "description": "신비롭고 깊이있는 영혼! 달빛 아래 빛나는 에브이는 통찰력 있는 INFJ와 운명의 짝! 🌌",
        "traits": ["🌙 통찰력", "💫 신비로움", "🤝 공감능력"]
    },
    "INFP": {
        "name": "이브이",
        "emoji": "🐾💖",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "description": "무한한 가능성을 품은 순수한 영혼! 이브이는 따뜻하고 이상주의적인 INFP에게 딱! 💝",
        "traits": ["💝 이상주의", "🌈 다재다능", "🕊️ 순수함"]
    },
    "ENFJ": {
        "name": "행복",
        "emoji": "💕🥰",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/242.png",
        "description": "모두에게 행복을 전하는 따뜻한 친구! 행복은 사람들을 이끌고 보살피는 ENFJ와 완벽한 매치! 🌟",
        "traits": ["💖 따뜻함", "🤗 친화력", "✨ 영감을줌"]
    },
    "ENFP": {
        "name": "피카츄",
        "emoji": "⚡🌟",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "description": "에너지 폭발 ⚡ 밝고 사교적인 피카츄는 열정 가득한 ENFP의 영혼 친구! 모두를 즐겁게 해요! 🎉",
        "traits": ["⚡ 에너지", "🎉 열정적", "🌈 사교적"]
    },
    "ISTJ": {
        "name": "거북왕",
        "emoji": "🐢🛡️",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "description": "신뢰감 그 자체! 든든하고 책임감 강한 거북왕은 성실한 ISTJ의 모습 그대로! 🏰",
        "traits": ["🛡️ 책임감", "📋 체계적", "💎 신뢰감"]
    },
    "ISFJ": {
        "name": "잠만보",
        "emoji": "😴🍙",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png",
        "description": "푸근하고 따뜻한 수호자! 잠만보처럼 든든하게 주변을 지키는 ISFJ! 평화로운 매력! 🌸",
        "traits": ["🤗 따뜻함", "🛌 안정감", "🌷 헌신적"]
    },
    "ESTJ": {
        "name": "나시",
        "emoji": "🌴📊",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/103.png",
        "description": "체계와 질서의 수호자! 나시처럼 단단하게 자신의 자리를 지키는 ESTJ! 관리자 끝판왕! 📈",
        "traits": ["📊 조직력", "⚖️ 원칙주의", "💼 실용적"]
    },
    "ESFJ": {
        "name": "푸린",
        "emoji": "🎤💗",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "description": "모두를 잠재우는 노래의 마법사! 사람들과 어울리기 좋아하는 푸린은 사교적인 ESFJ와 짝꿍! 🎵",
        "traits": ["🎵 사교적", "💗 배려심", "🌟 인기쟁이"]
    },
    "ISTP": {
        "name": "루카리오",
        "emoji": "🥋⚔️",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "description": "차분하고 강한 무도가! 파동을 읽는 루카리오는 관찰력 뛰어난 ISTP의 멋진 파트너! 🌀",
        "traits": ["🎯 집중력", "🛠️ 손재주", "🧘 차분함"]
    },
    "ISFP": {
        "name": "이상해꽃",
        "emoji": "🌸🌿",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png",
        "description": "조용한 예술가의 영혼! 자연과 어우러진 이상해꽃은 감성 넘치는 ISFP와 완벽한 조화! 🎨",
        "traits": ["🎨 예술적", "🌿 자연친화", "💐 온화함"]
    },
    "ESTP": {
        "name": "켄타로스",
        "emoji": "🐂💨",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/128.png",
        "description": "거침없는 모험가! 폭주하는 에너지의 켄타로스는 행동파 ESTP와 환상의 짝! 🏇",
        "traits": ["💨 행동파", "🔥 대담함", "🎯 즉흥적"]
    },
    "ESFP": {
        "name": "라이츄",
        "emoji": "⚡🎉",
        "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png",
        "description": "파티의 주인공! 활기차고 분위기 메이커인 라이츄는 흥 많은 ESFP의 베스트 프렌드! 🎊",
        "traits": ["🎉 흥부자", "✨ 활발함", "🎭 매력만점"]
    }
}

# 커스텀 CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3em;
        background: linear-gradient(45deg, #FF6B9D, #FEC8D8, #FFD93D, #6BCB77);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        padding: 20px;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .pokemon-card {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D1 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .trait-badge {
        display: inline-block;
        background: white;
        color: #FF6B9D;
        padding: 8px 16px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-title">✨ MBTI 포켓몬 매칭 ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🎮 당신의 MBTI에 어울리는 포켓몬을 찾아보세요! 🎮</div>', unsafe_allow_html=True)

st.markdown("---")

# MBTI 선택
st.markdown("### 🔮 당신의 MBTI를 선택해주세요!")

col1, col2 = st.columns(2)
with col1:
    ei = st.radio("🌟 에너지 방향", ["E (외향) 🎉", "I (내향) 🌙"], horizontal=True)
    sn = st.radio("🔍 인식 방식", ["S (감각) 👀", "N (직관) 💫"], horizontal=True)
with col2:
    tf = st.radio("💭 판단 방식", ["T (사고) 🧠", "F (감정) 💖"], horizontal=True)
    jp = st.radio("📅 생활 양식", ["J (계획) 📋", "P (즉흥) 🎲"], horizontal=True)

# MBTI 조합
mbti = ei[0] + sn[0] + tf[0] + jp[0]

st.markdown("---")

# 결과 보기 버튼
if st.button("🎁 내 포켓몬 파트너 찾기!", use_container_width=True):
    pokemon = mbti_pokemon[mbti]
    
    st.balloons()
    
    st.markdown(f"### 🎊 당신의 MBTI는 **{mbti}** 입니다!")
    
    st.markdown(f"""
        <div class="pokemon-card">
            <h2>{pokemon['emoji']} {pokemon['name']} {pokemon['emoji']}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 포켓몬 이미지
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(pokemon['image'], use_container_width=True)
    
    # 설명
    st.markdown(f"#### 💌 {pokemon['description']}")
    
    # 특성 배지
    st.markdown("#### ✨ 당신과 포켓몬의 공통 매력 ✨")
    traits_html = ""
    for trait in pokemon['traits']:
        traits_html += f'<span class="trait-badge">{trait}</span>'
    st.markdown(f'<div style="text-align:center;">{traits_html}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.success(f"🌈 {pokemon['name']}와 함께 멋진 모험을 떠나보세요! 🚀")

# 푸터
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#aaa; padding:20px;">
        Made with 💖 for 당곡고 학생들 | 🎓 재미있게 즐겨주세요!
    </div>
""", unsafe_allow_html=True)
