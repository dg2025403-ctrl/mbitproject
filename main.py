import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🐍 스네이크 게임",
    page_icon="🐍",
    layout="centered"
)

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
st.markdown('<div class="sub-title">⌨️ 방향키 또는 WASD | 스페이스바로 시작!</div>', unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 650px;
        font-family: 'Arial', sans-serif;
    }

    .game-container {
        background: white;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 25px 70px rgba(0,0,0,0.4);
        text-align: center;
    }

    .score-board {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 15px;
    }

    .score-item {
        background: linear-gradient(135deg, #ffeaa7, #fab1a0);
        padding: 10px 25px;
        border-radius: 50px;
        font-size: 1.1em;
        font-weight: bold;
        color: #2d3436;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    canvas {
        border-radius: 16px;
        display: block;
        box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        cursor: pointer;
    }

    .controls {
        margin-top: 12px;
        color: #636e72;
        font-size: 0.9em;
    }

    .speed-wrap {
        margin-top: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-weight: bold;
        color: #2d3436;
    }

    input[type=range] {
        width: 140px;
        accent-color: #6c5ce7;
    }

    .btn {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        color: white;
        border: none;
        padding: 10px 28px;
        border-radius: 50px;
        font-size: 1em;
        font-weight: bold;
        cursor: pointer;
        margin-top: 12px;
        box-shadow: 0 5px 15px rgba(108,92,231,0.4);
        transition: transform 0.15s, box-shadow 0.15s;
    }

    .btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(108,92,231,0.6);
    }

    .overlay {
        position: absolute;
        inset: 0;
        border-radius: 16px;
        background: rgba(0,0,0,0.55);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.4em;
        font-weight: bold;
        text-align: center;
        line-height: 1.8;
        backdrop-filter: blur(3px);
        transition: opacity 0.3s;
    }

    .overlay.hidden { display: none; }

    .canvas-wrap {
        position: relative;
        display: inline-block;
    }
</style>
</head>
<body>
<div class="game-container">
    <div class="score-board">
        <div class="score-item">🏆 점수: <span id="score">0</span></div>
        <div class="score-item">⭐ 최고: <span id="high">0</span></div>
    </div>

    <div class="canvas-wrap">
        <canvas id="c" width="420" height="420"></canvas>
        <div class="overlay" id="overlay">
            🐍 스네이크 게임<br>
            <span style="font-size:0.65em; opacity:0.85;">스페이스바 또는 화면 클릭으로 시작</span>
        </div>
    </div>

    <div class="controls">⌨️ 방향키 / WASD 조작 &nbsp;|&nbsp; Space 시작·일시정지</div>

    <div class="speed-wrap">
        ⚡ 속도:
        <input type="range" id="spd" min="1" max="5" value="3" step="1">
        <span id="spdLabel">보통</span>
    </div>

    <button class="btn" onclick="resetGame()">🔄 새 게임</button>
</div>

<script>
// ── 캔버스 기본 설정 ──────────────────────────────────────
const canvas  = document.getElementById('c');
const ctx     = canvas.getContext('2d');
const overlay = document.getElementById('overlay');
const scoreEl = document.getElementById('score');
const highEl  = document.getElementById('high');
const spdSlider = document.getElementById('spd');
const spdLabel  = document.getElementById('spdLabel');

const W = canvas.width;
const H = canvas.height;
const COLS = 21;           // 격자 수
const ROWS = 21;
const TW = W / COLS;       // 타일 너비 (픽셀)
const TH = H / ROWS;

// ── 속도 설정 ─────────────────────────────────────────────
// stepInterval: 뱀이 한 칸 이동하는 데 걸리는 ms
const SPEEDS = [220, 160, 110, 75, 45];
const SPEED_LABELS = ['🐢 느림', '🚶 천천히', '⚡ 보통', '🏃 빠름', '🔥 매우 빠름'];
let stepInterval = SPEEDS[2];

spdSlider.addEventListener('input', () => {
    const idx = parseInt(spdSlider.value) - 1;
    stepInterval = SPEEDS[idx];
    spdLabel.textContent = SPEED_LABELS[idx];
});

// ── 게임 상태 ─────────────────────────────────────────────
let snake, dir, nextDir, food, score, highScore, particles;
let running, paused, dead;

// 보간용 (부드러운 이동)
let progress   = 0;   // 0 ~ 1  (현재 칸 → 다음 칸 진행률)
let lastStepTs = 0;   // 마지막 스텝 타임스탬프

highScore = parseInt(localStorage.getItem('snakeHi') || '0');
highEl.textContent = highScore;

// ── 초기화 ────────────────────────────────────────────────
function resetGame() {
    snake    = [{x:10, y:10}, {x:9, y:10}, {x:8, y:10}];
    dir      = {x:1,  y:0};
    nextDir  = {x:1,  y:0};
    score    = 0;
    particles = [];
    running  = false;
    paused   = false;
    dead     = false;
    progress = 0;
    scoreEl.textContent = 0;
    placeFood();
    showOverlay('🐍 스네이크 게임<br><span style="font-size:0.65em;opacity:0.85;">스페이스바 또는 화면 클릭으로 시작</span>');
    requestAnimationFrame(loop);
}

function placeFood() {
    let pos;
    do {
        pos = {x: Math.floor(Math.random()*COLS), y: Math.floor(Math.random()*ROWS)};
    } while (snake.some(s => s.x===pos.x && s.y===pos.y));
    food = pos;
}

// ── 오버레이 ──────────────────────────────────────────────
function showOverlay(html) {
    overlay.innerHTML = html;
    overlay.classList.remove('hidden');
}
function hideOverlay() {
    overlay.classList.add('hidden');
}

// ── 파티클 (먹을 때 반짝) ─────────────────────────────────
function spawnParticles(gx, gy) {
    const cx = (gx + 0.5) * TW;
    const cy = (gy + 0.5) * TH;
    for (let i = 0; i < 14; i++) {
        const angle = Math.random() * Math.PI * 2;
        const spd   = 1.5 + Math.random() * 3;
        particles.push({
            x: cx, y: cy,
            vx: Math.cos(angle) * spd,
            vy: Math.sin(angle) * spd,
            life: 1,
            decay: 0.03 + Math.random() * 0.03,
            r: Math.random() * 5 + 3,
            color: ['#e74c3c','#ff9f43','#ffeaa7','#55efc4'][Math.floor(Math.random()*4)]
        });
    }
}

function updateParticles() {
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.12;   // 중력
        p.life -= p.decay;
        p.r *= 0.97;
    });
}

function drawParticles() {
    particles.forEach(p => {
        ctx.save();
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI*2);
        ctx.fill();
        ctx.restore();
    });
}

// ── 게임 로직: 한 스텝 ────────────────────────────────────
function step() {
    // 방향 확정 (180도 반전 금지)
    if (!(nextDir.x === -dir.x && nextDir.y === -dir.y)) {
        dir = {...nextDir};
    }

    const head    = snake[0];
    const newHead = {x: head.x + dir.x, y: head.y + dir.y};

    // 벽 충돌
    if (newHead.x < 0 || newHead.x >= COLS || newHead.y < 0 || newHead.y >= ROWS) {
        gameOver(); return;
    }
    // 자기 몸 충돌 (꼬리는 이번 스텝에 제거되므로 마지막 제외)
    if (snake.slice(0, -1).some(s => s.x===newHead.x && s.y===newHead.y)) {
        gameOver(); return;
    }

    const ate = (newHead.x === food.x && newHead.y === food.y);
    snake.unshift(newHead);
    if (ate) {
        score += 10;
        scoreEl.textContent = score;
        if (score > highScore) {
            highScore = score;
            highEl.textContent = highScore;
            localStorage.setItem('snakeHi', highScore);
        }
        spawnParticles(food.x, food.y);
        placeFood();
    } else {
        snake.pop();
    }
}

function gameOver() {
    dead    = true;
    running = false;
    showOverlay(`💥 게임 오버!<br>🏆 ${score}점<br><span style="font-size:0.6em;opacity:0.8;">스페이스바로 다시 시작</span>`);
}

// ── 그리기 ────────────────────────────────────────────────
function drawBg() {
    for (let x = 0; x < COLS; x++) {
        for (let y = 0; y < ROWS; y++) {
            ctx.fillStyle = (x+y)%2===0 ? '#aad751' : '#a2d149';
            ctx.fillRect(x*TW, y*TH, TW, TH);
        }
    }
}

function drawFood() {
    const cx = (food.x + 0.5) * TW;
    const cy = (food.y + 0.5) * TH;
    const r  = TW * 0.42;

    // 사과 몸통
    ctx.fillStyle = '#e74c3c';
    ctx.beginPath();
    ctx.arc(cx, cy + 1, r, 0, Math.PI*2);
    ctx.fill();

    // 광택
    ctx.fillStyle = 'rgba(255,255,255,0.35)';
    ctx.beginPath();
    ctx.ellipse(cx - r*0.28, cy - r*0.28, r*0.28, r*0.18, -Math.PI/5, 0, Math.PI*2);
    ctx.fill();

    // 잎
    ctx.fillStyle = '#27ae60';
    ctx.beginPath();
    ctx.ellipse(cx + 2, cy - r - 1, 5, 3, Math.PI/4, 0, Math.PI*2);
    ctx.fill();

    // 꼭지
    ctx.strokeStyle = '#795548';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(cx, cy - r + 1);
    ctx.lineTo(cx + 2, cy - r - 4);
    ctx.stroke();
}

// 부드러운 뱀 그리기 ── 핵심 부분!
function drawSnake(t) {
    // t = progress (0~1): 이전 칸 → 현재 칸 이동 비율
    const len = snake.length;

    // 각 세그먼트의 실제 픽셀 위치 계산 (보간 적용)
    // snake[0] = 새 머리, snake[1] = 이전 머리 위치 …
    // progress=0 이면 이전 위치, progress=1 이면 새 위치
    function segPos(i) {
        // 현재 세그먼트와 "이전" 세그먼트(한 스텝 전에 이 자리에 있던 것)
        const cur  = snake[i];
        const prev = snake[i + 1] || snake[i]; // 꼬리 끝
        return {
            x: (prev.x + (cur.x - prev.x) * t + 0.5) * TW,
            y: (prev.y + (cur.y - prev.y) * t + 0.5) * TH
        };
    }

    // 경계선(path) 그리기
    // 몸통 두께
    const thickness = TW * 0.72;

    ctx.lineWidth   = thickness;
    ctx.lineJoin    = 'round';
    ctx.lineCap     = 'round';

    // 그라데이션 색 (머리 → 꼬리)
    const grad = ctx.createLinearGradient(
        segPos(0).x, segPos(0).y,
        segPos(len-1).x, segPos(len-1).y
    );
    grad.addColorStop(0,   '#2980b9');
    grad.addColorStop(0.4, '#3498db');
    grad.addColorStop(1,   '#74b9ff');

    ctx.strokeStyle = grad;
    ctx.beginPath();
    const p0 = segPos(0);
    ctx.moveTo(p0.x, p0.y);
    for (let i = 1; i < len; i++) {
        const p = segPos(i);
        ctx.lineTo(p.x, p.y);
    }
    ctx.stroke();

    // 머리 (더 진한 원)
    const head = segPos(0);
    ctx.fillStyle = '#1a6fa3';
    ctx.beginPath();
    ctx.arc(head.x, head.y, thickness/2, 0, Math.PI*2);
    ctx.fill();

    // 눈
    const eyeR = TW * 0.1;
    const d    = dir;
    // 방향에 수직인 벡터
    const perp = {x: -d.y, y: d.x};
    const eyeDist  = thickness * 0.3;
    const eyeFront = thickness * 0.22;

    for (let side of [-1, 1]) {
        const ex = head.x + d.x * eyeFront + perp.x * side * eyeDist;
        const ey = head.y + d.y * eyeFront + perp.y * side * eyeDist;
        // 흰자
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(ex, ey, eyeR, 0, Math.PI*2);
        ctx.fill();
        // 눈동자
        ctx.fillStyle = '#2d3436';
        ctx.beginPath();
        ctx.arc(ex + d.x*eyeR*0.3, ey + d.y*eyeR*0.3, eyeR*0.5, 0, Math.PI*2);
        ctx.fill();
    }
}

// ── 메인 루프 ─────────────────────────────────────────────
function loop(ts) {
    // 배경
    drawBg();

    if (running && !paused) {
        // 경과 시간 → progress 계산
        const elapsed = ts - lastStepTs;
        progress = Math.min(elapsed / stepInterval, 1);

        // 한 스텝 완료 → 실제 이동
        if (progress >= 1) {
            step();
            if (dead) { drawFood(); drawSnake(1); drawParticles(); return; }
            lastStepTs = ts;
            progress   = 0;
        }
    }

    drawFood();
    drawSnake(running && !paused ? progress : 1);
    updateParticles();
    drawParticles();

    requestAnimationFrame(loop);
}

// ── 입력 처리 ─────────────────────────────────────────────
document.addEventListener('keydown', e => {
    if (e.key === ' ') {
        e.preventDefault();
        if (dead) { resetGame(); return; }
        if (!running) {
            running = true; paused = false;
            lastStepTs = performance.now();
            hideOverlay();
        } else {
            paused = !paused;
            if (paused) showOverlay('⏸️ 일시정지<br><span style="font-size:0.65em;opacity:0.85;">스페이스바로 계속</span>');
            else { hideOverlay(); lastStepTs = performance.now(); }
        }
        return;
    }
    const map = {
        ArrowUp:    {x:0, y:-1}, w: {x:0, y:-1},
        ArrowDown:  {x:0, y:1},  s: {x:0, y:1},
        ArrowLeft:  {x:-1,y:0},  a: {x:-1,y:0},
        ArrowRight: {x:1, y:0},  d: {x:1, y:0}
    };
    const v = map[e.key] || map[e.key.toLowerCase()];
    if (v) { e.preventDefault(); nextDir = v; }
});

canvas.addEventListener('click', () => {
    if (dead) { resetGame(); return; }
    if (!running) {
        running = true; paused = false;
        lastStepTs = performance.now();
        hideOverlay();
    }
});

window.focus();
document.body.tabIndex = 0;
document.body.focus();

// 시작
resetGame();
</script>
</body>
</html>
"""

components.html(game_html, height=680)

st.info("💡 게임 화면을 한 번 클릭한 후 키보드를 조작하세요!")

with st.expander("📖 게임 방법"):
    st.markdown("""
    | 키 | 동작 |
    |---|---|
    | ⬆️⬇️⬅️➡️ / WASD | 방향 조작 |
    | **스페이스바** | 시작 / 일시정지 |
    | **속도 슬라이더** | 1~5단계 속도 |
    | **새 게임 버튼** | 리셋 |
    
    ### ✨ 부드러운 움직임의 비밀
    - 🎯 **보간(Interpolation)**: 격자 이동 사이를 픽셀 단위로 채워요!
    - 🔴 **파티클 효과**: 사과를 먹으면 반짝 터져요!
    - 👀 **눈동자**: 진행 방향 따라 눈이 움직여요!
    - 💾 **최고점수 자동 저장**
    """)

st.markdown("---")
st.markdown('<div style="text-align:center;color:#aaa;">Made with 💚 for 당곡고 학생들</div>', unsafe_allow_html=True)
