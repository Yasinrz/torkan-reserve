import { toJalali } from './datepicker-config.js';

document.addEventListener("DOMContentLoaded", function () {
    function updateDateTime() {
        let now = new Date().toLocaleString("en-US", { timeZone: "Asia/Tehran" });
        now = new Date(now);
        const jalali = toJalali(now);
        const weekdays = ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه"];
        const weekdayName = weekdays[now.getDay()];
        const h = String(now.getHours()).padStart(2, '0');
        const m = String(now.getMinutes()).padStart(2, '0');
        const s = String(now.getSeconds()).padStart(2, '0');
        document.getElementById("datetime").innerText =
            `${h}:${m}:${s} - ${jalali.year}/${jalali.month}/${jalali.day} -  ${weekdayName}`;
    }

    setInterval(updateDateTime, 1000);
    updateDateTime();
});
