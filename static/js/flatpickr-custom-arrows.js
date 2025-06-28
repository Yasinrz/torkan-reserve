document.addEventListener('DOMContentLoaded', function () {
    flatpickr(".big-timepicker", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true,
        locale: "fa",
        onReady: function (selectedDates, dateStr, instance) {
            setTimeout(function () {
                const inputs = instance.timeContainer.querySelectorAll('.numInputWrapper');
                inputs.forEach(wrapper => {
                    wrapper.querySelectorAll('.arrowUp, .arrowDown').forEach(el => el.remove());
                    const arrowContainer = document.createElement('div');
                    arrowContainer.className = 'custom-arrow-container';
                    const arrowUp = document.createElement('div');
                    arrowUp.className = 'custom-arrow custom-arrow-up';
                    arrowUp.onclick = function () {
                        const input = wrapper.querySelector('input');
                        input.stepUp();
                        input.dispatchEvent(new Event('change'));
                    };
                    const arrowDown = document.createElement('div');
                    arrowDown.className = 'custom-arrow custom-arrow-down';
                    arrowDown.onclick = function () {
                        const input = wrapper.querySelector('input');
                        input.stepDown();
                        input.dispatchEvent(new Event('change'));
                    };
                    arrowContainer.appendChild(arrowUp);
                    arrowContainer.appendChild(arrowDown);
                    // add container to wrapper
                    wrapper.appendChild(arrowContainer);
                    // set final style
                    wrapper.style.position = 'relative';
                    wrapper.querySelector('input').style.paddingRight = '25px';
                });
            }, 300);
        }
    });
});