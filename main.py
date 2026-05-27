import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="🐍 스네이크 게임",
    page_icon="🐍",
    layout="centered"
)

# 헤더 스타일
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3em;
        background: linear-gradient(45deg, #4CAF50, #8BC34A, #CDDC39);
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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🐍 스네이크 게임 🍎</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">⌨️ 방향키 또는 WASD로 조작! 스페이스바로 시작! 🎮</div>', unsafe_allow_html=True)

# 게임 HTML/CSS/JavaScript
game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%);
        min-height: 600px;
        font-family: 'Arial', sans-serif;
        padding: 20px;
    }
    
    .game-container {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        text-align: center;
    }
    
    .score-board {
        display: flex;
        justify-content: space-around;
        margin-bottom: 15px;
        gap: 20px;
    }
    
    .score-item {
        background: linear-gradient(135deg, #ffeaa7, #fab1a0);
        padding: 10px 20px;
        border-radius: 12px;
        font-size: 1.2em;
        font-weight: bold;
        color: #2d3436;
        min-width: 120px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    canvas {
        background: #aad751;
        border-radius: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
        display: block;
    }
    
    .controls {
        margin-top: 15px;
        color: #636e72;
        font-size: 0.95em;
    }
    
    .game-message {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(45, 52, 54, 0.95);
        color: white;
        padding: 30px 50px;
        border-radius: 20px;
        font-size: 1.5em;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        display: none;
        z-index: 100;
    }
    
    .game-message.show {
        display: block;
        animation: popIn 0.3s ease-out;
    }
    
    @keyframes popIn {
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }
    
    .canvas-wrapper {
        position: relative;
        display: inline-block;
    }
    
    .btn {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-size: 1.1em;
        font-weight: bold;
        cursor: pointer;
        margin-top: 15px;
        box-shadow: 0 5px 15px rgba(108, 92, 231, 0.4);
        transition: all 0.2s;
    }
    
    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(108, 92, 231, 0.6);
    }
    
    .speed-control {
        margin-top: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    .speed-control label {
        font-weight: bold;
        color: #2d3436;
    }
</style>
</head>
<body>
    <div class="game-container">
        <div class="score-board">
            <div class="score-item">🏆 점수: <span id="score">0</span></div>
            <div class="score-item">⭐ 최고: <span id="highScore">0</span></div>
        </div>
        
        <div class="canvas-wrapper">
            <canvas id="gameCanvas" width="400" height="400"></canvas>
            <div id="gameMessage" class="game-message">
                <div id="messageText">🎮 스페이스바를 눌러 시작!</div>
            </div>
        </div>
        
        <div class="controls">
            ⌨️ <b>방향키</b> 또는 <b>WASD</b>로 이동 | <b>스페이스바</b>로 시작/일시정지
        </div>
        
        <div class="speed-control">
            <label>⚡ 속도:</label>
            <input type="range" id="speedSlider" min="50" max="200" value="120" step="10">
            <span id="speedValue">보통</span>
        </div>
        
        <button class="btn" onclick="resetGame()">🔄 새 게임</button>
    </div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const highScoreEl = document.getElementById('highScore');
const messageEl = document.getElementById('gameMessage');
const messageTextEl = document.getElementById('messageText');
const speedSlider = document.getElementById('speedSlider');
const speedValueEl = document.getElementById('speedValue');

const GRID_SIZE = 20;
const TILE_COUNT = canvas.width / GRID_SIZE;

let snake = [{x: 10, y: 10}];
let velocity = {x: 0, y: 0};
let food = {x: 15, y: 15};
let score = 0;
let highScore = parseInt(localStorage.getItem('snakeHighScore') || '0');
let gameRunning = false;
let gamePaused = false;
let gameOver = false;
let gameSpeed = 120;
let lastTime = 0;
let nextVelocity = {x: 0, y: 0};

highScoreEl.textContent = highScore;

// 속도 슬라이더
speedSlider.addEventListener('input', (e) => {
    gameSpeed = 250 - parseInt(e.target.value);
    if (gameSpeed < 80) speedValueEl.textContent = '🔥 빠름';
    else if (gameSpeed < 130) speedValueEl.textContent = '⚡ 보통';
    else speedValueEl.textContent = '🐢 느림';
});

function generateFood() {
    while (true) {
        food = {
            x: Math.floor(Math.random() * TILE_COUNT),
            y: Math.floor(Math.random() * TILE_COUNT)
        };
        // 뱀 몸과 겹치지 않게
        let onSnake = snake.some(seg => seg.x === food.x && seg.y === food.y);
        if (!onSnake) break;
    }
}

function drawGame() {
    // 배경 - 체크무늬
    for (let i = 0; i < TILE_COUNT; i++) {
        for (let j = 0; j < TILE_COUNT; j++) {
            ctx.fillStyle = (i + j) % 2 === 0 ? '#aad751' : '#a2d149';
            ctx.fillRect(i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE);
        }
    }
    
    // 음식 (사과)
    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.arc(
        food.x * GRID_SIZE + GRID_SIZE/2,
        food.y * GRID_SIZE + GRID_SIZE/2,
        GRID_SIZE/2 - 2,
        0, Math.PI * 2
    );
    ctx.fill();
    // 사과 잎
    ctx.fillStyle = '#27ae60';
    ctx.fillRect(
        food.x * GRID_SIZE + GRID_SIZE/2 - 2,
        food.y * GRID_SIZE + 2,
        4, 5
    );
    
    // 뱀 그리기
    snake.forEach((segment, index) => {
        if (index === 0) {
            // 머리
            ctx.fillStyle = '#4a69bd';
            ctx.fillRect(
                segment.x * GRID_SIZE + 1,
                segment.y * GRID_SIZE + 1,
                GRID_SIZE - 2, GRID_SIZE - 2
            );
            // 눈
            ctx.fillStyle = 'white';
            let eyeOffsetX1, eyeOffsetY1, eyeOffsetX2, eyeOffsetY2;
            if (velocity.x === 1) {
                eyeOffsetX1 = 13; eyeOffsetY1 = 5;
                eyeOffsetX2 = 13; eyeOffsetY2 = 13;
            } else if (velocity.x === -1) {
                eyeOffsetX1 = 3; eyeOffsetY1 = 5;
                eyeOffsetX2 = 3; eyeOffsetY2 = 13;
            } else if (velocity.y === -1) {
                eyeOffsetX1 = 5; eyeOffsetY1 = 3;
                eyeOffsetX2 = 13; eyeOffsetY2 = 3;
            } else {
                eyeOffsetX1 = 5; eyeOffsetY1 = 13;
                eyeOffsetX2 = 13; eyeOffsetY2 = 13;
            }
            ctx.fillRect(segment.x * GRID_SIZE + eyeOffsetX1, segment.y * GRID_SIZE + eyeOffsetY1, 3, 3);
            ctx.fillRect(segment.x * GRID_SIZE + eyeOffsetX2, segment.y * GRID_SIZE + eyeOffsetY2, 3, 3);
        } else {
            // 몸통 - 그라데이션 효과
            const ratio = index / snake.length;
            const r = Math.floor(74 - ratio * 20);
            const g = Math.floor(105 - ratio * 20);
            const b = Math.floor(189 - ratio * 40);
            ctx.fillStyle = `rgb(${r},${g},${b})`;
            ctx.fillRect(
                segment.x * GRID_SIZE + 2,
                segment.y * GRID_SIZE + 2,
                GRID_SIZE - 4, GRID_SIZE - 4
            );
        }
    });
}

function updateGame() {
    // 방향 적용 (180도 회전 방지)
    if (nextVelocity.x !== -velocity.x || nextVelocity.y !== -velocity.y) {
        velocity = {...nextVelocity};
    }
    
    if (velocity.x === 0 && velocity.y === 0) return;
    
    const head = {x: snake[0].x + velocity.x, y: snake[0].y + velocity.y};
    
    // 벽 충돌
    if (head.x < 0 || head.x >= TILE_COUNT || head.y < 0 || head.y >= TILE_COUNT) {
        endGame();
        return;
    }
    
    // 자기 몸 충돌
    if (snake.some(seg => seg.x === head.x && seg.y === head.y)) {
        endGame();
        return;
    }
    
    snake.unshift(head);
    
    // 음식 먹기
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        scoreEl.textContent = score;
        if (score > highScore) {
            highScore = score;
            highScoreEl.textContent = highScore;
            localStorage.setItem('snakeHighScore', highScore);
        }
        generateFood();
    } else {
        snake.pop();
    }
}

function gameLoop(currentTime) {
    if (!gameRunning || gamePaused || gameOver) {
        drawGame();
        return;
    }
    
    if (currentTime - lastTime >= gameSpeed) {
        updateGame();
        lastTime = currentTime;
    }
    
    drawGame();
    requestAnimationFrame(gameLoop);
}

function startGame() {
    if (gameOver) {
        resetGame();
        return;
    }
    if (!gameRunning) {
        gameRunning = true;
        gamePaused = false;
        messageEl.classList.remove('show');
        if (velocity.x === 0 && velocity.y === 0) {
            nextVelocity = {x: 1, y: 0};
        }
        lastTime = performance.now();
        requestAnimationFrame(gameLoop);
    } else {
        gamePaused = !gamePaused;
        if (gamePaused) {
            messageTextEl.innerHTML = '⏸️ 일시정지<br><small>스페이스로 계속</small>';
            messageEl.classList.add('show');
        } else {
            messageEl.classList.remove('show');
            lastTime = performance.now();
            requestAnimationFrame(gameLoop);
        }
    }
}

function endGame() {
    gameRunning = false;
    gameOver = true;
    messageTextEl.innerHTML = `💥 게임 오버!<br>🏆 ${score}점<br><small>스페이스로 다시 시작</small>`;
    messageEl.classList.add('show');
}

function resetGame() {
    snake = [{x: 10, y: 10}];
    velocity = {x: 0, y: 0};
    nextVelocity = {x: 0, y: 0};
    score = 0;
    scoreEl.textContent = 0;
    gameRunning = false;
    gamePaused = false;
    gameOver = false;
    generateFood();
    messageTextEl.innerHTML = '🎮 스페이스바로 시작!<br><small>방향키로 조작</small>';
    messageEl.classList.add('show');
    drawGame();
}

// 키보드 이벤트
document.addEventListener('keydown', (e) => {
    const key = e.key.toLowerCase();
    
    // 스페이스바 - 시작/일시정지
    if (e.key === ' ') {
        e.preventDefault();
        startGame();
        return;
    }
    
    if (!gameRunning || gamePaused || gameOver) return;
    
    // 방향키 + WASD
    if ((e.key === 'ArrowUp' || key === 'w') && velocity.y !== 1) {
        nextVelocity = {x: 0, y: -1};
        e.preventDefault();
    } else if ((e.key === 'ArrowDown' || key === 's') && velocity.y !== -1) {
        nextVelocity = {x: 0, y: 1};
        e.preventDefault();
    } else if ((e.key === 'ArrowLeft' || key === 'a') && velocity.x !== 1) {
        nextVelocity = {x: -1, y: 0};
        e.preventDefault();
    } else if ((e.key === 'ArrowRight' || key === 'd') && velocity.x !== -1) {
        nextVelocity = {x: 1, y: 0};
        e.preventDefault();
    }
});

// 캔버스 클릭 시 포커스
canvas.addEventListener('click', () => {
    canvas.focus();
});

// 초기 화면
generateFood();
drawGame();
messageEl.classList.add('show');

// iframe 포커스 자동 설정
window.focus();
document.body.tabIndex = 0;
document.body.focus();
</script>
</body>
</html>
"""

# 게임 실행
components.html(game_html, height=650)

# 안내 메시지
st.info("💡 **팁**: 게임이 작동하지 않으면 게임 화면을 한 번 **클릭**한 후 키를 눌러주세요!")

# 게임 설명
with st.expander("📖 게임 방법 보기"):
    st.markdown("""
    ### 🎯 게임 규칙
    - 🍎 **빨간 사과**를 먹으면 10점을 얻고 뱀이 길어져요!
    - 🧱 **벽**에 부딪히면 게임 오버! 💥
    - 🐍 **자기 몸**에 부딪혀도 게임 오버! 😱
    
    ### 🎮 조작법
    | 키 | 동작 |
    |---|---|
    | ⬆️ ⬇️ ⬅️ ➡️ 또는 **WASD** | 방향 조작 |
    | **스페이스바** | 시작 / 일시정지 |
    | **속도 슬라이더** | 게임 속도 조절 |
    | **새 게임 버튼** | 게임 리셋 |
    
    ### ✨ 특징
    - 🏆 **최고 점수 저장**: 브라우저에 자동 저장됩니다!
    - 🎨 **체크무늬 보드**: 진짜 구글 스네이크처럼!
    - 👀 **눈이 있는 뱀**: 방향에 따라 눈도 움직여요!
    - 🌈 **그라데이션 몸통**: 머리부터 꼬리까지 색이 변해요!
    """)

# 푸터
st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#aaa; padding:20px;">
        Made with 💚 for 당곡고 학생들 | 🎓 재미있게 플레이하세요!
    </div>
""", unsafe_allow_html=True)
