/* -------- タブ切り替え -------- */
const tabBtns = document.querySelectorAll('.tab-btn');
const sections = document.querySelectorAll('.tab-section');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));

        btn.classList.add('active');
        document.getElementById(btn.dataset.target).classList.add('active');
    });
});

function checkOrientation() {
    const warning = document.getElementById("rotate-warning");
    if (window.innerHeight > window.innerWidth) {
        warning.style.display = "flex";
    } else {
        warning.style.display = "none";
    }
}

window.addEventListener("resize", checkOrientation);
window.addEventListener("load", checkOrientation);

/* -------- 時計 -------- */
function updateClock(){
    const now = new Date();
    document.getElementById('clock').textContent =
        now.toLocaleTimeString('ja-JP', { hour12:false });
}
setInterval(updateClock, 1000);
updateClock();

/* -------- ストップウォッチ -------- */
let swInterval, swTime = 0;
const swDisplay = document.getElementById('stopwatch');

document.getElementById('sw-start').onclick = () => {
    clearInterval(swInterval);
    swInterval = setInterval(() => {
        swTime++;
        const h = String(Math.floor(swTime/3600)).padStart(2,'0');
        const m = String(Math.floor(swTime/60)%60).padStart(2,'0');
        const s = String(swTime%60).padStart(2,'0');
        swDisplay.textContent = `${h}:${m}:${s}`;
    },1000);
};

document.getElementById('sw-stop').onclick = () => clearInterval(swInterval);
document.getElementById('sw-reset').onclick = () => {
    clearInterval(swInterval);
    swTime = 0;
    swDisplay.textContent = "00:00:00";
};

// --- タイマー ---
let timerInterval;
let timerTime = 0;

const timerFinish = document.getElementById("timer-finish");

document.getElementById("timer-start").onclick = () => {
    const minutes = parseInt(document.getElementById("timer-min").value);
    timerTime = minutes * 60;

    clearInterval(timerInterval);

    timerInterval = setInterval(() => {
        if (timerTime <= 0) {
            clearInterval(timerInterval);
            timerFinish.classList.add("show");
            return;
        }
        timerTime--;
    }, 1000);
};

document.getElementById("timer-reset").onclick = () => {
    clearInterval(timerInterval);
    timerTime = 0;
};