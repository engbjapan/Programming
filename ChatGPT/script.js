const pong = document.getElementById('pong');
const ball = document.getElementById('ball');
const paddle1 = document.getElementById('paddle1');
const paddle2 = document.getElementById('paddle2');
const score1Display = document.getElementById('score1');
const score2Display = document.getElementById('score2');
const gameoverText = document.getElementById('gameover-text');
const startButton = document.getElementById('start-button');
const delayInput = document.getElementById('delay-input');
const speedIncrementInput = document.getElementById('speed-increment-input');
let intervalId;
let paddle1TimerId;
let paddle1Y = 200;
let paddle2Y = 200;
let ballX = 400;
let ballY = 200;
let ballSpeedX = 3;
let ballSpeedY = 3;
let score1 = 0;
let score2 = 0;
let paddleHeight = 80;
let paddleWidth = 10;
let ballRadius = 10;
let paddle1Delay = parseInt(delayInput.value);
let speedIncrement = parseInt(speedIncrementInput.value);
let gameStarted = false;
let gameRunning = false;

// 指定した周波数の音を指定した回数だけ繰り返し再生し、一定間隔で停止する関数
function playTone(frequency, volume, duration, interval, repetitions, waveType = 'sine') {
  const audioContext = new (window.AudioContext || window.webkitAudioContext)();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();

  oscillator.type = waveType;
  oscillator.frequency.value = frequency;

  gainNode.gain.value = volume;

  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);

  for (let i = 0; i < repetitions; i++) {
    oscillator.start(audioContext.currentTime + i * (duration + interval) / 1000);
    oscillator.stop(audioContext.currentTime + (i + 1) * (duration + interval) / 1000);
  }
}

function increaseBallSpeed() {
  const maxSpeed = 8;
  const increment = Math.min(speedIncrement, maxSpeed);
  ballSpeedX += Math.sign(ballSpeedX) * increment;
  ballSpeedY += Math.sign(ballSpeedY) * increment;

  const colorIncrement = 255 / maxSpeed;
  const currentSpeed = Math.abs(ballSpeedX);
  const redValue = Math.max(0, 255 - colorIncrement * currentSpeed);
  const blueValue = Math.max(0, 255 - colorIncrement * currentSpeed);
  ball.style.fill = `rgb(${redValue}, 0, ${blueValue})`;
}

function playBeepSound(duration) {
  playTone(800, 0.1, duration, 50);
}

function playGoalSound() {
  playTone(400, 0.1, 200, 100);
}

function playGameOverSound() {
  playTone(200, 0.2, 500, 200, 3);
}

function update() {
  if (!gameRunning) {
    return;
  }

  ballX += ballSpeedX;
  ballY += ballSpeedY;

  if (ballY < ballRadius || ballY > 400 - ballRadius) {
    ballSpeedY *= -1;
    playBeepSound(100);
  }

  if (ballX < paddleWidth + ballRadius && ballY > paddle1Y && ballY < paddle1Y + paddleHeight) {
    ballSpeedX *= -1;
    playBeepSound(100);
  }

  if (ballX > 800 - paddleWidth - ballRadius && ballY > paddle2Y && ballY < paddle2Y + paddleHeight) {
    ballSpeedX *= -1;
    playBeepSound(100);
  }

  if (ballX < 0) {
    score2++;
    playGoalSound();
    reset();
  }

  if (ballX > 800) {
    score1++;
    playGoalSound();
    reset();
  }

  ball.style.transform = `translate(${ballX}px, ${ballY}px)`;
  paddle1.style.transform = `translateY(${paddle1Y}px)`;
  paddle2.style.transform = `translateY(${paddle2Y}px)`;
  score1Display.textContent = score1;
  score2Display.textContent = score2;

  if (score1 === 5 || score2 === 5) {
    gameoverText.style.visibility = 'visible';
    clearInterval(intervalId);
    clearInterval(paddle1TimerId);
    playGameOverSound();
    startButton.disabled = false;
  }
console.log('ボールの位置:', ballX, ballY);
console.log('パドル1の位置:', paddle1Y);
console.log('パドル2の位置:', paddle2Y);
console.log('スコア1:', score1);
console.log('スコア2:', score2);
}

function reset() {
  ballX = 400;
  ballY = 200;
  ballSpeedX = 3;
  ballSpeedY = 3;
}

function handleMouseMove(event) {
  console.log('マウス移動イベントが発生しました');
  console.log('マウスのY座標:', event.clientY);

  const boundingRect = pong.getBoundingClientRect();
  const mousePosition = event.clientY - boundingRect.top;
  console.log('マウス位置の計算結果:', mousePosition);

  paddle1Y = Math.min(400 - paddleHeight, mousePosition);
  console.log('パドル1のY座標:', paddle1Y);
}

function handlePaddle1Movement() {
  const centerOfPaddle = paddle1Y + paddleHeight / 2;

  if (centerOfPaddle < ballY - 35) {
    paddle1Y += 6;
  } else if (centerOfPaddle > ballY + 35) {
    paddle1Y -= 6;
  }
}

startButton.addEventListener('click', function () {
  if (gameRunning) {
    stopGame();
  } else {
    startGame();
  }
});

function startGame() {
  if (gameRunning) {
    stopGame();
    startButton.textContent = 'ゲーム開始';
  } else {
    scoreReset();
    reset();
    gameoverText.style.visibility = 'hidden';
    //startButton.disabled = true; //startButtonは常に有効にする
    paddle1Delay = parseInt(delayInput.value);
    speedIncrement = parseInt(speedIncrementInput.value);
    intervalId = setInterval(update, 1000 / 60);
    pong.addEventListener('mousemove', handleMouseMove);
    gameStarted = true;
    paddle1TimerId = setInterval(handlePaddle1Movement, 1000 / 60);
    gameRunning = true;
    startButton.textContent = 'ゲーム停止';
  }
}

function stopGame() {
  clearInterval(intervalId);
  clearInterval(paddle1TimerId);
  startButton.disabled = false;
  gameRunning = false;
}

delayInput.addEventListener('change', function () {
  if (!gameStarted) {
    paddle1Delay = parseInt(delayInput.value);
  }
});

speedIncrementInput.addEventListener('change', function () {
  speedIncrement = parseInt(speedIncrementInput.value);
});

function scoreReset() {
  score1 = 0;
  score2 = 0;
}
