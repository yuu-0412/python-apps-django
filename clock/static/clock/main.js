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

const clockDisplay = document.getElementById('clock');

document.getElementById('timer-start').onclick = () => {
    const t = document.getElementById('timer-time').value; // "00:30:00" みたいなのが入る
    if(!t) return;

    const [h, m, s] = t.split(":").map(Number);
    timerTime = h*3600 + m*60 + s;

    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if(timerTime <= 0){
            clearInterval(timerInterval);
            alert("時間です⏰");
            updateClock(); // 普通の時計に戻す
            return;
        }
        timerTime--;

        let mm = String(Math.floor(timerTime/60)).padStart(2,'0');
        let ss = String(timerTime%60).padStart(2,'0');

        // 時計表示をタイマー表示に変える
        clockDisplay.textContent = `${mm}:${ss}`;
    }, 1000);
};

document.getElementById('timer-reset').onclick = () => {
    clearInterval(timerInterval);
    updateClock();
};