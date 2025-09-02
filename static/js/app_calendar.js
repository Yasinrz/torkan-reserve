String.prototype.getBaseConversionNumber = getBaseConversionNumber
String.prototype.CvnFromTo = CvnFromTo;
String.prototype.convertDigits = convertDigits;

var today = Date.now();
const todayFa = {
	"day": getDateFormat(today, {
		"day": "2-digit"
	}),
	"month": getDateFormat(today, {
		"month": "numeric"
	}),
	"monthTitle": getDateFormat(today, {
		"month": "long"
	}),
	"year": getDateFormat(today, {
		"year": "numeric"
	}),
	"dayWeek": getDateFormat(today, {
		"weekday": "long"
	}),
}

// index month to label
const monthLabel = [
	"فروردین",
	"اردیبهشت",
	"خرداد",
	"تیر",
	"مرداد",
	"شهریور",
	"مهر",
	"آبان",
	"آذر",
	"دی",
	"بهمن",
	"اسفند",
];

const headDOM = document.getElementsByTagName("head")[0];
const parentDateDOM = document.getElementsByClassName('num-dates')[0];
const parentMetaYearDOM = document.getElementsByClassName('year-wrapper')[0];
const parentEventsDOM = document.getElementsByClassName('calendar-left')[0];
const todayDateDOM = document.getElementsByClassName("num-date")[0];
const todayDayDOM = document.getElementsByClassName("day")[0];

// set Property
todayDateDOM.textContent = todayFa['day'].convertDigits("fa");
todayDayDOM.textContent = todayFa['dayWeek'].convertDigits("fa");

// Ensure we have a valid month
let currentMonth = todayFa.month;
if (!currentMonth || currentMonth < 1 || currentMonth > 12) {
	currentMonth = 1; // Default to first month if detection fails
}

// Function to generate calendar for a specific month
function generateMonthCalendar(monthNumber) {
	// Clear existing calendar content
	parentDateDOM.innerHTML = '';

	// Clear existing events
	const existingEvents = parentEventsDOM.querySelectorAll('.events-list');
	existingEvents.forEach(event => event.remove());

	const month = calendarObject[monthNumber - 1];
	const dateList = [];
	let UlCounter = 1;
	let oneStarted = false;

	// Add year info for this month
	parentMetaYearDOM.innerHTML = '';
	let tmpMetaYear = metaYear.metaYear[monthNumber - 1];
	tmpMetaYear = tmpMetaYear.split(" | ");
	parentMetaYearDOM.innerHTML += generateTemplateHTML("metaYear", {
		index: monthNumber,
		year: metaYear.year,
		arabic: tmpMetaYear[1],
		miladi: tmpMetaYear[0],
	});

	// Create event list for this month
	const eventClass = `event-list-${monthNumber}`;
	parentEventsDOM.innerHTML += `<ul class="events-list event-list-${monthNumber} dynamic-element dynamic-element-${monthNumber}"></ul>`;
	let eventDOM = document.getElementsByClassName(eventClass)[0];

	// Create calendar weeks for this month
	let currentWeek = [];

	for (const day of month) {
		const currentMonth = monthLabel[monthNumber - 1];

		// Check if this day belongs to the current month
		// day[5] indicates if it's from previous/next month
		if (day[5]) {
			oneStarted = false; // Day from previous/next month
		} else {
			oneStarted = true; // Day from current month
			dateList.push(day[0]);
		}

		// Add day to current week
		currentWeek.push(day);

		// When we have 7 days or reach the end of the month, create a week
		if (currentWeek.length === 7 || day === month[month.length - 1]) {
			// Fill remaining slots if week is not complete
			while (currentWeek.length < 7) {
				currentWeek.push(null); // Empty day placeholder
			}

			// Create week container
			var ulCurrentClass = `wk-${monthNumber}-${UlCounter}`;
			var htmlUL = '';
			htmlUL += `<ul class="week ${ulCurrentClass} month-${monthNumber} dynamic-element dynamic-element-${monthNumber}"></ul>`;
			parentDateDOM.innerHTML += htmlUL;

			var ulCurrent = document.getElementsByClassName(ulCurrentClass)[0];

			// Add days to the week in correct order
			for (let i = 0; i < 7; i++) {
				const dayData = currentWeek[i];

				if (dayData === null) {
					// Empty day cell
					ulCurrent.innerHTML += '<li class="day-element empty-day"></li>';
				} else {
					let liClass = "day-element ";

					// Apply disable-one class only to days from previous/next month
					if (dayData[5]) {
						liClass += "disable-one ";
					} else {
						liClass += `date-${monthNumber}-${dayData[0].convertDigits("en")} `;
					}

					// Check if this is today's date
					if (monthNumber === currentMonth && dayData[0] === parseInt(todayFa.day)) {
						liClass += "today ";
					}

					if (dayData[3] === true)
						liClass += "holiday ";

					ulCurrent.innerHTML += generateTemplateHTML('date', {
						class: liClass,
						jalali: dayData[0].toString().convertDigits("fa"),
						miladi: dayData[1],
						ghamari: dayData[2].toString().convertDigits("ar"),
					});
				}
			}

			// Add clearfix class to the week
			ulCurrent.classList.add("clearfix");

			// Reset for next week
			currentWeek = [];
			UlCounter++;
		}

		// Add events to the event list
		if (oneStarted && day[4] && day[4].length > 0) {
			for (const dayElement of day[4]) {
				const indexBracket = dayElement.indexOf("[");
				const eventdate = (0 <= indexBracket) ? dayElement.substring(indexBracket) : "";
				const eventTitle = dayElement.replace(eventdate, "");
				const startedDate = dateList[dateList.length - 1];

				eventDOM.innerHTML += generateTemplateHTML('events', {
					day: `${startedDate} ${currentMonth}`.convertDigits("fa"),
					eventTitle: eventTitle,
					date: eventdate,
				});
			}
		}
	}

	// Set active month button
	activeMonthElement('month-letter', `month-letter-${monthNumber}`, 'active-season-cr');

	// Set active day if it's today
	if (monthNumber === currentMonth) {
		activeMonthElement('day-element', `date-${monthNumber}-${parseInt(todayFa.day)}`, 'active-season');
	}
}

// Generate initial calendar for current month
generateMonthCalendar(currentMonth);

// event listener for month buttons
const monthLetter = document.getElementsByClassName("month-letter");
for (const element of monthLetter) {
	element.onclick = function (e) {
		const thisElement = e.target;
		if (thisElement.classList.contains("active-season-cr")) return;

		const monthDataNumber = parseInt(thisElement.getAttribute("data-num"));

		// Generate calendar for clicked month
		generateMonthCalendar(monthDataNumber);
	}
}

let season = getSeasonByMonNum(todayFa.month);
let cssSeason = getCssBySeason(season);

let styleCustom = document.getElementById("style-cln");

if (!styleCustom)
	headDOM.innerHTML += `<style id="style-cln">${cssSeason}</style>`;
else {
	styleCustom.innerHTML = cssSeason;
}

// Ensure current month is visible and active
setTimeout(() => {
	// Set active month button
	const activeMonthButton = document.querySelector(`.month-letter-${currentMonth}`);
	if (activeMonthButton) {
		activeMonthButton.classList.add('active-season-cr');
	}

	// Set active day if it's today
	activeMonthElement('day-element', `date-${currentMonth}-${parseInt(todayFa.day)}`, 'active-season');
}, 100);

// Additional initialization when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
	// Set active month button
	const activeMonthButton = document.querySelector(`.month-letter-${currentMonth}`);
	if (activeMonthButton) {
		activeMonthButton.classList.add('active-season-cr');
	}

	// Set active day if it's today
	activeMonthElement('day-element', `date-${currentMonth}-${parseInt(todayFa.day)}`, 'active-season');
});

function getSeasonByMonNum(numMonth) {
	const monthSeason = [
		"spring",
		"summer",
		"fall",
		"winter",
	];

	let season = "";

	if (numMonth <= 3) {
		season = monthSeason[0];
	} else if (3 < numMonth && numMonth <= 6) {
		season = monthSeason[1];
	} else if (6 < numMonth && numMonth <= 9) {
		season = monthSeason[2];
	} else if (9 < numMonth && numMonth <= 12) {
		season = monthSeason[3];
	}

	return season;
}

function getCssBySeason(season) {
	const cssObjects = cssProperty[season];
	let cssString = "";
	for (const cssObject of cssObjects) {
		let template = `${cssObject['selector']}{\n`;
		for (const property of cssObject['property']) {
			template += `${property}\n`;
		}
		template += "}\n\n"
		cssString += template;
	}

	return cssString;
}

function getDateFormat(uDate, option) {
	let date = new Intl.DateTimeFormat('fa-IR', option).format(uDate);
	date = date.convertDigits("en");
	return date;
}

function activeMonthElement(allCls, whichCls, activeCls) {
	const dynamicElement = document.getElementsByClassName(allCls);
	for (const element of dynamicElement) {
		if (element.classList.contains(activeCls))
			element.classList.remove(activeCls);
		else if (element.classList.contains(whichCls))
			element.classList.add(activeCls);
	}
}

function generateTemplateHTML(type, data) {
	let htmlTemplate = '';

	if (type == "date")
		htmlTemplate = `<li class="${data.class}"><span id="jalali">${data.jalali}</span><small id="miladi">${data.miladi}</small><small id="ghamari">${data.ghamari}</small></li>`;
	else if (type == "metaYear") {
		htmlTemplate = `<div class="year yr-${data.index} dynamic-element dynamic-element-${data.index}">${data.year}</div> <div class="year-meta myr-${data.index} dynamic-element dynamic-element-${data.index}">${data.arabic}<br>${data.miladi}</div>`;
	} else if (type == "events") {
		htmlTemplate = `<li><span class="event-day">${data.day} </span><div class="event-title">${data.eventTitle}</div><span class="event-date-type"> ${data.date}</span></li>`;
	}
	return htmlTemplate;
}

function convertDigits(to) {
	let str = this;
	const toCvn = (this.getBaseConversionNumber(to))[to];
	const allDigits = this.getBaseConversionNumber("all");

	delete allDigits[to];

	const Objkeys = Object.keys(allDigits);
	for (var i = 0; i < Objkeys.length; i++) {
		const currentKey = Objkeys[i];
		const fromCvn = allDigits[currentKey];
		str = this.CvnFromTo(fromCvn, toCvn, str)
	}
	return str;
}

function CvnFromTo(fromDigits, toDigits, str) {
	var str = str == undefined ? this : str;
	for (var i = 0; i < toDigits.length; i++) {
		const currentFromDigit = fromDigits[i];
		const currentToDigit = toDigits[i];
		const regex = new RegExp(currentFromDigit, 'g');
		str = str.replace(regex, currentToDigit);
	}
	return str;
}

function getBaseConversionNumber(label) {
	const faDigits = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰'];
	const enDigits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
	const arDigits = ['١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩', '٠'];

	var whichDigit = {};

	switch (label) {
		case 'fa':
			whichDigit[label] = faDigits;
			break;
		case 'en':
			whichDigit[label] = enDigits;
			break;
		case 'ar':
			whichDigit[label] = arDigits;
			break;
		case 'all':
			whichDigit = {
				"fa": faDigits,
				"en": enDigits,
				"ar": arDigits
			};
			break;
		default:
			whichDigit = [];
	}

	return whichDigit;
}

window.onkeyup = function (e) {
	const keyName = e.code;
	let action = null;

	if (keyName == "ArrowLeft") {
		action = "DECREASE";
	} else if (keyName == "ArrowRight") {
		action = "INCREASE";
	} else {
		return;
	}

	const activeMonthDOM = document.getElementsByClassName("active-season-cr")[0];
	const numberMonth = activeMonthDOM.getAttribute("data-num");

	let numberMonthFinal = 0;

	if (action == "INCREASE") {
		numberMonthFinal = parseInt(numberMonth) + 1;
	} else if (action == "DECREASE") {
		numberMonthFinal = parseInt(numberMonth) - 1;
	}

	if (numberMonthFinal == 0 || numberMonthFinal == 13) {
		numberMonthFinal = 1;
	}

	const newMonthDOM = document.getElementsByClassName("month-letter")[(numberMonthFinal - 1)];

	const eventClick = new Event("click");

	newMonthDOM.dispatchEvent(eventClick);
}