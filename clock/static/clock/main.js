// タブ切り替え
const tabBtns = document.querySelectorAll('.tab-btn');
const tabSections = document.querySelectorAll('.tab-section');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        tabSections.forEach(sec => sec.classList.remove('active'));
        document.getElementById(btn.dataset.target).classList.add('active');
    });
});

// --- 時計 ---
function updateClock() {
    const clock = document.getElementById('clock');
    const now = new Date();
    clock.textContent = now.toLocaleTimeString('ja-JP', { hour12: false });
}
setInterval(updateClock, 1000);
updateClock();

// --- ストップウォッチ ---
let swInterval, swTime = 0;
const swDisplay = document.getElementById('stopwatch');

document.getElementById('sw-start').onclick = () => {
    clearInterval(swInterval);
    swInterval = setInterval(() => {
        swTime++;
        let h = String(Math.floor(swTime/3600)).padStart(2,'0');
        let m = String(Math.floor(swTime/60 % 60)).padStart(2,'0');
        let s = String(swTime%60).padStart(2,'0');
        swDisplay.textContent = `${h}:${m}:${s}`;
    }, 1000);
};

document.getElementById('sw-stop').onclick = () => clearInterval(swInterval);
document.getElementById('sw-reset').onclick = () => {
    clearInterval(swInterval);
    swTime = 0;
    swDisplay.textContent = "00:00:00";
};

// --- タイマー ---
let timerInterval, timerTime = 0;
const timerDisplay = document.getElementById('timer');

document.getElementById('timer-start').onclick = () => {
    const minutes = parseInt(document.getElementById('timer-min').value) || 0;
    timerTime = minutes * 60;
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        if(timerTime <= 0){
            clearInterval(timerInterval);
            alert("時間です⏰");
            return;
        }
        timerTime--;
        let m = String(Math.floor(timerTime/60)).padStart(2,'0');
        let s = String(timerTime%60).padStart(2,'0');
        timerDisplay.textContent = `${m}:${s}`;
    }, 1000);
};

document.getElementById('timer-reset').onclick = () => {
    clearInterval(timerInterval);
    timerTime = 0;
    timerDisplay.textContent = "00:00";
};