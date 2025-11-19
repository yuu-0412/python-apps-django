function updateClock() {
    const clock = document.getElementById('clock');
    const now = new Date();

    // 時・分・秒を取得
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    // 2桁表示に調整
    hours = hours.toString().padStart(2, '0');
    minutes = minutes.toString().padStart(2, '0');
    seconds = seconds.toString().padStart(2, '0');

    // 表示更新
    clock.textContent = `${hours}:${minutes}:${seconds}`;
}

// ページ読み込み時と1秒ごとに更新
document.addEventListener('DOMContentLoaded', () => {
    updateClock();
    setInterval(updateClock, 1000);
})