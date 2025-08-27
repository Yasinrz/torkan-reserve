document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("datetime");

    function toPersianDigits(input) {
        const persianMap = {
            '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
            '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
        };
        return String(input).replace(/[0-9]/g, d => persianMap[d]);
    }

    function updateDateTime() {
        let now = new Date().toLocaleString("en-US", { timeZone: "Asia/Tehran" });
        now = new Date(now);

        const h = String(now.getHours()).padStart(2, '0');
        const m = String(now.getMinutes()).padStart(2, '0');
        const s = String(now.getSeconds()).padStart(2, '0');

        const timeHtml = `
            <div class="clock-time" dir="rtl">
                <span class="digit">${toPersianDigits(s)}</span>
                <span class="colon">:</span>
                <span class="digit">${toPersianDigits(m)}</span>
                <span class="colon">:</span>
                <span class="digit">${toPersianDigits(h)}</span>
            </div>
        `;

        container.innerHTML = timeHtml;
    }

    setInterval(updateDateTime, 1000);
    updateDateTime();
});
