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

/* =========================
   タイマー
========================= */

let timerInterval = null;
let timerTime = 0;

const timerFinish = document.getElementById("timer-finish");

// ホイール設定
const wheelSettings = [
    { id: "hours", max: 23 },
    { id: "minutes", max: 59 },
    { id: "seconds", max: 59 }
];

const wheels = {};

// ホイールを作成
wheelSettings.forEach(setting => {

    const wheel = document.getElementById(setting.id + "-wheel");
    const list = document.getElementById(setting.id + "-list");

    wheels[setting.id] = wheel;

    // 数字を作成
    for (let i = 0; i <= setting.max; i++) {

        const item = document.createElement("div");

        item.className = "wheel-item";
        item.textContent = String(i).padStart(2, "0");

        // 数字をクリックして選択
        item.onclick = () => {
            if (timerInterval !== null) return;

            wheel.scrollTop = i * 48;
            updateSelected(setting.id);
        };

        list.appendChild(item);
    }

    // スクロール時に選択数字を更新
    wheel.addEventListener("scroll", () => {
        updateSelected(setting.id);
    });

    updateSelected(setting.id);
});


// 選択中の数字を更新
function updateSelected(id) {

    const wheel = wheels[id];

    const index = Math.round(wheel.scrollTop / 48);

    wheel.querySelectorAll(".wheel-item").forEach((item, i) => {

        item.classList.toggle("selected", i === index);

    });
}


// ホイールを指定した数字に戻す
function setWheel(id, value) {

    const wheel = wheels[id];

    wheel.scrollTop = value * 48;

    updateSelected(id);
}


// ホイールから選択中の数字を取得
function getWheelValue(id) {

    return Math.round(wheels[id].scrollTop / 48);
}


// タイマーの残り時間をホイールに表示
function setTimerDisplay(seconds) {

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    setWheel("hours", hours);
    setWheel("minutes", minutes);
    setWheel("seconds", secs);
}


// 開始ボタン
document.getElementById("timer-start").onclick = () => {

    if (timerInterval !== null) return;

    // 初回はホイールの選択時間を取得
    if (timerTime === 0) {

        const hours = getWheelValue("hours");
        const minutes = getWheelValue("minutes");
        const seconds = getWheelValue("seconds");

        timerTime =
            hours * 3600 +
            minutes * 60 +
            seconds;

        if (timerTime <= 0) return;
    }

    // ホイール操作を無効化
    Object.values(wheels).forEach(wheel => {
        wheel.style.pointerEvents = "none";
    });

    timerInterval = setInterval(() => {

        timerTime--;

        setTimerDisplay(timerTime);

        // 0になったら終了
        if (timerTime <= 0) {

            clearInterval(timerInterval);
            timerInterval = null;

            timerTime = 0;

            Object.values(wheels).forEach(wheel => {
                wheel.style.pointerEvents = "auto";
            });

            timerFinish.classList.remove("hidden");
        }

    }, 1000);
};


// リセットボタン
document.getElementById("timer-reset").onclick = () => {

    clearInterval(timerInterval);
    timerInterval = null;

    timerTime = 0;

    // ホイール操作を有効化
    Object.values(wheels).forEach(wheel => {
        wheel.style.pointerEvents = "auto";
    });

    // 全部00に戻す
    setWheel("hours", 0);
    setWheel("minutes", 0);
    setWheel("seconds", 0);

    // 終了画面を閉じる
    timerFinish.classList.add("hidden");
};