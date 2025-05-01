document.addEventListener("DOMContentLoaded", function () {
    const today = new Date();
    const oneWeekLater = new Date();
    oneWeekLater.setDate(today.getDate() + 7);

    function toJalali(gregorianDate) {
        var t, n, e = gregorianDate,
            i = parseInt(e.getFullYear()),
            o = parseInt(e.getMonth()) + 1,
            a = parseInt(e.getDate());
        i > 1600 ? (t = 979, i -= 1600) : (t = 0, i -= 621);
        var r = o > 2 ? i + 1 : i;
        return n = 365 * i + parseInt((r + 3) / 4) - parseInt((r + 99) / 100) + parseInt((r + 399) / 400) - 80 + a + [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][o - 1], t += 33 * parseInt(n / 12053), n %= 12053, t += 4 * parseInt(n / 1461), (n %= 1461) > 365 && (t += parseInt((n - 1) / 365), n = (n - 1) % 365), {
            year: t,
            month: n < 186 ? 1 + parseInt(n / 31) : 7 + parseInt((n - 186) / 30),
            day: 1 + (n < 186 ? n % 31 : (n - 186) % 30)
        };
    }

    const todayJalali = toJalali(today);
    const oneWeekLaterJalali = toJalali(oneWeekLater);

    jalaliDatepicker.startWatch({
        minDate: todayJalali,
        maxDate: oneWeekLaterJalali,
        changeMonth: false,
        changeYear: false,
        dayRendering: function (day, input) {

            const dayOfWeek = it(day.year, day.month, day.day);
            if (dayOfWeek === 6) {
                day.isValid = false;
                day.className += " disabled-friday";
            }
            return day;
        }
    });

    function it(year, month, day) {
        const a = (year - 1) * 365 + Math.floor((year) / 4) - Math.floor((year) / 100) + Math.floor((year) / 400);
        const b = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][month - 1];
        const totalDays = a + b + day;
        return (totalDays + 5) % 7;
    }
});