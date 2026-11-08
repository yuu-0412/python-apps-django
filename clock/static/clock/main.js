
/* =========================
   タブ切り替え
========================= */

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


/* =========================
   画面の向き
========================= */

function checkOrientation() {
    const warning = document.getElementById("rotate-warning");

    if (!warning) return;

    if (window.innerHeight > window.innerWidth) {
        warning.style.display = "flex";
    } else {
        warning.style.display = "none";
    }
}

window.addEventListener("resize", checkOrientation);
window.addEventListener("load", checkOrientation);


/* =========================
   時計
========================= */

function updateClock() {
    const clock = document.getElementById('clock');

    if (!clock) return;

    const now = new Date();

    clock.textContent = now.toLocaleTimeString('ja-JP', {
        hour12: false
    });
}

setInterval(updateClock, 1000);
updateClock();


/* =========================
   ストップウォッチ
========================= */

let swInterval = null;
let swTime = 0;

const swDisplay = document.getElementById('stopwatch');

document.getElementById('sw-start').onclick = () => {

    if (swInterval !== null) return;

    swInterval = setInterval(() => {

        swTime++;

        const h = String(Math.floor(swTime / 3600)).padStart(2, '0');
        const m = String(Math.floor(swTime / 60) % 60).padStart(2, '0');
        const s = String(swTime % 60).padStart(2, '0');

        swDisplay.textContent = `${h}:${m}:${s}`;

    }, 1000);
};


document.getElementById('sw-stop').onclick = () => {
    clearInterval(swInterval);
    swInterval = null;
};


document.getElementById('sw-reset').onclick = () => {

    clearInterval(swInterval);

    swInterval = null;
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

    for (let i = 0; i <= setting.max; i++) {

        const item = document.createElement("div");

        item.className = "wheel-item";
        item.textContent = String(i).padStart(2, "0");

        // 数字をクリックして選択
        item.onclick = () => {

            if (timerInterval !== null) return;

            const itemHeight = item.getBoundingClientRect().height;

            wheel.scrollTop = i * itemHeight;

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


// 数字1つ分の高さを取得
function getItemHeight(id) {

    const item = wheels[id].querySelector(".wheel-item");

    return item.getBoundingClientRect().height;
}


// 選択中の数字を更新
function updateSelected(id) {

    const wheel = wheels[id];
    const itemHeight = getItemHeight(id);

    const index = Math.round(wheel.scrollTop / itemHeight);

    wheel.querySelectorAll(".wheel-item").forEach((item, i) => {
        item.classList.toggle("selected", i === index);
    });
}


// ホイールを指定した数字に移動
function setWheel(id, value) {

    const wheel = wheels[id];
    const itemHeight = getItemHeight(id);

    wheel.scrollTo({
        top: value * itemHeight,
        behavior: "instant"
    });

    updateSelected(id);
}


// ホイールから選択中の数字を取得
function getWheelValue(id) {

    const wheel = wheels[id];
    const itemHeight = getItemHeight(id);

    const max = wheel.querySelectorAll(".wheel-item").length - 1;

    return Math.max(0, Math.min(
        Math.round(wheel.scrollTop / itemHeight),
        max
    ));
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


// ホイール操作の有効・無効
function setWheelEnabled(enabled) {

    Object.values(wheels).forEach(wheel => {
        wheel.style.pointerEvents = enabled ? "auto" : "none";
    });
}


// タイマーを00に戻す
function resetTimer() {

    clearInterval(timerInterval);

    timerInterval = null;
    timerTime = 0;

    setWheelEnabled(true);

    ["hours", "minutes", "seconds"].forEach(id => {

        const wheel = wheels[id];

        wheel.scrollTo({
            top: 0,
            behavior: "instant"
        });

        wheel.querySelectorAll(".wheel-item").forEach((item, index) => {
            item.classList.toggle("selected", index === 0);
        });

    });
}


// タイマー開始
document.getElementById("timer-start").onclick = () => {

    if (timerInterval !== null) return;

    // 選択した時間を取得
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
    setWheelEnabled(false);

    timerInterval = setInterval(() => {

        timerTime--;

        setTimerDisplay(timerTime);

        // タイマー終了
        if (timerTime <= 0

        ) {

            clearInterval(timerInterval);
            timerInterval = null;

            timerTime = 0;

            setWheelEnabled(true);

            // 終了画面を表示
            timerFinish.classList.remove("hidden");
        }

    }, 1000);
};


// タイマーリセット
document.getElementById("timer-reset").onclick = () => {

    resetTimer();

    // 終了画面を閉じる
    timerFinish.classList.add("hidden");
};


/* =========================
   タイマー終了画面
========================= */

// OKボタン
document.getElementById("finish-close").onclick = () => {

    // 終了画面を閉じる
    timerFinish.classList.add("hidden");

    // タイマーを初期状態に戻す
    resetTimer();
};
