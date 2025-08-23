// window.addEventListener("DOMContentLoaded", function () {
//     const protocol = window.location.protocol === "https:" ? "wss" : "ws";
//     const socket = new WebSocket(protocol + "://" + window.location.host + "/ws/notifications/");

//     const icon = document.getElementById("notif-icon");
//     const dropdown = document.getElementById("notif-dropdown");
//     const notifList = document.getElementById("notif-list");
//     const notifCount = document.getElementById("notif-count");
//     const markAllRead = document.getElementById("mark-all-read");

//     let unreadCount = 0;

//     // Toggle dropdown (اصلاح: حذف ریست unreadCount)
//     icon.addEventListener("click", function (e) {
//         e.stopPropagation();
//         dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
//         // حذف شده: unreadCount = 0; و notifCount.style.display = "none";
//     });

//     // Mark all as read
//     markAllRead.addEventListener("click", function () {
//         notifList.innerHTML = '<li style="text-align:center; color:#888;">🔕 نوتیفیکیشنی وجود ندارد</li>';
//         unreadCount = 0;
//         notifCount.style.display = "none";
//     });

//     // Handle WebSocket messages
//     socket.onmessage = function (e) {
//         const data = JSON.parse(e.data);
//         addNotification(data.message, data.ticket_url, data.notif_type || "default");
//     };

//     function addNotification(message, url, notifType) {
//         // Remove empty message
//         const emptyMsg = notifList.querySelector("li");
//         if (emptyMsg && emptyMsg.innerText.includes("نوتیفیکیشنی وجود ندارد")) {
//             notifList.innerHTML = "";
//         }

//         // Create notification item
//         const li = document.createElement("li");
//         li.classList.add("unread");
//         li.style.padding = "12px 16px";
//         li.style.borderBottom = "1px solid rgba(255,255,255,0.1)";

//         // Add notification type icon
//         let icon = "🔔";
//         if (notifType === "employee_ticket") {
//             icon = "👨‍💼";
//         } else if (notifType === "reservation") {
//             icon = "📅";
//         } else if (notifType === "suggestion") {
//             icon = "💡";
//         }

//         // Add relative time
//         const time = new Date().toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });

//         li.innerHTML = `
//             <span class="notif-icon">${icon}</span>
//             <a href="${url}" style="text-decoration:none; color:#ffffff; display:block;">
//                 ${message}
//             </a>
//             <span class="notif-time">${time}</span>
//         `;

//         // Remove notification on click
//         li.querySelector("a").addEventListener("click", function (e) {
//             e.preventDefault();
//             li.style.animation = "fadeOut 0.3s ease";
//             setTimeout(() => {
//                 li.remove();
//                 unreadCount = Math.max(0, unreadCount - 1);
//                 notifCount.innerText = unreadCount;
//                 notifCount.style.display = unreadCount > 0 ? "inline-block" : "none";
//                 if (!notifList.children.length) {
//                     notifList.innerHTML = '<li style="text-align:center; color:#888;">🔕 نوتیفیکیشنی وجود ندارد</li>';
//                 }
//                 window.location.href = url;
//             }, 300);
//         });

//         notifList.prepend(li);

//         // Update count
//         unreadCount++;
//         notifCount.innerText = unreadCount;
//         notifCount.style.display = "inline-block";
//     }

//     // Fade out animation
//     const style = document.createElement("style");
//     style.innerHTML = `
//         @keyframes fadeOut {
//             from { opacity: 1; }
//             to { opacity: 0; height: 0; padding: 0; margin: 0; }
//         }
//     `;
//     document.head.appendChild(style);
// });