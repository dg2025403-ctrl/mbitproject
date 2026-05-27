import streamlit as st
import numpy as np
import random
import time

# 페이지 설정
st.set_page_config(
    page_title="🐍 스네이크 게임",
    page_icon="🐍",
    layout="centered"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3em;
        background: linear-gradient(45deg, #6BCB77, #4D96FF, #FFD93D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        padding: 10px;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
    .score-box {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFC2D1 100%);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        font-size: 1.3em;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .stButton button {
        width: 100%;
        height: 60px;
        font-size: 1.5em;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 헤더
st.markdown('<div class="main-title">🐍 스네이크 게임 🎮</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">🍎 사과를 먹고 뱀을 길게 키워보세요! 🌟</div>', unsafe_allow_html=True)

# 게임 설정
BOARD_SIZE = 15
EMOJI_EMPTY = "⬛"
EMOJI_SNAKE_HEAD = "🟢"
EMOJI_SNAKE_BODY = "🟩"
EMOJI_FOOD = "🍎"
EMOJI_WALL = "🟫"

# 세션 상태 초기화
def init_game():
    st.session_state.snake = [(7, 7), (7, 6), (7, 5)]  # (row, col)
    st.session_state.direction = "RIGHT"
    st.session_state.food = generate_food(st.session_state.snake)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.high_score = st.session_state.get('high_score', 0)

def generate_food(snake):
    """뱀이 없는 위치에 음식 생성"""
    while True:
        food = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
        if food not in snake:
            return food

def move_snake():
    """뱀을 한 칸 이동"""
    if st.session_state.game_over:
        return
    
    head = st.session_state.snake[0]
    direction = st.session_state.direction
    
    if direction == "UP":
        new_head = (head[0] - 1, head[1])
    elif direction == "DOWN":
        new_head = (head[0] + 1, head[1])
    elif direction == "LEFT":
        new_head = (head[0], head[1] - 1)
    else:  # RIGHT
        new_head = (head[0], head[1] + 1)
    
    # 벽 충돌 체크
    if (new_head[0] < 0 or new_head[0] >= BOARD_SIZE or 
        new_head[1] < 0 or new_head[1] >= BOARD_SIZE):
        st.session_state.game_over = True
        return
    
    # 자기 몸 충돌 체크
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return
    
    # 뱀 이동
    st.session_state.snake.insert(0, new_head)
    
    # 음식 먹기
    if new_head == st.session_state.food:
        st.session_state.score += 10
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score
        st.session_state.food = generate_food(st.session_state.snake)
    else:
        st.session_state.snake.pop()  # 꼬리 제거

def change_direction(new_direction):
    """방향 전환 (반대 방향은 불가)"""
    opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    if opposites.get(st.session_state.direction) != new_direction:
        st.session_state.direction = new_direction

def render_board():
    """게임 보드를 이모지로 렌더링"""
    board = [[EMOJI_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    # 음식 표시
    fr, fc = st.session_state.food
    board[fr][fc] = EMOJI_FOOD
    
    # 뱀 표시
    for i, (r, c) in enumerate(st.session_state.snake):
        if i == 0:
            board[r][c] = EMOJI_SNAKE_HEAD
        else:
            board[r][c] = EMOJI_SNAKE_BODY
    
    # 보드 문자열 생성
    board_str = "\n".join("".join(row) for row in board)
    return board_str

# 게임 초기화
if 'snake' not in st.session_state:
    init_game()

# 점수 표시
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="score-box">🏆 점수: {st.session_state.score}</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="score-box">⭐ 최고점: {st.session_state.high_score}</div>', unsafe_allow_html=True)

st.markdown("---")

# 게임 보드 표시
board_placeholder = st.empty()
board_str = render_board()
board_placeholder.markdown(
    f"<div style='font-size:25px; line-height:1; text-align:center; letter-spacing:-2px; font-family:monospace;'>{board_str.replace(chr(10), '<br>')}</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# 게임 오버 메시지
if st.session_state.game_over:
    st.error(f"💥 게임 오버! 최종 점수: {st.session_state.score}점 💥")
    if st.button("🔄 다시 시작하기!", use_container_width=True):
        init_game()
        st.rerun()
else:
    # 방향 조작 버튼
    st.markdown("### 🎮 방향을 선택하세요!")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⬆️ 위", key="up"):
            change_direction("UP")
            move_snake()
            st.rerun()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ 왼쪽", key="left"):
            change_direction("LEFT")
            move_snake()
            st.rerun()
    with col2:
        if st.button("🍎 직진", key="forward"):
            move_snake()
            st.rerun()
    with col3:
        if st.button("➡️ 오른쪽", key="right"):
            change_direction("RIGHT")
            move_snake()
            st.rerun()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⬇️ 아래", key="down"):
            change_direction("DOWN")
            move_snake()
            st.rerun()
    
    st.markdown("---")
    
    # 자동 진행 모드
    st.markdown("### 🤖 자동 진행 모드")
    auto_play = st.checkbox("자동으로 직진하기 (방향만 바꿔주세요!)")
    speed = st.slider("⚡ 속도", 0.1, 1.0, 0.5, 0.1)
    
    if auto_play and not st.session_state.game_over:
        time.sleep(speed)
        move_snake()
        st.rerun()

# 게임 설명
with st.expander("📖 게임 방법"):
    st.markdown("""
    ### 🎯 게임 규칙
    - 🟢 **초록 머리**가 뱀의 머리예요!
    - 🍎 **사과**를 먹으면 10점을 얻고 뱀이 길어져요!
    - 🟫 **벽**에 부딪히면 게임 오버! 💥
    - 🐍 **자기 몸**에 부딪혀도 게임 오버! 😱
    
    ### 🎮 조작법
    - **방향 버튼**: 뱀의 방향을 바꿔요
    - **직진 버튼**: 현재 방향으로 한 칸 이동
    - **자동 진행**: 체크하면 자동으로 움직여요!
    """)

# 푸터
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#aaa; padding:20px;">
        Made with 💚 for 당곡고 학생들 | 🎓 재미있게 플레이하세요!
    </div>
""", unsafe_allow_html=True)
